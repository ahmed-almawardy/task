import datetime
from decimal import Decimal
from aiohttp import web
from models import User, Balance, DEFAULT_AMOUNT, Transaction
from requests import status_codes


async def create_user(request):
    """Create user to db with inital balance 0.00 """
    data = await request.json()
    user = await User.create(name=data['name'])
    balance = await Balance.create(user_id=user.id)
    return web.json_response({
        'id': user.id,
        'name': user.name,
        'balance': str(balance.amount),
    }, status=status_codes.codes.CREATED)


async def get_user_balance(request):
    """Get a user with his own balance in a specfic date if not return only user with empty balance"""
    user_id = int(request.match_info.get('user_id'))
    date = request.query.get('date', None)
    where_args = (User.id == user_id,)
    if date:
        timestamp = datetime.datetime.fromisoformat(date)
        where_args = (Balance.timestamp == timestamp and User.id == user_id, )
    balance = await Balance.load(user=User).where(*where_args).order_by(Balance.id.desc()).gino.first()

    return web.json_response({
        'id': user_id,
        'balance': str(balance),
    }, status=status_codes.codes.OK)


async def get_transaction(request):
    """get a transaction"""
    tranasction_id = request.match_info.get('id')
    tranasction = await Transaction.get(tranasction_id)
    return web.json_response(data=tranasction.json(), status=status_codes.codes.OK)


async def create_transaction(request):
    """Create transction in DB , i have hard-coded it to avoid any uneeded data to be passed"""
    data = await request.json()

    for key in Transaction.REQUIRED_FIELDS:
        if not data.get(key):
            raise Exception(f'this field \'{key}\' is required')

    create_data = {
        "uid": data.get('uid'),
        'type': data['type'],
        'user_id': data['user_id'],
        'amount': Decimal(data['amount']),
        'timestamp': datetime.datetime.fromisoformat(data['timestamp'])
    }

    transaction = await Transaction.get(data.get('uid'))
    if transaction:
        return web.json_response(data=transaction.json(), status=status_codes.codes.CREATED)

    user = await User.get(data['user_id'])

    last_balance = await Balance.load(user=User).order_by(Balance.id.desc()).where(User.id==user.id).gino.first()
    if create_data['type'] == Transaction.TransactionTypes[0] and last_balance.amount < create_data['amount']:
        return web.json_response(data={'msg': "insufficient funds", 'balance': str(last_balance.amount)}, status=402)
    elif create_data['type'] == Transaction.TransactionTypes[0]:
        new_balance = last_balance.amount - create_data['amount']
    else:
        new_balance = last_balance.amount + create_data['amount']
    new_balance = new_balance if new_balance > DEFAULT_AMOUNT else DEFAULT_AMOUNT
    await Balance.create(user_id=user.id, amount=new_balance, timestamp=create_data['timestamp'])

    transaction = await Transaction.create(**create_data)
    return web.json_response(data=transaction.json(), status=status_codes.codes.CREATED)



async def create_user_balance(request):
    """Add balance to current user """
    data = await request.json()
    user_id = int(request.match_info.get('id'))
    balance = await Balance.create(amount=Decimal(data['amount']), user_id=user_id)
    return web.json_response(
        data={'balance': str(balance.amount)},
        status=status_codes.codes.CREATED)


def add_routes(app):
    app.router.add_route('POST', r'/v1/user', create_user, name='create_user')
    app.router.add_route('GET', r'/v1/user/{user_id}', get_user_balance, name='get_user_balance')
    app.router.add_route('POST', r'/v1/transaction', create_transaction, name='create_transaction')
    app.router.add_route('GET', r'/v1/transaction/{id}', get_transaction, name='incoming_transaction')
    app.router.add_route('POST', r'/v1/user/{id}/balance', create_user_balance, name='create_user_balance')

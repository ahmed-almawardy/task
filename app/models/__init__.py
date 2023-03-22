import datetime
from decimal import Decimal

from gino import Gino
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import TIMESTAMP
from sqlalchemy import text


db = Gino()


DEFAULT_AMOUNT = Decimal('0.00')


class Balance(db.Model):
    __tablename__ = 'balances'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(precision=5, scale=2), default=DEFAULT_AMOUNT)
    timestamp = db.Column(TIMESTAMP(timezone=False), server_default=text('now()'), nullable=False)
    _user = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    def __str__(self) -> str:
        return  f'{self.amount:.2f}'


class User(db.Model):
    """Model for table users in DB"""
    __tablename__ = 'users'

    def __init__(self, **kw):
        super().__init__(**kw)
        self._balances = set()
        self._transactions = set()

    @property
    def transactions(self):
        return self._transactions

    @transactions.setter
    def transactions(self, transaction):
        self._transactions.add(transaction)

    @property
    def balances(self):
        return self._balances

    @balances.setter
    def balances(self, balance):
        self._balances.add(balance)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(TIMESTAMP(timezone=False), server_default=text('now()'), nullable=False, unique=True)

    def __str__(self) -> str:
        return str(self.id)


class Transaction(db.Model):
    """Model for table transactions in DB"""
    __tablename__ = 'transactions'
    uid = db.Column(UUID(as_uuid=False), primary_key=True, default=str(uuid4()), unique=True)
    type = db.Column(db.String(8), nullable=False)
    amount = db.Column(db.Numeric(precision=5, scale=2))
    timestamp = db.Column(TIMESTAMP(timezone=False), server_default=text('now()'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    REQUIRED_FIELDS = {'type', 'amount', 'user_id'}
    TransactionTypes = ['WITHDRAW', 'DEPOSIT']

    def __str__(self) -> str:
        return str(self.uid)


    @classmethod
    async def create(cls, *args, **kwargs):
        type = kwargs.pop('type', '').upper()
        if type and type not in cls.TransactionTypes:
            raise ValueError('Type only is DEPOSIT, WITHDRAW')
        return await super().create(type=type, *args, **kwargs)

    def json(self):
        return {
            "uid": str(self.uid),
            "timestamp": str(self.timestamp),
            "user_id": self.user_id,
            "amount": str(self.amount),
            "type": self.type
        }

import uvloop
from aiohttp import web

from app import init_app


def create_app() -> web.Application:
    return init_app()


def main() -> None:
    uvloop.install()
    app = create_app()
    web.run_app(app, host=app['config'].HOST, port=app['config'].PORT)


if __name__ == '__main__':
    main()

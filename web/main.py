import os
import asyncio
import logging
import pathlib

import aiohttp_jinja2
import jinja2
from aiohttp import web

from restApi.routes import setup_routes
from restApi.utils import init_redis, load_config
from restApi.vod_histories.views import VodHandler

PROJ_ROOT = pathlib.Path(__file__).parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'


async def setup_redis(app, conf, loop):
    pool = await init_redis(conf['redis'], loop)

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool


def setup_jinja(app):
    loader = jinja2.FileSystemLoader(str(TEMPLATES_ROOT))
    jinja_env = aiohttp_jinja2.setup(app, loader=loader)
    return jinja_env


async def init(loop):
    conf = load_config(PROJ_ROOT / 'configs' / 'config.yml')

    app = web.Application(loop=loop)
    redis_pool = await setup_redis(app, conf, loop)
    setup_jinja(app)

    handler = VodHandler(redis_pool, conf)

    setup_routes(app, handler, PROJ_ROOT)
    # host, port = conf['host'], conf['port']
    return app


def run_web():
    logging.basicConfig(level=logging.DEBUG)
    print("ahihi")
    print("REDIS_HOST: " + os.environ["REDIS_HOST"])
    loop = asyncio.get_event_loop()

    return loop.run_until_complete(init(loop))


# gunicorn main:app --bind localhost:6969 --worker-class aiohttp.worker.GunicornWebWorker

app = run_web()
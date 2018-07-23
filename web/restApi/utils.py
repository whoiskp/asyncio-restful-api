import os
import aioredis
import trafaret as t  # TODO: for check validate dict in request
import yaml
from aiohttp import web


# TODO: Load data from *.yml file
def load_config(fname):
    with open(fname, 'rt') as f:
        data = yaml.load(f)

    return data


# TODO: create redis pool
# docs: http://aioredis.readthedocs.io/en/v0.2.9/api_reference.html
async def init_redis(loop):
    """
    Init redis pool
    :minsize (int) – Minimum number of free connection to create in pool. 1 by default.
    :maxsize (int) – Maximum number of connection to keep in pool. 10 by default.
    Must be greater then 0. None is disallowed.
    :param loop:
    :return:
    """
    redis_host = os.environ["REDIS_HOST"]
    redis_port = os.environ["REDIS_PORT"]
    redis_minsize = int(os.environ["REDIS_MINSIZE"])
    redis_maxsize = int(os.environ["REDIS_MAXSIZE"])
    pool = await aioredis.create_redis_pool(
        (redis_host, redis_port),
        minsize=redis_minsize,
        maxsize=redis_maxsize,
        loop=loop
    )
    return pool


# For valid json request
# docs: http://trafaret.readthedocs.io/en/latest/
VodHistoryData = t.Dict({
    t.Key('user_id'): t.Int,
    t.Key('object_id'): t.String,
    t.Key('episode_num'): t.Int,
    t.Key('elapsed_time'): t.Int,
})


def fetch_data(data):
    """
    TODO: check data is valid with temp_data (VodHistoryData)
    FIXME: () write decorator for reuse function with any format data just by send func *_temp()
    :param data: to parse in VodHistory
    :return:
    """
    try:
        data = VodHistoryData(data)
    except t.DataError:
        raise web.HTTPBadRequest('data is not valid')

    return data

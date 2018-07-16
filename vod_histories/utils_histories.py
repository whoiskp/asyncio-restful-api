import asyncio
import random
import uuid

from redis import Redis

from config import DevConfig
from vod_histories import Config as vod_conf

try:
    import cPickle as pickle
except ImportError:  # pragma: no cover
    import pickle

redis = Redis(host=DevConfig.REDIS_HOST, port=DevConfig.REDIS_POST, db=DevConfig.REDIS_DB)


async def add_vod_history_redis(vod_history_data):
    """
    add {object_id} to [redis list] by key 'history:list:<user_id>'
    add { episode_num, elapsed_time } to key 'history:<user_id>:<object_id>'
    :param vod_history: <dict> { object_id, user_id, episode_num, elapsed_time }
    :return: True || False
    """

    # vod_history_data = json.loads(vod_history_json)
    user_id = vod_history_data['user_id']
    object_id = vod_history_data['object_id']
    episode_num = vod_history_data['episode_num']
    elapsed_time = vod_history_data['elapsed_time']

    key_list_vod_user = vod_conf.LIST_VOD_USER_HISTORY_KEY_PATTERN % user_id

    if redis.llen(key_list_vod_user) == vod_conf.MAX_VOD_HISTORY_PER_USER:
        vod_remove = redis.rpop(key_list_vod_user)
        key_vod_remove = vod_conf.VOD_HISTORY_KEY_PATTERN % (user_id, vod_remove)
        redis.delete(key_vod_remove)

    # add newest data to top
    redis.lrem(key_list_vod_user, object_id, 1)
    redis.lpush(key_list_vod_user, object_id)

    key_vod_add = vod_conf.VOD_HISTORY_KEY_PATTERN % (user_id, object_id)
    data_vod_add = {"episode_num": int(episode_num), "elapsed_time": int(elapsed_time)}

    # add data to redis with timeout
    redis.set(key_vod_add, pickle.dumps(data_vod_add), vod_conf.VOD_HISTORY_TIMEOUT)

    print("done!")
    return True


def get_vod_history_redis(user_id, object_id):
    key_vod_add = vod_conf.VOD_HISTORY_KEY_PATTERN % (user_id, object_id)
    result = redis.get(key_vod_add)
    if result is None:
        return None
    print(f'result: {result}')
    result_json = pickle.loads(result)
    print(f'result json: {result_json}')
    return result_json


def get_vod_history_user_redis(user_id):
    key_list_vod_user = vod_conf.LIST_VOD_USER_HISTORY_KEY_PATTERN % user_id
    results = redis.lrange(key_list_vod_user, 0, -1)
    return [rs.decode('utf-8') for rs in results]


# Testing problem
MAX_NUMBER_USER_FOR_TEST = 10000
MAX_VOD_FOR_TEST = 100


def get_uuid():
    return str(uuid.uuid4()).replace('-', '')


async def init_data_for_test():
    VOD_HIS_TEMP = {'user_id': str(""), 'object_id': str(""), "episode_num": int(0), "elapsed_time": int(0)}
    current_users = redis.keys("histories:list:*")

    if len(current_users) > MAX_NUMBER_USER_FOR_TEST:
        return

    # redis.flushall()

    # init all data
    for _ in range(0, MAX_NUMBER_USER_FOR_TEST):
        vod_history_data = VOD_HIS_TEMP

        vod_history_data['user_id'] = get_uuid()

        for i in range(0, MAX_VOD_FOR_TEST):
            vod_history_data['object_id'] = i
            vod_history_data['episode_num'] = random.randint(1, 100)
            vod_history_data['elapsed_time'] = random.randint(1, 100)

            result = await add_vod_history_redis(vod_history_data)
            print("result: " + str(result))

    for user in redis.keys("histories:list:*"):
        user_id = str(user.decode('utf-8')).rsplit(":")[-1]
        print(user_id)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    asyncio.ensure_future(init_data_for_test())

    loop.run_forever()

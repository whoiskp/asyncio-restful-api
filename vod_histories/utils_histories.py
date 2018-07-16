from redis import Redis
from vod_histories import Config as vod_conf
from config import DevConfig

try:
    import cPickle as pickle
except ImportError:  # pragma: no cover
    import pickle

redis = Redis(host=DevConfig.REDIS_HOST, port=DevConfig.REDIS_POST)


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

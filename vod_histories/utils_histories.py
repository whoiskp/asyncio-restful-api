from redis import Redis
import json
try:
    import cPickle as pickle
except ImportError:  # pragma: no cover
    import pickle

redis = Redis(host="localhost", port=6379)

NUM_USER_TEST = 10
MAX_VOD_HISTORY_PER_USER = 100
VOD_POST_TEMP = { 'user_id': str(""), 'object_id': str(""), "episode_num": int(0), "elapsed_time": int(0)}

LIST_VOD_USER_HISTORY_KEY_PATTERN = "histories:list:%s"
VOD_HISTORY_KEY_PATTERN = "histories:%s:%s"


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

    key_list_vod_user = LIST_VOD_USER_HISTORY_KEY_PATTERN % user_id

    if redis.llen(key_list_vod_user) == MAX_VOD_HISTORY_PER_USER:
        vod_remove = redis.rpop(key_list_vod_user)
        key_vod_remove = VOD_HISTORY_KEY_PATTERN % (user_id, vod_remove)
        redis.delete(key_vod_remove)

    # add newest data to top
    redis.lrem(key_list_vod_user, object_id, 1)
    redis.lpush(key_list_vod_user, object_id)

    key_vod_add = VOD_HISTORY_KEY_PATTERN % (user_id, object_id)
    data_vod_add = {"episode_num": int(episode_num), "elapsed_time": int(elapsed_time)}

    redis.set(key_vod_add, pickle.dumps(data_vod_add))

    print("done!")
    return True


def get_vod_history_redis(user_id, object_id):
    key_vod_add = VOD_HISTORY_KEY_PATTERN % (user_id, object_id)
    result = redis.get(key_vod_add)
    if result is None:
        return None
    print(f'result: {result}')
    result_json = pickle.loads(result)
    print(f'result json: {result_json}')
    return result_json


def get_vod_history_user_redis(user_id):
    key_list_vod_user = LIST_VOD_USER_HISTORY_KEY_PATTERN % user_id
    results = redis.lrange(key_list_vod_user, 0, -1)
    return [rs.decode('utf-8') for rs in results]

import os
from aiohttp import web

try:
    import cPickle as pickle
except ImportError:  # pragma: no cover
    import pickle


class VodController:
    def __init__(self, redis):
        self._redis = redis

    async def add_vod_history_redis(self, vod_history_data):
        """
        add {object_id} to [redis list] by key 'history:list:<user_id>'
        add { episode_num, elapsed_time } to key 'history:<user_id>:<object_id>'
        :param vod_history_data: <dict> { object_id, user_id, episode_num, elapsed_time }
        :return: True || False
        """
        vod_timeout_secs = int(os.environ["VOD_TIMEOUT_SECS"])

        # vod_history_data = json.loads(vod_history_json)
        user_id = vod_history_data['user_id']
        object_id = vod_history_data['object_id']
        episode_num = vod_history_data['episode_num']
        elapsed_time = vod_history_data['elapsed_time']

        key_list_vod_user = os.environ["VOD_LIST_VOD_USER"] % user_id
        print(f'key: {key_list_vod_user}')
        len_vod_user = await self._redis.llen(key_list_vod_user)

        if len_vod_user == int(os.environ['VOD_MAX_VOD_PER_USER']):
            vod_remove = await self._redis.rpop(key_list_vod_user)
            key_vod_remove = os.environ['VOD_HISTORY'] % (user_id, vod_remove)
            await self._redis.delete(key_vod_remove)

        # delete all value
        await self._redis.lrem(key_list_vod_user, count=len_vod_user, value=object_id)
        # add newest data to top
        await self._redis.lpush(key_list_vod_user, object_id)

        key_vod_add = os.environ['VOD_HISTORY'] % (user_id, object_id)
        print(f'key vod add: {key_vod_add}')
        data_vod_add = {"episode_num": int(episode_num), "elapsed_time": int(elapsed_time)}

        # add data to redis with timeout
        return await self._redis.set(
            key_vod_add,
            pickle.dumps(data_vod_add),
            expire=vod_timeout_secs
        )

    async def get_vod_history_redis(self, user_id, object_id):

        key_vod_add = os.environ['VOD_HISTORY'] % (user_id, object_id)
        result = await self._redis.get(key_vod_add)
        if not result:
            return web.HTTPNotFound('Not found data')
        print(f'result: {result}')
        result_json = pickle.loads(result)
        print(f'result json: {result_json}')
        return result_json

    async def get_vod_history_user_redis(self, user_id):
        key_list_vod_user = os.environ["VOD_LIST_VOD_USER"] % user_id
        print(f'key: {key_list_vod_user}')
        results = await self._redis.lrange(key_list_vod_user, 0, -1)
        print(results)
        return [rs.decode('utf-8') for rs in results]

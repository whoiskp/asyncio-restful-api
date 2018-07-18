import aiohttp_jinja2
from aiohttp import web

from .utils import fetch_data

try:
    import cPickle as pickle
except ImportError:  # pragma: no cover
    import pickle


class Vod_handler:
    def __init__(self, redis, conf):
        self._redis = redis
        self._conf = conf

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {}

    async def get_list_vod_history_user(self, request):
        user_id = request.match_info['user_id']
        response = {'result': int(0), 'msg': 'Success', 'data': {}}
        data = await self.__get_vod_history_user_redis(user_id)
        print(data)
        if not data:
            response['msg'] = "not found!"
            return web.json_response(data=response, status=404)

        response['data'] = data
        return web.json_response(data=response)

    async def get_vod_history(self, request):
        user_id = request.match_info['user_id']
        object_id = request.match_info['object_id']
        response = {'result': int(0), 'msg': 'Success', 'data': {}}
        data = await self.__get_vod_history_redis(user_id, object_id)
        if data is None:
            response['msg'] = "not found!"
            return web.json_response(data=response, status=404)
        print(data)
        response['data'] = data
        return web.json_response(data=response)

    async def post_vod_history(self, request):
        data = await request.json()
        # check validate request
        vod_history_data = fetch_data(data)
        result = await self.__add_vod_history_redis(vod_history_data)
        response = {'result': int(0), 'msg': 'Success', 'data': result}
        return web.json_response(data=response)

    async def __add_vod_history_redis(self, vod_history_data):
        """
        add {object_id} to [redis list] by key 'history:list:<user_id>'
        add { episode_num, elapsed_time } to key 'history:<user_id>:<object_id>'
        :param vod_history_data: <dict> { object_id, user_id, episode_num, elapsed_time }
        :return: True || False
        """
        vod_conf = self._conf['vod']

        print(f"vod timeout {vod_conf['vod_timeout_secs']}")

        # vod_history_data = json.loads(vod_history_json)
        user_id = vod_history_data['user_id']
        object_id = vod_history_data['object_id']
        episode_num = vod_history_data['episode_num']
        elapsed_time = vod_history_data['elapsed_time']

        key_list_vod_user = vod_conf['list_vod_user'] % user_id
        print(f'key: {key_list_vod_user}')
        len_vod_user = await self._redis.llen(key_list_vod_user)

        if len_vod_user == vod_conf['max_vod_per_user']:
            vod_remove = await self._redis.rpop(key_list_vod_user)
            key_vod_remove = vod_conf['vod_history'] % (user_id, vod_remove)
            await self._redis.delete(key_vod_remove)

        # add newest data to top
        await self._redis.lrem(key_list_vod_user, count=1, value=object_id)
        await self._redis.lpush(key_list_vod_user, object_id)

        key_vod_add = vod_conf['vod_history'] % (user_id, object_id)
        print(f'key vod add: {key_vod_add}')
        data_vod_add = {"episode_num": int(episode_num), "elapsed_time": int(elapsed_time)}

        # add data to redis with timeout
        return await self._redis.set(
            key_vod_add,
            pickle.dumps(data_vod_add),
            expire=vod_conf['vod_timeout_secs']
        )

    async def __get_vod_history_redis(self, user_id, object_id):
        vod_conf = self._conf['vod']

        key_vod_add = vod_conf['vod_history'] % (user_id, object_id)
        result = await self._redis.get(key_vod_add)
        if not result:
            return web.HTTPNotFound('Not found data')
        print(f'result: {result}')
        result_json = pickle.loads(result)
        print(f'result json: {result_json}')
        return result_json

    async def __get_vod_history_user_redis(self, user_id):
        key_list_vod_user = self._conf['vod']['list_vod_user'] % user_id
        print(f'key: {key_list_vod_user}')
        results = await self._redis.lrange(key_list_vod_user, 0, -1)
        print(results)
        return [rs.decode('utf-8') for rs in results]

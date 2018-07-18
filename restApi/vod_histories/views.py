import aiohttp_jinja2
from aiohttp import web
from restApi.utils import fetch_data
from .controller import VodController


class VodHandler:
    def __init__(self, redis, conf):
        self._controller = VodController(redis, conf)

    @aiohttp_jinja2.template('vod_histories/index.html')
    async def index(self, request):
        return {}

    async def get_list_vod_history_user(self, request):
        user_id = request.match_info['user_id']
        response = {'result': int(0), 'msg': 'Success', 'data': {}}
        data = await self._controller.get_vod_history_user_redis(user_id)
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
        data = await self._controller.get_vod_history_redis(user_id, object_id)
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
        result = await self._controller.add_vod_history_redis(vod_history_data)
        response = {'result': int(0), 'msg': 'Success', 'data': result}
        return web.json_response(data=response)

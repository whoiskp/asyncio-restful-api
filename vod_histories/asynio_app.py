from aiohttp import web

from config import DevConfig
from utils_histories import add_vod_history_redis, get_vod_history_redis, get_vod_history_user_redis


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def handler_list_user_id(request):
    user_id = request.match_info['user_id']
    response = {'result': int(0), 'msg': 'Success', 'data': {}}
    data = get_vod_history_user_redis(user_id)
    print(data)
    if data.__len__() == 0:
        response['msg'] = "not found!"
        return web.json_response(data=response, status=404)

    response['data'] = data
    return web.json_response(data=response)


async def get_vod_history(request):
    user_id = request.match_info['user_id']
    object_id = request.match_info['object_id']
    response = {'result': int(0), 'msg': 'Success', 'data': {}}
    data = get_vod_history_redis(user_id, object_id)
    if data is None:
        response['msg'] = "not found!"
        return web.json_response(data=response, status=404)
    print(data)
    response['data'] = data
    return web.json_response(data=response)


async def post_vod_history(request):
    data = await request.json()
    result = await add_vod_history_redis(data)
    response = {'result': int(0), 'msg': 'Success', 'data': result}
    return web.json_response(data=response)


app = web.Application()

app.add_routes([web.get('/', handle),
                web.get('/histories/list/{user_id}', handler_list_user_id),
                web.get('/histories/{user_id}/{object_id}', get_vod_history),
                web.post('/histories/add', post_vod_history)
                ])

if __name__ == '__main__':
    web.run_app(app, host=DevConfig.WEB_APP_HOST, port=DevConfig.WEB_APP_POST)
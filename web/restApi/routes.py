def setup_routes(app, handler, project_root):
    router = app.router
    h = handler
    router.add_get(
        '/',
        h.index,
        name='index'
    )
    router.add_get(
        '/histories/list/{user_id}',
        h.get_list_vod_history_user,
        name='get_list_vod_history_user'
    )
    router.add_get(
        '/histories/{user_id}/{object_id}'
        , h.get_vod_history,
        name='get_vod_history'
    )
    router.add_post(
        '/histories/add',
        h.post_vod_history,
        name='post_vod_history'
    )
    router.add_static(
        '/static/',
        path=str(project_root / 'templates' / 'static'),
        name='static'
    )

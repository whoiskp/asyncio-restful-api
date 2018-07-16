class Config:
    LIST_VOD_USER_HISTORY_KEY_PATTERN = "histories:list:%s"
    VOD_HISTORY_KEY_PATTERN = "histories:%s:%s"

    VOD_POST_TEMP = {'user_id': str(""), 'object_id': str(""), "episode_num": int(0), "elapsed_time": int(0)}

    # Each user has max 100 vod
    MAX_VOD_HISTORY_PER_USER = 100
    # 30 days
    VOD_HISTORY_TIMEOUT = 2592000

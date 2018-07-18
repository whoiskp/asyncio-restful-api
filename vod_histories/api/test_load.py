import asyncio
import random
import uuid

# Testing problem
from vod_histories.utils_histories import add_vod_history_redis

MAX_NUMBER_USER_FOR_TEST = 10000
MAX_VOD_FOR_TEST = 100

redis = ""
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
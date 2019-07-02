
import redis


class RedisHelper:
    def __init__(self, host, port, db):
        self.__redis = redis.StrictRedis(host, port, db)

    def get(self, key):
        if self.__redis.exists(key):
            return self.__redis.get(key)
        else:
            return ""

    def set(self, key, value):
        self.__redis.set(key, value)


if __name__ == "__main__":

    rd = RedisHelper(host='localhost', port=6379, db=1)
    rd.set('louis', 'hello world!')
    print(rd.get('louis'))

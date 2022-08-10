import redis
from user_follow.models import UserFollow

from .graphqlTypes import UserFollowType, UserType

import json

class RedisService:
    def __init__(self) -> None:
        self.redis = redis.StrictRedis(host="localhost", port=6379,db=0, charset="utf-8", decode_responses=True)
        
    def redis_and_db(self,key,userId,isFollowing=True):
        data = self.redis.get(key)


        if data is None or len(data) == 2:
            print("miss")
            if isFollowing:
                ufs = UserFollow.objects.filter(source_id=userId) 
                ufs_return = [x.destination.id for x in ufs]
            else:
                ufs = UserFollow.objects.filter(destination_id=userId)
                ufs_return = [x.source.id for x in ufs]

            ufs_redis = [x.getJson() for x in ufs]



            ufs_str = json.dumps(ufs_redis)

            self.redis.set(key, ufs_str)
            return ufs_return
        else:
            print("hit")
            ufs_str = json.loads(data)

            ufs = []
            for x in ufs_str:
                uf = UserFollowType(**x)

                uf.source = UserType(**x['source'])
                uf.destination = UserType(**x['destination'])

                ufs.append(uf.source.id)

            return ufs
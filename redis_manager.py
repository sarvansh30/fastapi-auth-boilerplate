import redis.asyncio as redis
import os
from typing import Optional

# This is a proper way to setup redis client in big projects
class RedisManager:
    def __init__(self):
        self.url = os.getenv("REDIS_URL")
        self.pool :Optional[redis.ConnectionPool] = None
        self.client : Optional[redis.Redis] = None
    
    async def redis_init(self):

        self.pool = redis.ConnectionPool.from_url(
            self.url,
            max_connections = 20,
            decode_responses = True
        )

        self.client = redis.Redis(connection_pool=self.pool)
        try:
            await self.client.ping()
        except Exception as err:
            print(err)
        else:
            print("Redis connection intialised.")
        
    async def close_redis(self):
        try:
            if self.client:
                await self.client.close()
            if self.pool:
                await self.pool.disconnect()
        except Exception as e:
                print(e)
        
        else:
            print("Redis connection closed")
    
    def get_redis(self) -> redis.Redis:
        if not self.client:
            raise RuntimeError("Redis server not intialised")
        
        return self.client
    

redis_manager = RedisManager()

async def get_redis() -> redis.Redis:
    return redis_manager.get_redis()
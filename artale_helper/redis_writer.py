import redis
import time
import random
from datetime import datetime, timedelta
from collections import deque

class RedisWriter:
    def __init__(self, host='192.168.1.100', port=6379, db=0, channel="smega_content"):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.pubsub = self.redis.pubsub()
        self.channel = channel
        self.dedup_queue = deque(maxlen=50)
        
    def store_string(self, content):
        """存储字符串到Redis，包含内容和时间戳，设置2天过期"""
        if content in self.dedup_queue:
            return
        else:
            self.dedup_queue.append()

        # 创建包含内容和时间戳的数据结构
        data = {
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        
        # 生成唯一键
        key = f"string:{time.time()}:{random.randint(1000, 9999)}"
        
        # 存储到Redis，设置24小时过期
        self.redis.hmset(key, data)
        self.redis.expire(key, timedelta(days=1).total_seconds())
        
        # 发布通知
        self.redis.publish(self.channel, data)
        
        print(f"存储成功: {key} - {content}")
        return key
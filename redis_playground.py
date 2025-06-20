import redis

# 替换为你的 Mac 局域网 IP（通过 ipconfig getifaddr en0 获取）
REDIS_HOST = '192.168.1.100'  
REDIS_PORT = 6379

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    
    # 测试 PING 命令
    response = r.ping()
    print("Redis 连接成功！PING 响应:", response)
    
    # 简单数据操作示例
    r.set('test_key', 'Hello Redis!')
    print("获取 test_key:", r.get('test_key'))
    
except Exception as e:
    print("连接失败:", e)
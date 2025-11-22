import requests
import hashlib
import time
import random
from urllib.parse import quote

def generate_callback():
    """生成 jQuery JSONP 回调函数名"""
    random_num = ''.join([str(random.randint(0, 9)) for _ in range(21)])
    timestamp = int(time.time() * 1000)
    return f"jQuery{random_num}_{timestamp}"

def crc32_like_js(id, timestamp=None):
    """生成 rem 参数"""
    if timestamp is None:
        timestamp = int(time.time() * 1000)
    combined = f"music.gdstudio.xyz|20251104|{str(timestamp)[:9]}|{quote(id)}"
    return hashlib.md5(combined.encode()).hexdigest()[-8:].upper()

def generate_request(id):
    """生成完整的请求"""
    callback = generate_callback()
    crc = crc32_like_js(id)
    
    # 查询参数
    params = {
        'callback': callback
    }
    
    # 请求体数据
    data = {
        'types': 'search',
        'count': '20',
        'source': 'spotify', 
        'pages': '1',
        'name': id,
        's': crc
    }
    
    return params, data

# 使用示例
id = "taylor swift"
params, data = generate_request(id)
print("查询参数 params:")
print(params)
print("\n请求体 data:")
print(data)

# 发送请求
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
response = requests.post(
    'https://music.gdstudio.xyz/api.php',
    params=params,
    data=data,
    headers=headers
)
print("\n完整URL:")
print(response.url)
print("\n响应:")
print(response.text)
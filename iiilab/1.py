import time
import hashlib
from urllib.parse import urlparse
import requests
def encrypt(url, salt="2HT8gjE3xL"):
    # 从URL中提取二级域名
    domain = urlparse(url).netloc.split('.')[-2]
    
    # 自动生成时间戳
    timestamp = str(int(time.time()))
    hash_string = f"{url}{domain}{timestamp}{salt}"
    print(hash_string)
    return hashlib.md5(hash_string.encode()).hexdigest(),timestamp
if __name__ == "__main__":
    url="https://service.iiilab.com/iiilab/extract"
    target_url="https://www.douyin.com/jingxuan?modal_id=7507815791161527552"

    g_footer,g_timestamp=encrypt(target_url)
    res=requests.post(url,json={
        "url":target_url,
        "site":urlparse(target_url).netloc.split('.')[-2]
    },headers={
        "G-Footer":g_footer,
        "G-Timestamp":g_timestamp
    })
    print(res.json())
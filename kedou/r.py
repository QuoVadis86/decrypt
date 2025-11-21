import json
import base64
import random
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def encrypt_url(youtube_url):
    """
    加密YouTube URL，返回RSA加密的Base64结果

    Args:
        youtube_url: YouTube视频URL

    Returns:
        Base64编码的RSA加密结果
    """
    # 固定参数
    RSA_PUBLIC_KEY_BASE64 = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkJZWIUIje8VjJ3okESY8stCs/a95hTUqK3fD/AST0F8mf7rTLoHCaW+AjmrqVR9NM/tvQNni67b5tGC5z3PD6oROJJ24QfcAW9urz8WjtrS/pTAfGeP/2AMCZfCu9eECidy16U2oQzBl9Q0SPoz0paJ9AfgcrHa0Zm3RVPL7JvOUzscL4AnirYImPsdaHZ52hAwz5y9bYoiWzUkuG7LvnAxO6JHQ71B3VTzM3ZmstS7wBsQ4lIbD318b49x+baaXVmC3yPW/E4Ol+OBZIBMWhzl7FgwIpgbGmsJSsqrOq3D8IgjS12K5CgkOT7EB/sil7lscgc22E5DckRpMYRG8dwIDAQAB"
    AES_KEY = "kedou@8989!63336"
    IV_BASE64 = "a2Vkb3VAODk4OSE2MzIzMw=="

    # 1. 构造请求数据并序列化
    request_data = {"url": youtube_url}
    json_string = json.dumps(request_data, separators=(",", ":"), ensure_ascii=False)

    # 2. AES加密
    key_bytes = AES_KEY.encode("utf-8")
    iv_bytes = base64.b64decode(IV_BASE64)
    data_bytes = json_string.encode("utf-8")

    aes_cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    aes_encrypted = base64.b64encode(
        aes_cipher.encrypt(pad(data_bytes, AES.block_size))
    ).decode("utf-8")

    # 3. RSA加密
    rsa_key = RSA.import_key(base64.b64decode(RSA_PUBLIC_KEY_BASE64))
    rsa_cipher = PKCS1_v1_5.new(rsa_key)
    rsa_encrypted = base64.b64encode(
        rsa_cipher.encrypt(aes_encrypted.encode("utf-8"))
    ).decode("utf-8")

    return rsa_encrypted


# 使用示例
if __name__ == "__main__":
    # 输入YouTube URL
    target_url = "https://www.youtube.com/shorts/snYZs99YUNI"
    url = "https://www.kedou.life/api/video/extract/v2"
    # 获取加密结果
    encrypted_result = encrypt_url(target_url)

    print("加密结果:")
    print(encrypted_result)
    random_ip = ".".join(
        str(random.randint(0, 255)) for _ in range(4)
    )  # 生成随机IP地址.绕开次数限制
    res = requests.post(
        url, json=encrypted_result, headers={"X-Forwarded-For": random_ip}
    )
    print(res.json())
#Twitter、YouTube、哔哩哔哩、西瓜视频、好看视频、微博、搜狐视频、
# 今日头条、网易新闻、Instagram、VK、Vimeo、Weverse、AcFun、
# 抖音、快手、微视、斗鱼、知乎、咪咕视频、皮皮搞笑、虎牙、YY直播、小红书、
# 花椒直播、Dzen、Reddit、Melon、IMDb、Afreecatv、茶杯狐、樱花动漫
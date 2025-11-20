import base64
import hashlib
import struct
import time
from Crypto.Cipher import AES
import urllib.parse
import requests


def encode(url, proxy=True):
    if isinstance(url, bytes):
        url = url.decode("utf-8")
    encoded = urllib.parse.quote(url, safe="")
    return f"url={encoded}{'&proxyip=on' if proxy else ''}"


def build_query(url):

    timestamp = int(time.time() * 1000)
    # 构建hash字符串并计算MD5
    hash_string = f"{url}%8vcf{timestamp}"
    md5_hash = hashlib.md5(hash_string.encode()).hexdigest()

    # 返回查询字符串
    return f"hash={md5_hash}&timestamp={timestamp}"


def words_to_key(words, sig_bytes):
    """将 CryptoJS 的 words 数组转换为 AES 密钥字节（大端序）"""
    byte_array = bytearray()
    for word in words:
        byte_array.extend(struct.pack(">I", word & 0xFFFFFFFF))
    return bytes(byte_array[:sig_bytes])


def encrypt(url_data):
    """
    加密函数，输入URL参数字符串，返回加密结果

    Args:
        url_data: URL参数字符串，如 "url=https%3A%2F%2Fwww.douyin.com%2Fjingxuan%3Fmodal_id%3D7571527285208091940&proxyip=on"

    Returns:
        str: Base64 编码的加密结果
    """
    # 固定的密钥 words 数组
    key_words = [
        1681142116,
        946037817,
        946221104,
        1647456308,
        1698248752,
        809056568,
        1701013048,
        875706213,
    ]
    sig_bytes = 32

    # 转换密钥
    key_bytes = words_to_key(key_words, sig_bytes)

    # PKCS7 填充
    data_bytes = url_data.encode("utf-8")
    block_size = 16
    padding_length = block_size - (len(data_bytes) % block_size)
    padded_data = data_bytes + bytes([padding_length] * padding_length)

    # AES ECB 加密
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    encrypted = cipher.encrypt(padded_data)

    # Base64 编码
    return base64.b64encode(encrypted).decode("utf-8")


def parse_base64(base64_string):
    """
    模拟 CryptoJS.enc.Base64.parse() 功能
    正确处理有符号整数

    Args:
        base64_string: Base64 编码的字符串

    Returns:
        dict: 包含 words 数组和 sigBytes 的字典
    """
    # 1. Base64 解码为字节
    data_bytes = base64.b64decode(base64_string)

    # 2. 转换为 words 数组，正确处理有符号整数
    words = []
    padded_data = data_bytes.ljust((len(data_bytes) + 3) // 4 * 4, b"\x00")

    for i in range(0, len(padded_data), 4):
        # 使用有符号整数解析
        word = struct.unpack(">i", padded_data[i : i + 4])[0]  # 有符号整数
        words.append(word)

    # 3. 返回结果
    return {"words": words, "sigBytes": len(data_bytes)}


def words_to_hex(word_array):
    """
    模拟 CryptoJS WordArray 的 toString(CryptoJS.enc.Hex) 功能
    将 WordArray 转换为十六进制字符串

    Args:
        word_array: 包含 words 和 sigBytes 的字典

    Returns:
        str: 十六进制字符串
    """
    words = word_array["words"]
    sig_bytes = word_array["sigBytes"]

    # 将 words 转换回字节
    byte_array = bytearray()
    for word in words:
        # 将有符号整数转换为无符号字节（大端序）
        byte_array.extend(struct.pack(">i", word))

    # 只取有效字节数
    result_bytes = bytes(byte_array[:sig_bytes])

    # 转换为十六进制字符串
    hex_string = result_bytes.hex()

    return hex_string


# 完整流程示例
if __name__ == "__main__":
    target_url = "https://www.douyin.com/jingxuan?modal_id=7571527285208091940"  # 要解析的目标链接
    url = "https://www.parsevideo.com/parsevideo/enc.html?"  # 服务地址

    query_url = url + build_query(target_url)  # 可以返回时间戳和hash,用params传参
    print(query_url)

    encode_url = encode(target_url)
    base64_string = encrypt(encode_url)

    # 第一步：Base64 解析
    word_array = parse_base64(base64_string)
    print(f"WordArray: {word_array}")
    # 第二步：转换为十六进制
    hex_result = words_to_hex(word_array)
    print(f"十六进制结果: {hex_result}")

    # 发送POST请求，设置明确的请求头
    headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {"data": hex_result}

    res = requests.post(
        query_url,
        cookies={"PHPSESSID": "s22fut4int3p725c3q8pls805t"},
        headers=headers,
        data=data,
    )
    # TODO:搞清楚phpsessid怎么来的，以及怎么解析响应体
    print(res.content)  # 输出响应内容

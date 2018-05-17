# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_login import LoginManager
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from app.config import config
# 扩展模块支持
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
moment = Moment()

# 全局配置
app_conf = config['dev']


# 创建用例APP
def create_app(conf_name):
    global app_conf
    conf = config[conf_name]

    # 配置
    app_conf = conf
    app = Flask(__name__)
    app.config.from_object(conf)
    conf.init_app(app)
    CSRFProtect(app)

    # 模块初始化
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    admin = Admin(app, name='WITS系统后台管理', template_mode='bootstrap3')

    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'

    # 视图模块导入
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .org import org_blueprint
    app.register_blueprint(org_blueprint, url_prefix='/org')
    from .home import home_blueprint
    app.register_blueprint(home_blueprint, url_prefix='/home')
    from .api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # 数据表导入
    from app.models import User, Org, Project, TestCase, TestCaseResult, SysDict
    from flask_admin.contrib.sqla import ModelView
    admin.add_view(ModelView(User, db.session, name='用户'))
    admin.add_view(ModelView(Org, db.session, endpoint='organization', name='组织'))     # org_blueprint的名字冲突
    admin.add_view(ModelView(Project, db.session, name='项目'))
    admin.add_view(ModelView(TestCase, db.session, name='测试用例'))
    admin.add_view(ModelView(TestCaseResult, db.session, name='用例结果'))
    admin.add_view(ModelView(SysDict, db.session, name='数据字典'))

    return app

# -*- coding: utf-8 -*-
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('dev')

# 添加命令行
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    from app.models import User, Org, Project, TestCase, TestCaseResult, SysDict
    return dict(db=db, User=User, Org=Org,
                Project=Project, TestCase=TestCase, TestCaseResult=TestCaseResult, SysDict=SysDict)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    print(app.url_map)
    app.run()

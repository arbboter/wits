# -*- coding: utf-8 -*-
from app import create_app, db


def db_init():
    app = create_app('dev')
    with app.app_context():
        db.create_all()
        quit(0)
    app.run()


if __name__ == '__main__':
    # db_init()
    app = create_app('dev')
    print(app.url_map)
    app.run()

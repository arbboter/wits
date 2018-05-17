# -*- coding: utf-8 -*-
import json

def main():
    pass


def to_encode(data, encoding='utf-8'):
    if type(data) == str:
        return data.encode(encoding)
    return data


# 判断是否为json字符串
def is_json(s):
    try:
        json.loads(s, strict=False)
        return True
    except Exception as err:
        # print(err, '->', s)
        return False


# 判断是否为json字符串是否为空
def is_json_null(s):
    try:
        # 为空
        if not s:
            return True

        # 空白串
        js = s.strip()
        if len(js) == 0:
            return True

        # 空json
        jd = json.loads(s)
        if len(jd) > 0:
            return False
        else:
            return True
    except:
        return False


# 获取用户输入，提供输入字典
def get_input(dd):
    ret = {}
    for d in dd:
        ui = input('please input [' + d + '], ' + dd[d] + ':')
        if ui:
            ret[d] = ui
    return ret


# sqlal转json
class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            from sqlalchemy.ext.declarative import DeclarativeMeta
            import datetime
            if isinstance(obj.__class__, DeclarativeMeta):
                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    data = obj.__getattribute__(field)
                    try:
                        json.dumps(data)  # this will fail on non-encodable values, like other classes
                        fields[field] = data
                    except TypeError:  # 添加了对datetime的处理
                        if isinstance(data, datetime.datetime):
                            fields[field] = data.isoformat()
                        elif isinstance(data, datetime.date):
                            fields[field] = data.isoformat()
                        elif isinstance(data, datetime.timedelta):
                            fields[field] = (datetime.datetime.min + data).time().isoformat()
                        else:
                            fields[field] = None
                return fields
            return json.JSONEncoder.default(self, obj)


# 字符串转json串，支持中文
def dumps(txt):
    if is_json(txt):
        data = json.loads(txt)
        return json.dumps(data, ensure_ascii=False)
    else:
        ret = {'msg': '非法json格式串', 'text': txt}
        return json.dumps(ret, ensure_ascii=False)


# 字符串转json串，支持中文
def loads(txt):
    if is_json(txt):
        data = json.loads(txt)
        return data
    else:
        ret = {'msg': '非法json格式串', 'text': txt}
        return ret


if __name__ == '__main__':
    main()

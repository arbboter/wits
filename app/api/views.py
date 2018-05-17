# -*- coding: utf-8 -*-
from . import api_blueprint as app
import json


@app.route('/run_case_test', methods=['GET', 'POST'])
def run_case_test():
    from app.comm import run_case
    from app.comm import util

    url = 'http://p.3.cn/prices/mgets'
    para = {"skuIds": 954086, "type": 1}
    headers = None

    code, msg = run_case.run_test_case(url=url, para=para, headers=headers)

    ret = {'status': code, 'msg': util.loads(msg)}
    print(json.dumps(ret, ensure_ascii=False))
    return json.dumps(ret, ensure_ascii=False)

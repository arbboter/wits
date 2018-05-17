# -*- coding: utf-8 -*-
from app.api import api_blueprint as app
import json
from app.models import TestCase
from flask import jsonify, request


@app.route('/szxl/run_case_test')
def szxl_run_case_test():
    from app.comm import run_case
    from app.comm import util

    url = 'http://p.3.cn/prices/szxl/mgets'
    para = {"skuIds": 954086, "type": 1}
    headers = None

    code, msg = run_case.run_test_case(url=url, para=para, headers=headers)

    ret = {'status': code, 'msg': util.loads(msg)}
    print(json.dumps(ret, ensure_ascii=False))
    return json.dumps(ret, ensure_ascii=False)


# 执行测试用例并把结果入库
def szxl_run_case(case, run_name):
    from app.busi.szxl.main import run_api_case
    from app.comm.util import dumps
    ret = run_api_case(url=case.url, method=case.method, para=json.loads(case.para))
    if ret:
        print(ret)
        from app.models import TestCaseResult
        r = TestCaseResult(name=run_name, uid=case.uid, cid=case.id, url=case.url, method=case.method, type=case.type,
                           headers=case.headers, validate_rsp=case.validate_rsp, para=case.para,
                           dealed_para=dumps(ret['dealed_req']), rsp=ret['rsp'], dealed_rsp=ret['dealed_rsp'],
                           code=str(ret['status']), msg=ret['msg'])
        r.commit()
    return jsonify(ret)


@app.route('/szxl/run_case/<int:cid>')
def szxl_run_case_by_id(cid):
    case_info = TestCase.query.filter_by(id=cid).first()
    if not case_info:
        return jsonify(status=604, msg=u'测试用例id[%d]不存在' % cid)
    # 入参执行测试用例名字
    run_name = request.args.get('batch_name')
    if not run_name:
        from app.comm.stime import timestamp
        run_name = case_info.name + '-' + timestamp()
    return szxl_run_case(case_info, run_name)

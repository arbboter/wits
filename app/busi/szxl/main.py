# -*- coding: utf-8 -*-
import app.comm.slog as slog
import app.comm.util as util
import app.comm.run_case as run_case
from app.busi.szxl.crypto import rsa_dec, rsa_enc, rsa_sign, rsa_sign_verify
import json


def main():
    pass


# 执行单个测试用例
def run_api_case(url, para='{}', method='GET', headers=None):
    try:
        # status：接口状态码
        # msg: 处理消息
        # rsp: 接口应答
        # dealed_rsp: 预处理后的结果
        # dealed_req: 预处理参数
        ret_info = {'status': 1000, 'msg': '接口执行异常，测试失败', 'dealed_req': '', 'rsp': '', 'dealed_rsp': ''}
        # 针对接口请求前参数加密签名处理
        # 请求参数加密签名预处理
        ret_ok, req_para = http_req_para_predeal(para)
        ret_info['dealed_req'] = req_para
        if not ret_ok:
            raise RuntimeError('参数预处理出错，请检查参数:'+para)

        # 执行测试用例
        # url, para={}, method='GET', headers=None
        status, rsp = run_case.run_test_case(url, req_para, method, headers)
        ret_info['status'] = status
        ret_info['rsp'] = rsp
        if status != 200:
            ret_info['msg'] = '请求结果状态不正常'
            return ret_info

        # 请求结果解密,验证
        # print('应答结果:', rsp)
        # 判断结果是否为合法json格式
        if not util.is_json(rsp):
            ret_info['status'] = 1001
            ret_info['msg'] = '数据结果非法，非合法json格式'
        else:
            ret_ok, text = http_rsp_para_predeal(rsp)
            ret_info['dealed_rsp'] = text
            print('预处理结果:', text)
            if ret_ok:
                ret_info['msg'] = '接收应答处理成功'
            else:
                ret_info['msg'] = '数据结果非法，解密验签失败'
    except Exception as err:
        slog.show_exp('接口执行异常', para, err)
    return ret_info


# xl请求参数加密签名
def http_req_para_predeal(para):
    try:
        ret_ok = True
        deal_data = {}
        ret_para = {}

        # 入参要求是json格式
        if not util.is_json(para):
            raise RuntimeError('请求参数非法，为非合法json格式')

        # 读取请求参数并转成字典
        para_dd = json.loads(para, strict=False)
        # 选出需要处理的数据
        for k, v in para_dd.items():
            # 忽略不需要加密的直接
            if k in ['insId', 'operId']:
                ret_para[k] = v
            else:
                deal_data[k] = v

        # 加密处理的数据
        jpara = json.dumps(deal_data).encode()
        enc_para = rsa_enc(jpara)
        ret_para['encrypt'] = enc_para.decode()

        # 数据签名
        sign = rsa_sign(jpara)
        ret_para['sign'] = sign.decode()
    except Exception as err:
        slog.show_exp('参数加密签名出错', para, err)
        ret_para = {}
        ret_ok = True
    return ret_ok, ret_para


# xl返回参数解密密验证签名
def http_rsp_para_predeal(rsp_data):
    try:
        plian_txt = rsp_data
        sign_ok = False
        para_dd = json.loads(rsp_data, strict=False)

        # 如果不包含encrypt和sign直接报错
        need_key = ['encrypt', 'sign']
        if [v for v in need_key if v not in para_dd]:
            RuntimeError('应答结果失败')

        # 解密处理的数据
        enc_data = para_dd['encrypt'].encode()
        para_dd['plain_text'] = rsa_dec(enc_data).decode()
        plian_txt = json.dumps(para_dd)

        # 数据签名
        sign_data = para_dd['sign'].encode()
        sign_ok = rsa_sign_verify(para_dd['plain_text'].encode(), sign_data)
    except Exception as err:
        slog.show_exp('返回参数解密密验证签名失败', '', err)
    return sign_ok, plian_txt


if __name__ == '__main__':
    main()

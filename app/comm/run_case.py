# -*- coding: utf-8 -*-
from . import http_util
from . import util


def main():
    pass


# 运行测试用例
def run_test_case(url, para={}, method='GET', headers=None):
    try:
        # url
        http_url = url.strip()

        # 请求类型
        http_method = method.upper()

        # 请求头
        http_headers = http_util.g_headers
        if not util.is_json_null(headers):
            http_headers = headers
            print('user my headers', headers)

        # 参数请求
        http_para = para

        # print('url:', http_url)
        # print('para:', http_para)
        # print('header:', http_headers)

        # 调用执行
        if http_method == 'GET':
            http_url = http_util.make_http_get_url(http_url, http_para)
            ret_code, rsp = http_util.http_get(http_url, http_headers)
        else:
            ret_code, rsp = http_util.http_post(http_url, http_para, http_headers)
    except Exception as err:
        ret_code = -1
        rsp = '请求异常' + str(err)
    return ret_code, rsp


if __name__ == '__main__':
    main()

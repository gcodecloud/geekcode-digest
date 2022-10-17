#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
推送文章到微信公众号
"""
import time
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler

import requests

from wechat.wechat import init_cache, run


def serve(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('0.0.0.0', 80)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main():
    init_cache()
    start_time = time.time()  # 开始时间
    times = [datetime.now()]
    for x in times:
        print("start time: {}".format(x.strftime("%m/%d/%Y, %H:%M:%S")))
        string_date = x.strftime('%Y-%m-%d')
        # print(string_date)
        run(string_date)
    end_time = time.time()  # 结束时间
    print("程序耗时%f秒." % (end_time - start_time))

    serve()


if __name__ == '__main__':
    main()

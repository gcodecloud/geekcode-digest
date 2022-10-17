#!/usr/bin/env python3
# coding: utf-8
"""
created: wangtai

"""
import requests


def push_lark(string_date):
    from settings import LARK_WEB_HOOK
    requests.post(LARK_WEB_HOOK, headers={'Content-Type': 'application/json'}, json={
        "msg_type": "text",
        "content": {
            "text": f"推送公众号草稿{string_date}成功"
        }
    })

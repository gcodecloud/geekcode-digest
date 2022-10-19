#!/usr/bin/env python3
# coding: utf-8
"""
created: wangtai

"""
from pprint import pprint

from notion.notion_loader import NotionLoader


def get_article(page_id):
    page_id = '59df4a4c3b0845b9b3a3e65aea9f36f4'
    print(page_id)
    notion = NotionLoader.load()
    my_page = notion.pages.retrieve(page_id)
    pprint(my_page)

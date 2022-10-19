#!/usr/bin/env python3
# coding: utf-8
"""
created: wangtai

"""
from notion_client import Client

from settings import NOTION_TOKEN


class NotionLoader:
    """
    Notion lazy loader
    """
    __notion: Client = None

    @classmethod
    def load(cls):
        if cls.__notion is None: cls.__notion = Client(auth=NOTION_TOKEN)
        return cls.__notion

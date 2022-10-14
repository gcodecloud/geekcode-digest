#!/usr/bin/env python3
# coding: utf-8
"""
docstring
"""
from pprint import pprint

from notion_client import Client

from settings import NOTION_TOKEN, NOTION_DATABASE_ID


class NotionLoader:
    """
    Notion lazy loader
    """
    __notion: Client = None

    @classmethod
    def load(cls):
        if cls.__notion is None: cls.__notion = Client(auth=NOTION_TOKEN)
        return cls.__notion


def get_digest_raw_data():
    notion = NotionLoader.load()
    my_page = notion.databases.query(
        **{
            "database_id": NOTION_DATABASE_ID,
            "filter": {
                "property": "publish date",
                "date": {
                    "equals": "2022-10-14",
                },
            },
        }
    )
    raw_data = []
    for row in my_page['results']:
        # print(row)
        _url = row['properties']['url']['url']
        try:
            _desc = row['properties']['desc']['rich_text'][0]['text']['content']
        except IndexError:
            _desc = ""
        try:
            _title = row['properties']['Title']['title'][0]['text']['content']
        except IndexError:
            continue
        raw_data += [{
            'title': _title,
            'url': _url,
            'desc': _desc
        }]
    pprint(raw_data)

    return raw_data


if __name__ == '__main__':
    get_digest_raw_data()

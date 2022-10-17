#!/usr/bin/env python3
# coding: utf-8
"""
docstring
"""
from datetime import datetime
from pprint import pprint

from notion_client import Client

from markdown.markdown import generate_md
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


def get_digest_md_data():
    notion = NotionLoader.load()
    my_page = notion.databases.query(
        **{
            "database_id": NOTION_DATABASE_ID,
            "filter": {
                # "property": "publish date",
                # "date": {
                #     "equals": datetime.now().strftime('%Y-%m-%d'),
                # }
                "and": [
                    {
                        "property": "publish date",
                        "date": {
                            "equals": datetime.now().strftime('%Y-%m-%d'),
                        }
                    },
                    {
                        "property": "Status",
                        "select": {
                            "does_not_equal": "Done",
                        }
                    },
                ]
            },
        }
    )
    pprint(my_page)
    raw_data = []
    for row in my_page['results']:
        # pprint(row)
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
            'desc': _desc,
            'status_id': row['id']
        }]

    return raw_data


def mark_done(status_id):
    print(status_id)
    notion = NotionLoader.load()
    notion.pages.update(page_id=status_id, properties={
        "Status": {
            'select': {'name': 'Done'}
        }
    })


if __name__ == '__main__':
    md_data = get_digest_md_data()
    pprint(md_data)
    # generate_md(md_data)

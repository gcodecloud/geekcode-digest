#!/usr/bin/env python3
# coding: utf-8
"""
docstring
"""
from datetime import datetime
from pprint import pprint

from notion.notion_article import get_article
from notion.notion_loader import NotionLoader
from settings import NOTION_DATABASE_ID


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
                            "equals": "In progress",
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
        _doc = row['properties']['doc'].get('url', '')
        _doc_content = '' if _doc == '' else get_article(_doc.split('/')[-1])
        try:
            _title = row['properties']['Title']['title'][0]['text']['content']
        except IndexError:
            continue
        _type = row['properties']['Type']['select']['name']
        raw_data += [{
            'title': _title,
            'url': _url,
            'desc': _desc,
            'status_id': row['id'],
            'doc': _doc,
            'doc_content': _doc_content,
            'type': _type,
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

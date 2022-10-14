#!/usr/bin/env python3
# coding: utf-8
"""
docstring
"""
from pprint import pprint

from notion_client import Client

from settings import NOTION_TOKEN

if __name__ == '__main__':
    notion = Client(auth=NOTION_TOKEN)

    list_users_response = notion.users.list()
    pprint(list_users_response)

    my_page = notion.databases.query(
        **{
            "database_id": "e5c7b98ea3d84f8f889e4c873d5ea2de",
            "filter": {
                "property": "publish date",
                "date": {
                    "equals": "2022-10-14",
                },
            },
        }
    )
    pprint(my_page)

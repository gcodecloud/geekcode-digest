#!/usr/bin/env python3
# coding: utf-8
"""
docstring
"""
from pprint import pprint

from notion_client import Client

from settings import NOTION_TOKEN, NOTION_DATABASE_ID

if __name__ == '__main__':
    notion = Client(auth=NOTION_TOKEN)

    list_users_response = notion.users.list()
    pprint(list_users_response)

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
    pprint(my_page)

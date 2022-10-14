#!/usr/bin/env python3
# coding: utf-8
import os

WECHAT_APP_ID = os.getenv('WECHAT_APP_ID')
WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET')
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_DATABASE_ID = 'e5c7b98ea3d84f8f889e4c873d5ea2de'

# assets location base ./src/
MD_TEMPLATE_DIR = '../template/markdown/'
BLOG_POST_DIR = '../blog/_posts/'

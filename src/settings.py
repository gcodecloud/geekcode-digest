#!/usr/bin/env python3
# coding: utf-8
import os

WECHAT_APP_ID = os.getenv('WECHAT_APP_ID')
WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET')
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = 'e5c7b98ea3d84f8f889e4c873d5ea2de'

# assets location base ./src/
MD_TEMPLATE_DIR = '../template/markdown/'
BLOG_POST_DIR = '../blog/_posts/'

GIT_USERNAME = os.getenv('GIT_USERNAME')
GIT_PASSWORD = os.getenv('GIT_PASSWORD')
GIT_URL = f'https://{GIT_USERNAME}:{GIT_PASSWORD}@github.com/gcodecloud/geekcode-digest.git'
GIT_BRANCH = 'new_post'

# Lark group web hook
LARK_WEB_HOOK = os.getenv('LARK_WEB_HOOK')

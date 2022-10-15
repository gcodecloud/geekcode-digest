#!/usr/bin/env python3
# coding: utf-8
"""
created: wangtai

"""

from markdown.markdown import generate_md
from notion.notion import get_digest_md_data

if __name__ == '__main__':
    md_data = get_digest_md_data()
    generate_md(md_data)

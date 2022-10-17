#!/usr/bin/env python3
# coding: utf-8
"""
created: wangtai
trigger by github action
"""

from markdown.markdown import generate_md
from notion.notion import get_digest_md_data, mark_done

if __name__ == '__main__':
    md_data = get_digest_md_data()
    if len(md_data) > 0:
        generate_md(md_data)
        for item in md_data:
            mark_done(item['status_id'])

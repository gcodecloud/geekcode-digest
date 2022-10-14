#!/usr/bin/env python3
# coding: utf-8
"""
docstring
"""
import re

import markdown2


def get_images_from_markdown(content):
    lines = content.split('\n')
    images = []
    for line in lines:
        line = line.strip()
        if line.startswith('![') and line.endswith(')'):
            image = line.split('(')[1].split(')')[0].strip()
            images.append(image)
    return images


def fetch_attr(content, key):
    """
    从markdown文件中提取属性
    """
    lines = content.split('\n')
    for line in lines:
        if line.startswith(key):
            return line.split(':')[1].strip()
    return ""


def render_markdown(content):
    post = "".join(content.split("---\n")[2:])
    html = markdown2.markdown(post)
    # open("origi.html", "w").write(html)
    return CssContent(html).css_beautify()


def update_images_urls(content, uploaded_images):
    for image, meta in uploaded_images.items():
        orig = "({})".format(image)
        new = "({})".format(meta[1])
        # print("{} -> {}".format(orig, new))
        content = content.replace(orig, new)
    return content


class CssContent(object):
    def __init__(self, content):
        self._content = content

    def _get_tag(self, style):
        return open('../assets/{}.tmpl'.format(style), 'r').read()

    def _css_section(self):
        self._content = self._get_tag('section') + self._content + '</section>'

    def _blockquote(self):
        self._content = self._content.replace('<blockquote>', self._get_tag('blockquote'))

    def _ul(self):
        self._content = self._content.replace('<ul>', self._get_tag('ul'))

    def _li(self):
        self._content = self._content.replace('<li>', self._get_tag('li'))
        self._content = self._content.replace('</li>', '</section></li>')

    def _p(self):
        self._content = self._content.replace('<p>', self._get_tag('p'))

    def _img(self):
        raw_string = r'{}'.format(self._get_tag('img'))
        self._content = re.sub(r'<img src="(.*?)" alt="(.*?)" />', raw_string, self._content)

    def css_beautify(self):
        self._css_section()
        self._blockquote()
        self._ul()
        self._li()
        self._p()
        self._img()
        return self._content

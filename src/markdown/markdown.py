#!/usr/bin/env python3
# coding: utf-8
"""
docstring
"""
import glob
import os.path
import random
import re
import string
from datetime import datetime

import git
import markdown2

from settings import MD_TEMPLATE_DIR, BLOG_POST_DIR, GIT_URL, GIT_BRANCH


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

    @staticmethod
    def _get_tag(style):
        return open('../template/html/{}.tmpl'.format(style), 'r').read()

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


class MDGenerator(object):
    def __init__(self, notion_data):
        self._notion_data = notion_data
        self._digest_md = ''
        self._article_md = []

    def generate(self):
        digest_item = []
        for item in self._notion_data:
            if item['type'] == 'digest':
                digest_item.append(item)
            elif item['type'] == 'article':
                self._g_article(item)
        self._g_digest(digest_item)

    def _g_article(self, article):
        print(article)

    def _g_digest(self, digest_item):
        item_md = open(MD_TEMPLATE_DIR + "digest_item.md", 'r').read()
        content = ''
        subtitle = ''
        for item in digest_item:
            content += item_md.format(**item)
            subtitle += item['title'] + "; "
        skeleton = open(MD_TEMPLATE_DIR + "digest_skeleton.md", 'r').read()

        digest_md = skeleton.format(
            title='GeekCode Digest {snum}',
            date=datetime.now().strftime('%Y-%m-%d'),
            subtitle=subtitle,
            digest_item=content
        )
        self._digest_md = digest_md

    def _g_digest1(self, digest_item):
        item_md = open(MD_TEMPLATE_DIR + "digest_item.md", 'r').read()
        content = ''
        subtitle = ''
        for item in digest_item:
            content += item_md.format(**item)
            subtitle += item['title'] + "; "
        skeleton = open(MD_TEMPLATE_DIR + "digest_skeleton.md", 'r').read()

        git_wrapper = GitWrapper()
        git_wrapper.init_repo()
        post_path = git_wrapper.work_dir + BLOG_POST_DIR.replace('../', '')
        snum = get_digest_snum(post_path)
        digest_md = skeleton.format(
            title=f'GeekCode Digest {snum}',
            date=datetime.now().strftime('%Y-%m-%d'),
            subtitle=subtitle,
            digest_item=content
        )
        digest_file_name = f"{post_path}digest{snum}.md"
        print(digest_file_name)
        open(digest_file_name, 'w').write(digest_md)
        git_wrapper.commit(digest_file_name)


def get_digest_snum(post_path):
    md_list = glob.glob(f'{post_path}/*.md')
    print(md_list)
    z = list(map(lambda x: re.findall(r'\d\d\d', x), md_list))
    z = [int(i[-1]) for i in z if len(i) > 0]
    max_snum = str(max(z) + 1)

    return max_snum.rjust(3, '0')


class GitWrapper:
    def __init__(self):
        self._repo = None
        self.work_dir = ""
        self._change_file = ""

    def init_repo(self):
        print("init repo")
        self.work_dir = '/tmp/geekcode_digest_repo_{}/'.format(''.join(random.choices(string.ascii_letters, k=8)))
        self._repo = git.Repo.clone_from(GIT_URL, self.work_dir, branch=GIT_BRANCH)

    def commit(self, file_name):
        print("git commit")
        self._repo.index.add(file_name)
        self._repo.index.commit(f"add {os.path.basename(file_name)}")
        origin = self._repo.remote(name='origin')
        origin.push()


if __name__ == '__main__':
    print(get_digest_snum(BLOG_POST_DIR))

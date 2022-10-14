#!/usr/bin/env python3
# coding: utf-8
"""
docstring
"""
import hashlib
import json
import os
import pickle
import urllib
import urllib.request
from datetime import datetime
from pathlib import Path

import requests
from werobot import WeRoBot

from markdown.tool import fetch_attr, get_images_from_markdown, update_images_urls, render_markdown
from settings import WECHAT_APP_ID, WECHAT_APP_SECRET

CACHE = {}

CACHE_STORE = "/tmp/cache.bin"

AUTHOR = 'GeekCode Genius'

BLOG_POST_PATH = "../blog/_posts"


def dump_cache():
    fp = open(CACHE_STORE, "wb")
    pickle.dump(CACHE, fp)


def init_cache():
    global CACHE
    if os.path.exists(CACHE_STORE):
        fp = open(CACHE_STORE, "rb")
        CACHE = pickle.load(fp)
        # print(CACHE)
        return
    dump_cache()


class NewClient:
    __access_token = ''
    __left_time = 0
    __client: WeRoBot.client

    @classmethod
    def __token(cls):
        robot = WeRoBot()
        robot.config["APP_ID"] = WECHAT_APP_ID
        robot.config["APP_SECRET"] = WECHAT_APP_SECRET
        cls.__client = robot.client
        token = cls.__client.grant_token()
        return token

    @classmethod
    def __real_get_access_token(cls):
        token = cls.__token()
        cls.__access_token = token['access_token']
        cls.__left_time = token['expires_in']

    @classmethod
    def get_access_token(cls):
        if cls.__left_time < 10:
            cls.__real_get_access_token()
        return cls.__access_token

    @classmethod
    def client(cls) -> WeRoBot.client:
        if cls.__left_time < 10:
            cls.__real_get_access_token()
        return cls.__client


def cache_get(key):
    if key in CACHE:
        return CACHE[key]
    return None


def file_digest(file_path):
    """
    计算文件的md5值
    """
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        md5.update(f.read())
    return md5.hexdigest()


def cache_update(file_path):
    digest = file_digest(file_path)
    CACHE[digest] = "{}:{}".format(file_path, datetime.now())
    dump_cache()


def file_processed(file_path):
    digest = file_digest(file_path)
    return cache_get(digest) is not None


def upload_image_from_path(image_path):
    image_digest = file_digest(image_path)
    res = cache_get(image_digest)
    if res is not None:
        return res[0], res[1]
    _client = NewClient.client()
    # media_json = _client.upload_permanent_media("image", open(image_path, "rb"))  ##永久素材
    media_json = requests.post("https://api.weixin.qq.com/cgi-bin/material/add_material",
                               params={
                                   "access_token": _client.get_access_token(),
                                   "type": "image"
                               },
                               files={"media": open(image_path, "rb")}).json()
    media_id = media_json['media_id']
    media_url = media_json['url']
    CACHE[image_digest] = [media_id, media_url]
    dump_cache()
    print("file: {} => media_id: {}".format(image_path, media_id))
    return media_id, media_url


def upload_image(img_url):
    """
    * 上传临时素菜
    * 1、临时素材media_id是可复用的。
    * 2、媒体文件在微信后台保存时间为3天，即3天后media_id失效。
    * 3、上传临时素材的格式、大小限制与公众平台官网一致。
    """
    resource = urllib.request.urlopen(img_url)
    name = img_url.split("/")[-1]
    f_name = "/tmp/{}".format(name)
    if "." not in f_name:
        f_name = f_name + ".png"
    with open(f_name, 'wb') as f:
        f.write(resource.read())
    return upload_image_from_path(f_name)


def upload_media_news(post_path):
    """
    上传到微信公众号素材
    """
    content = open(post_path, 'r').read()
    TITLE = fetch_attr(content, 'title').strip('"').strip('\'')
    gen_cover = fetch_attr(content, 'gen_cover').strip('"')
    images = get_images_from_markdown(content)
    if len(gen_cover) > 0:
        images = [gen_cover] + images
    elif len(images) == 0:
        images = ['https://source.unsplash.com/random/600x400'] + images
    print(images)
    uploaded_images = {}
    for image in images:
        if image.startswith("http"):
            media_id, media_url = upload_image(image)
        else:
            media_id, media_url = upload_image_from_path(BLOG_POST_PATH + "/" + image)
        uploaded_images[image] = [media_id, media_url]

    content = update_images_urls(content, uploaded_images)

    THUMB_MEDIA_ID = (len(images) > 0 and uploaded_images[images[0]][0]) or ''
    RESULT = render_markdown(content)

    digest = fetch_attr(content, 'subtitle').strip().strip('"').strip('\'')
    CONTENT_SOURCE_URL = 'https://github.com/gcodecloud/geekcode-digest/blob/main/{}'.format(post_path)

    articles = {
        'articles':
            [
                {
                    "title": TITLE,
                    "thumb_media_id": THUMB_MEDIA_ID,
                    "author": AUTHOR,
                    "digest": digest,
                    "show_cover_pic": 1,
                    "content": RESULT,
                    "content_source_url": CONTENT_SOURCE_URL
                }
                # 若新增的是多图文素材，则此处应有几段articles结构，最多8段
            ]
    }

    # open('./result.html', 'w').write(RESULT)

    resp = upload_draft(articles)
    cache_update(post_path)
    return resp


def upload_draft(articles):
    _client = NewClient()
    token = _client.get_access_token()
    headers = {'Content-type': 'text/plain; charset=utf-8'}
    datas = json.dumps(articles, ensure_ascii=False).encode('utf-8')

    post_url = "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=%s" % token
    r = requests.post(post_url, data=datas, headers=headers)
    resp = json.loads(r.text)
    # media_id = resp['media_id']
    return resp


def run(string_date):
    path_list = Path(BLOG_POST_PATH).glob('**/*.md')
    for path in path_list:
        path_str = str(path)
        if file_processed(path_str):
            print("{} has been processed".format(path_str))
            continue
        content = open(path_str, 'r').read()
        date = fetch_attr(content, 'date').strip()
        if string_date in date:
            news_json = upload_media_news(path_str)
            print(news_json)
            print('successful')

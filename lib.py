import os
import re
import jsonlines
from requests import Session
from re import compile, sub
from json import loads
import configparser

config = configparser.ConfigParser()
config.read('Jobs/CV/小红书图片/cfg.ini', encoding='utf8')
root_path = config['default']['root_path']
root = os.path.join(root_path, "xiaohongshu")
if not os.path.exists(root):
    os.makedirs(root, exist_ok=True)
staic_path = os.path.join(root_path, "Statistics")
if not os.path.exists(staic_path):
    os.makedirs(staic_path, exist_ok=True)

EXPLORE_URL = "https://www.xiaohongshu.com/explore"
PREFETCH_URL = "https://www.xiaohongshu.com/explore/prefetch"

IMAGE_PATTREN = compile(r'"infoList":\[\{.*?\}\]')
EXPLORE_PATTREN = compile(
    r'"currentTime":\d{13},"note":(.*?)}},"serverRequestInfo"')
TOKEN_PATTREN = compile(
    r"http://sns-webpic-qc.xhscdn.com/\d+/\w+/(\w+)!")
session = Session()
session.cookies.update({
    "webId": config['default']['webId'],
    "web_session": config['default']['web_session'],
})


def get_channel():
    """
    小红书主页链接生成器
    :return: 参数字典
    """
    for channel in [
        '.recommend',
        '.fashion_v3',
        '.food_v3',
        '.cosmetics_v3',
        '.movie_and_tv_v3',
        '.career_v3',
        '.love_v3',
        '.household_product_v3',
        '.gaming_v3',
        '.travel_v3',
        '.fitness_v3'
    ]:
        yield {"channel_id": f"homefeed{channel}"}


def get_source_image(explore_params):
    """
    获取ID
    :param explore_params: 小红书主页链接
    :return: None
    """
    response = session.get(EXPLORE_URL, params=explore_params)
    prefetch_params = {"prefetch_id": response.cookies.get_dict()['cacheId']}
    response = session.get(PREFETCH_URL, params=prefetch_params)
    if "您当前系统版本过低，请升级后再试" in response.text:
        raise Exception("Cookie失效")
    items = response.json()["data"]["items"]
    if not items:
        return None
    for item in items:
        if item['note_card']['type'] == 'normal':
            yield item['id']


def explore(source_id):
    """
    获取作品信息
    :param source_id: 作品ID
    :return: 作品信息字典
    """
    source_link = f"{EXPLORE_URL}/{source_id}"
    # print("链接:", source_link)
    html = session.get(source_link).text
    data = EXPLORE_PATTREN.findall(html)
    data = {} if len(data) != 1 else loads(data[0])
    return {
        "作品ID": data.get("noteId", ""),
        "作品标题": data.get("title", ""),
        "作品描述": sub(r'\[话题\]', '', data.get("desc", "")),
        "作品链接": get_image_link(html)
    }


def get_image_link(html):
    """
    获取图片链接
    :param html: 带有图片链接的HTML
    :return: 图片链接列表
    """
    urls = []
    for i in [loads(f"{{{i}}}") for i in IMAGE_PATTREN.findall(html)]:
        for j in i.get("infoList", []):
            if j.get("imageScene", "").startswith("CRD_WM_"):
                # urls.append(j.get("url", ""))
                temp_url = j.get("url", "")
                url = f"https://ci.xiaohongshu.com/{token}?imageView2/2/w/format/png" if (
                    token := TOKEN_PATTREN.findall(temp_url)) else temp_url
                urls.append(url)
                break
    return [bytes(i, "utf-8").decode("unicode_escape") for i in urls if i]


def download_source_link(source_link):
    """
    下载资源
    :param source_link: 资源链接
    :return: None
    """
    save_name = source_link.split("/")[-1]
    # print("图片:", save_name, end=" ")
    save_path = os.path.join(root, "image")
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    with session.get(source_link, stream=True) as response:
        with open(f'{save_path}/{save_name}.jpg', "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
    # print("下载完成")
    return save_path


def record_source_link(source_dict, save_path):
    """
    记录信息
    :return: None
    """
    with jsonlines.open(f"{root}/image_sessage.jsonl", "a") as writer:
        writer.write({
            'image_id': save_path,
            'image_title': source_dict['作品标题'],
            'image_content': source_dict['作品描述']
        })


def perceive():
    """
    :return: 最新序号，最近大小
    """
    last_num = 0
    for _, dirs, files in os.walk(root):
        for file_ in files:
            if re.search(r'^xhs_\d+', file_):
                num = int(file_.split('_')[1])
                if num > last_num:
                    last_num = num
        for dir_ in dirs:
            if re.search(r'^xhs_\d+', dir_):
                num = int(dir_.split('_')[1])
                if num > last_num:
                    last_num = num
    return last_num + 1

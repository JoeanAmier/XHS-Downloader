from asyncio import run

from httpx import post
from rich import print

from source import XHS


async def example():
    """通过代码设置参数，适合二次开发"""
    # 示例链接
    demo_link = "https://www.xiaohongshu.com/explore/XXX?xsec_token=XXX"

    # 实例对象
    work_path = "D:\\"  # 作品数据/文件保存根路径，默认值：项目根路径
    folder_name = "Download"  # 作品文件储存文件夹名称（自动创建），默认值：Download
    name_format = "作品标题 作品描述"
    user_agent = ""  # User-Agent
    cookie = ""  # 小红书网页版 Cookie，无需登录，可选参数，登录状态对数据采集有影响
    proxy = None  # 网络代理
    timeout = 5  # 请求数据超时限制，单位：秒，默认值：10
    chunk = 1024 * 1024 * 10  # 下载文件时，每次从服务器获取的数据块大小，单位：字节
    max_retry = 2  # 请求数据失败时，重试的最大次数，单位：秒，默认值：5
    record_data = False  # 是否保存作品数据至文件
    image_format = "WEBP"  # 图文作品文件下载格式，支持：AUTO、PNG、WEBP、JPEG、HEIC
    folder_mode = False  # 是否将每个作品的文件储存至单独的文件夹
    image_download = True  # 图文作品文件下载开关
    video_download = True  # 视频作品文件下载开关
    live_download = False  # 图文动图文件下载开关
    download_record = True  # 是否记录下载成功的作品 ID
    language = "zh_CN"  # 设置程序提示语言
    author_archive = True  # 是否将每个作者的作品存至单独的文件夹
    write_mtime = True  # 是否将作品文件的 修改时间 修改为作品的发布时间
    read_cookie = None  # 读取浏览器 Cookie，支持设置浏览器名称（字符串）或者浏览器序号（整数），设置为 None 代表不读取

    # async with XHS() as xhs:
    #     pass  # 使用默认参数

    async with XHS(
        work_path=work_path,
        folder_name=folder_name,
        name_format=name_format,
        user_agent=user_agent,
        cookie=cookie,
        proxy=proxy,
        timeout=timeout,
        chunk=chunk,
        max_retry=max_retry,
        record_data=record_data,
        image_format=image_format,
        folder_mode=folder_mode,
        image_download=image_download,
        video_download=video_download,
        live_download=live_download,
        download_record=download_record,
        language=language,
        read_cookie=read_cookie,
        author_archive=author_archive,
        write_mtime=write_mtime,
    ) as xhs:  # 使用自定义参数
        download = True  # 是否下载作品文件，默认值：False
        # 返回作品详细信息，包括下载地址
        # 获取数据失败时返回空字典
        print(
            await xhs.extract(
                demo_link,
                download,
                index=[
                    1,
                    2,
                    5,
                ],
            )
        )


async def example_api():
    """通过 API 设置参数，适合二次开发"""
    server = "http://127.0.0.1:5556/xhs/"
    data = {
        "url": "",  # 必需参数
        "download": True,
        "index": [
            3,
            6,
            9,
        ],
        "proxy": "http://127.0.0.1:10808",
    }
    response = post(server, json=data, timeout=10)
    print(response.json())


async def test():
    url = ""
    async with XHS(
        download_record=False,
        # image_format="PNG",
        # image_format="WEBP",
        # image_format="JPEG",
        # image_format="HEIC",
        # image_format="AVIF",
        # image_format="AUTO",
    ) as xhs:
        print(
            await xhs.extract(
                url,
                # download=True,
            )
        )


if __name__ == "__main__":
    # run(example())
    # run(example_api())
    run(test())

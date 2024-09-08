from asyncio import run
from asyncio.exceptions import CancelledError
from contextlib import suppress
from sys import argv

from source import Settings
from source import XHS
from source import XHSDownloader
from source import cli


async def example():
    """通过代码设置参数，适合二次开发"""
    # 示例链接
    error_link = "https://github.com/JoeanAmier/XHS_Downloader"
    demo_link = "https://www.xiaohongshu.com/explore/xxxxxxxxxx"
    multiple_links = f"{demo_link} {demo_link} {demo_link}"
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
    image_format = "WEBP"  # 图文作品文件下载格式，支持：PNG、WEBP
    folder_mode = False  # 是否将每个作品的文件储存至单独的文件夹
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
    ) as xhs:  # 使用自定义参数
        download = True  # 是否下载作品文件，默认值：False
        # 返回作品详细信息，包括下载地址
        # 获取数据失败时返回空字典
        print(await xhs.extract(error_link, download, ))
        print(await xhs.extract(demo_link, download, index=[1, 2]))
        # 支持传入多个作品链接
        print(await xhs.extract(multiple_links, download, ))


async def app():
    async with XHSDownloader() as xhs:
        await xhs.run_async()


async def server(host="0.0.0.0", port=8000, log_level="info", ):
    async with XHS(**Settings().run()) as xhs:
        await xhs.run_server(host, port, log_level, )


if __name__ == '__main__':
    with suppress(
            KeyboardInterrupt,
            CancelledError,
    ):
        if len(argv) == 1:
            run(app())
        elif argv[1] == "server":
            run(server())
        else:
            cli()

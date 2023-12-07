from asyncio import run

from source import XHS
from source import XHSDownloader


async def example():
    """通过代码设置参数，适合二次开发"""
    # 测试链接
    error_demo = "https://github.com/JoeanAmier/XHS_Downloader"
    image_demo = "https://www.xiaohongshu.com/explore/63b275a30000000019020185"
    video_demo = "https://www.xiaohongshu.com/explore/64edb460000000001f03cadc"
    multiple_demo = f"{image_demo} {video_demo}"
    # 实例对象
    path = ""  # 作品数据/文件保存根路径，默认值：项目根路径
    folder_name = "Download"  # 作品文件储存文件夹名称（自动创建），默认值：Download
    user_agent = ""  # 请求头 User-Agent
    proxy = ""  # 网络代理
    timeout = 5  # 网络请求超时限制，单位：秒，默认值：10
    chunk = 1024 * 1024  # 下载文件时，每次从服务器获取的数据块大小，单位：字节
    max_retry = 2  # 请求数据失败时，重试的最大次数，单位：秒，默认值：5
    # async with XHS() as xhs:
    #     pass  # 使用默认参数
    async with XHS(path=path,
                   folder_name=folder_name,
                   user_agent=user_agent,
                   proxy=proxy,
                   timeout=timeout,
                   chunk=chunk,
                   max_retry=max_retry, ) as xhs:  # 使用自定义参数
        download = True  # 是否下载作品文件，默认值：False
        # 返回作品详细信息，包括下载地址
        print(await xhs.extract(error_demo, download))  # 获取数据失败时返回空字典
        print(await xhs.extract(image_demo, download))
        print(await xhs.extract(video_demo, download))
        print(await xhs.extract(multiple_demo, download))  # 支持传入多个作品链接


async def main():
    async with XHSDownloader() as xhs:
        await xhs.run_async()


if __name__ == '__main__':
    # run(example())
    run(main())

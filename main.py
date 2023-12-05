from asyncio import run

from source import XHS


async def example():
    """通过代码设置参数，适合二次开发"""
    # 测试链接
    error_demo = "https://github.com/JoeanAmier/XHS_Downloader"
    image_demo = "https://www.xiaohongshu.com/explore/63b275a30000000019020185"
    video_demo = "https://www.xiaohongshu.com/explore/64edb460000000001f03cadc"
    multiple_demo = f"{image_demo} {video_demo}"
    # 实例对象
    path = "D:\\"  # 作品下载储存根路径，默认值：当前路径
    folder = "Download"  # 作品下载文件夹名称（自动创建），默认值：Download
    proxies = None  # 网络代理
    timeout = 5  # 网络请求超时限制，默认值：10
    chunk = 1024 * 1024  # 下载文件时，每次从服务器获取的数据块大小，单位字节
    async with XHS() as xhs:
        pass  # 使用默认参数
    async with XHS(path=path,
                   folder=folder,
                   proxy=proxies,
                   timeout=timeout,
                   chunk=chunk) as xhs:  # 使用自定义参数
        download = False  # 是否下载作品文件，默认值：False
        # 返回作品详细信息，包括下载地址
        print(await xhs.extract(error_demo))  # 获取数据失败时返回空字典
        print(await xhs.extract(image_demo, download=download))
        print(await xhs.extract(video_demo, download=download))
        print(await xhs.extract(multiple_demo, download=download))


if __name__ == '__main__':
    run(example())
    # with XHSDownloader() as xhs:
    #     xhs.run()

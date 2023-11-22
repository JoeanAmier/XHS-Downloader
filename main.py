from source import XHS
from source import XHSDownloader


def example():
    """通过代码设置参数，适合二次开发"""
    # 测试链接
    error_demo = "https://github.com/JoeanAmier/XHS_Downloader"
    image_demo = "https://www.xiaohongshu.com/explore/63b275a30000000019020185"
    video_demo = "https://www.xiaohongshu.com/explore/64edb460000000001f03cadc"
    # 实例对象
    path = ""  # 作品下载储存根路径，默认值：当前路径
    folder = "Download"  # 作品下载文件夹名称（自动创建），默认值：Download
    cookie = ""  # 小红书网页版 Cookie
    proxies = None  # 网络代理
    timeout = 5  # 网络请求超时限制，默认值：10
    chunk = 1024 * 1024  # 下载文件时，每次从服务器获取的数据块大小，单位字节
    xhs = XHS(
        path=path,
        folder=folder,
        cookie=cookie,
        proxies=proxies,
        timeout=timeout,
        chunk=chunk, )  # 使用自定义参数
    # xhs = XHS()  # 使用默认参数
    download = True  # 是否下载作品文件
    # 返回作品详细信息，包括下载地址
    print(xhs.extract(error_demo))  # 获取数据失败时返回空字典
    print(xhs.extract(image_demo, download=download))
    print(xhs.extract(video_demo, download=download))


if __name__ == '__main__':
    # example()
    XHSDownloader().run()

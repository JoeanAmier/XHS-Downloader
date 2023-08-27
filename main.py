from source import XHS


def example():
    """使用示例"""
    # 测试链接
    image_demo = "https://www.xiaohongshu.com/explore/64d1b406000000000103ee8d"
    video_demo = "https://www.xiaohongshu.com/explore/64c05652000000000c0378e7"
    # 实例对象
    path = "./"  # 作品下载储存根路径，默认值：当前路径
    folder = "Download"  # 作品下载文件夹名称（自动创建），默认值：Download
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
    }  # 请求头
    proxies = None  # 代理
    timeout = 10  # 网络请求超时限制，默认值：10
    cookie = ""  # 小红书网页 cookie，无需登录，获取数据失败时可以尝试手动设置
    xhs = XHS(
        path=path,
        folder=folder,
        headers=headers,
        proxies=proxies,
        timeout=timeout,
        cookie=cookie)  # 使用自定义参数
    # xhs = XHS()  # 使用默认参数
    # 无需区分图文和视频作品
    # 返回作品详细数据，包括下载地址
    download = True  # 启用自动下载作品文件
    print(xhs.extract(image_demo, download=download))
    print(xhs.extract(video_demo, download=download))


if __name__ == '__main__':
    example()

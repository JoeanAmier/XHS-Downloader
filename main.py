from source import XHS


def example():
    """使用示例"""
    image_demo = "https://www.xiaohongshu.com/explore/64d1b406000000000103ee8d"
    video_demo = "https://www.xiaohongshu.com/explore/64c05652000000000c0378e7"
    xhs = XHS()
    print(xhs.get_image(image_demo))
    print(xhs.get_video(video_demo))


if __name__ == '__main__':
    example()

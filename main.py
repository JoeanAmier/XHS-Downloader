from source import XHS


def example():
    test_cookie = "abRequestId=25c57ab7-8cbf-5383-b020-08852c1704e1; webBuild=3.4.1; xsecappid=xhs-pc-web; a1=18a033d274338lwsfacj9x5bpf4fznhhc8xrakemj50000250510; webId=93c0636350d85103d93bca88da2959cd; websectiga=2a3d3ea002e7d92b5c9743590ebd24010cf3710ff3af8029153751e41a6af4a3; sec_poison_id=ae1f0190-4d0c-45f5-a75f-68c2d87c5573; web_session=030037a3ed570060b3a43845a6234a2f100ef4; gid=yY08qqfYy0SSyY08qqfJWYTd4qqY1EMi0SVjC6VC2DUi4F28iuIxx0888J282y880JfWY0Di; cache_feeds=[]"
    demo = "https://www.xiaohongshu.com/explore/64a3a5170000000031008914"
    xhs = XHS()
    print(xhs.get_image(demo, cookie=test_cookie))


if __name__ == '__main__':
    example()

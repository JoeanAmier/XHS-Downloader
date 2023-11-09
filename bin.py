from lib import *
import shutil
import time
from multiprocessing import Manager, Pipe
from concurrent.futures import ProcessPoolExecutor


def core_put(queue):
    for channel_id in get_channel():
        for source_id in get_source_image(channel_id):
            one_dict = explore(source_id)
            queue.put(one_dict)
            # print(f'当前队列: {queue.qsize()}', end='\r')


def core_get(queue, conn_send):
    while True:
        try:
            one_dict = queue.get(timeout=10, block=True)
            for source_link in one_dict['作品链接']:
                save_path = download_source_link(source_link)
                record_source_link(one_dict, save_path)
                conn_send.send(True)
                print(f'当前队列: {queue.qsize()}', end='\r')
        except TimeoutError:
            conn_send.send('end')
            break


def core_change(conn_recv):
    count = 0
    while True:
        f = conn_recv.recv()
        if f:
            count += 1
            print('当前完成:', count)
        if count >= 100:
            new_path = f'xhs_{perceive()}_{time.strftime("%Y%m%d",time.localtime())}'
            shutil.move(root, os.path.join(root_path, new_path))
            print('移动完成')
            count = 0
        if f == 'end':
            break


def main():
    queue = Manager().Queue()
    conn_send, conn_recv = Pipe()
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.submit(core_change, conn_recv)
        executor.submit(core_put, queue)
        for _ in range(3):
            executor.submit(core_get, queue, conn_send)
        exit()


def core():
    for channel_id in get_channel():
        for source_id in get_source_image(channel_id):
            one_dict = explore(source_id)
            for source_link in one_dict['作品链接']:
                # 下载资源
                save_path = download_source_link(source_link)
                # 记录信息
                record_source_link(one_dict, save_path)
                print("下载完成")
        break


if __name__ == '__main__':
    main()
    # core()

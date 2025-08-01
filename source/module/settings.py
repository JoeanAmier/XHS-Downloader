from json import dump, load
from pathlib import Path
from platform import system

from .static import ROOT, USERAGENT

__all__ = ["Settings"]


class Settings:
    # 默认配置参数
    default = {
        "mapping_data": {},  # 账号备注映射数据
        "work_path": "",  # 工作目录路径
        "folder_name": "Download",  # 下载文件夹名称
        "name_format": "发布时间 作者昵称 作品标题",  # 文件命名格式
        "user_agent": USERAGENT,  # 请求头
        "cookie": "",  # Cookie
        "proxy": None,  # 代理设置
        "timeout": 10,  # 超时时间(秒)
        "chunk": 1024 * 1024 * 2,  # 下载块大小(字节)
        "max_retry": 5,  # 最大重试次数
        "record_data": False,  # 是否记录作品数据
        "image_format": "PNG",  # 图文作品格式
        "image_download": True,  # 是否下载图文
        "video_download": True,  # 是否下载视频
        "live_download": False,  # 是否下载动图
        "folder_mode": False,  # 文件夹归档模式
        "download_record": True,  # 是否记录下载历史
        "author_archive": False,  # 是否按作者归档
        "write_mtime": False,  # 是否写入修改时间
        "language": "zh_CN",  # 语言设置
    }
    # 根据操作系统设置编码格式
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

    def __init__(self, root: Path = ROOT):
        # 设置文件路径
        self.file = root.joinpath("./settings.json")

    def run(self):
        # 如果文件存在则读取,否则创建新文件
        return self.read() if self.file.is_file() else self.create()

    def read(self) -> dict:
        # 读取设置文件
        with self.file.open("r", encoding=self.encode) as f:
            return self.compatible(load(f))

    def create(self) -> dict:
        # 创建新的设置文件
        with self.file.open("w", encoding=self.encode) as f:
            dump(self.default, f, indent=4, ensure_ascii=False)
            return self.default

    def update(self, data: dict):
        # 更新设置文件
        with self.file.open("w", encoding=self.encode) as f:
            dump(data, f, indent=4, ensure_ascii=False)

    def compatible(
        self,
        data: dict,
    ) -> dict:
        # 兼容性检查: 确保所有默认配置都存在
        update = False
        for i, j in self.default.items():
            if i not in data:
                data[i] = j
                update = True
        if update:
            self.update(data)
        return data

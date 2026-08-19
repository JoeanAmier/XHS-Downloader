"""PyWebView 静态界面与下载器核心之间的运行时桥接层。"""

import asyncio
import sys
from asyncio import CancelledError
from collections import deque
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from re import search
from subprocess import DEVNULL, Popen
from threading import Event, Thread
from typing import Any
from urllib.parse import urlsplit
from uuid import uuid4
from webbrowser import open as open_browser

import webview
from pyperclip import copy, paste

from ..application import XHS
from ..module import (
    LICENCE,
    RELEASES,
    REPOSITORY,
    VERSION_BETA,
    VERSION_MAJOR,
    VERSION_MINOR,
    VOLUME,
    Settings,
    compare_versions,
)
from ..translation import _
from .ui_strings import (
    NAME_FORMAT_FIELDS,
    get_ui_translations,
    normalize_name_format_field,
)

# 下载记录固定按每页 100 条返回，前端仅负责渲染当前页。
HISTORY_PAGE_SIZE = 100
ABOUT_URLS = {
    "repository": REPOSITORY,
    "discord": "https://discord.com/invite/ZYtmgKud9Y",
    "tk": "https://github.com/JoeanAmier/TikTokDownloader",
    "ks": "https://github.com/JoeanAmier/KS-Downloader",
}


def now_text() -> str:
    """返回用于界面显示的本地时间。"""

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def task_display_id(url: str) -> str:
    parts = urlsplit(url)
    return parts.path.rstrip("/").rsplit("/", 1)[-1]


def build_update_result(release_url: str) -> dict[str, Any]:
    """根据 GitHub 重定向后的发布页 URL 构造界面可直接展示的更新结果。"""

    tag = release_url.rstrip("/").split("/")[-1]
    match = search(r"(?<!\d)(\d+)\.(\d+)(?!\d)", tag)
    if not match:
        return {
            "status": "error",
            "message": _("无法解析版本号：{0}").format(tag),
        }

    target = tuple(map(int, match.groups()))
    current = (VERSION_MAJOR, VERSION_MINOR)
    latest_version = f"{target[0]}.{target[1]}"
    current_version = f"{VERSION_MAJOR}.{VERSION_MINOR}"
    if VERSION_BETA:
        current_version += " Beta"

    match compare_versions(
        f"{current[0]}.{current[1]}",
        latest_version,
        VERSION_BETA,
    ):
        case 4:
            kind = "update_available"
            title = _("检测到新版本：{0}.{1}").format(
                target[0],
                target[1],
            )
            message = _("当前版本为 {0}").format(current_version)
        case 3:
            kind = "stable_available"
            title = _("当前版本为开发版, 可更新至正式版")
            message = _("{0} 正式版已发布，当前版本为 {1}").format(
                latest_version, current_version
            )
        case 1:
            kind = "up_to_date"
            title = _("当前已是最新正式版")
            message = _("当前版本为 {0}").format(current_version)
        case 2:
            kind = "development_current"
            title = _("当前已是最新开发版")
            message = _("当前版本为 {0}，最新正式版为 {1}").format(
                current_version, latest_version
            )
        case _:
            return {
                "status": "error",
                "message": _("版本比较结果无效"),
            }

    return {
        "status": "ok",
        "kind": kind,
        "title": title,
        "message": message,
    }


@dataclass
class TaskState:
    """界面任务队列中的单个任务快照。"""

    task_id: str
    url: str
    source: str = "manual"
    state: str = "pending"
    script_data: dict[str, Any] | None = None
    index: list | tuple | None = None
    display_text: str | None = None

    def as_dict(self) -> dict[str, Any]:
        """转换为可通过 PyWebView 序列化给 JavaScript 的普通字典。"""

        return {
            "task_id": self.task_id,
            "url": self.url,
            "display_text": self.display_text or self.url,
            "source": self.source,
            "state": self.state,
        }


class GuiLogSink:
    """把核心下载器的 RichLog 写入接口适配到 GUI 日志缓冲区。"""

    def __init__(self, backend: "GuiBackend"):
        self.backend = backend

    def write(self, value: Any, scroll_end: bool = True) -> None:
        # 核心日志包含 Rich 样式；此处仅保留颜色对应的等级，交由前端完成着色。
        text = getattr(value, "plain", str(value))
        style = str(getattr(value, "style", ""))
        if "red" in style:
            level = "error"
        elif "yellow" in style:
            level = "warning"
        elif "green" in style:
            level = "success"
        else:
            level = "info"
        self.backend.add_log(text, level)


class GuiBackend:
    """维护一个下载器实例和一个长期运行的 asyncio 事件循环。"""

    def __init__(self) -> None:
        self.loop: asyncio.AbstractEventLoop | None = None
        self.thread: Thread | None = None
        self.ready = Event()
        self.start_error: BaseException | None = None
        self.closed = False
        self.settings_manager = Settings(VOLUME)
        self.settings: dict[str, Any] = {}
        self.xhs: XHS | None = None
        self.task_queue: asyncio.Queue[str] | None = None
        self.worker: asyncio.Task | None = None
        self.monitor_task: asyncio.Task | None = None
        self.tasks: dict[str, TaskState] = {}
        self.files: dict[str, dict[str, Any]] = {}
        self.history_revision = 0
        self.logs: deque[dict[str, str]] = deque(maxlen=300)
        self.monitor: dict[str, Any] = {
            "active": False,
            "state": "stopped",
            "started_at": None,
            "created": 0,
        }

    def start(self, wait: bool = True) -> None:
        # PyWebView 的 JavaScript 调用来自主线程，下载器事件循环运行于后台线程，
        # 以避免网络请求阻塞窗口，并通过 call() 实现跨线程协程调度。
        self.thread = Thread(
            target=self._thread_main,
            name="xhs-gui-backend",
            daemon=True,
        )
        self.thread.start()
        if not wait:
            return
        self.wait_until_ready()

    def wait_until_ready(self, timeout: float | None = None) -> None:
        """等待 GUI 后端线程完成初始化，以便处理接口调用。"""

        if not self.ready.wait(timeout):
            raise RuntimeError("GUI 后端初始化超时")
        if self.start_error:
            raise RuntimeError("GUI 后端初始化失败") from self.start_error

    def _thread_main(self) -> None:
        """创建后台事件循环，并在初始化完成后持续处理异步任务。"""

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self._initialize())
        except BaseException as error:
            self.start_error = error
            self.ready.set()
            self.loop.close()
            return
        self.ready.set()
        self.loop.run_forever()
        self.loop.close()

    async def _initialize(self) -> None:
        """读取配置；用户已同意免责声明后才创建下载器运行时。"""

        self.settings = self.settings_manager.run()
        if not self.settings["disclaimer_accepted"]:
            return
        await self._start_runtime()

    async def _start_runtime(self) -> None:
        """创建下载器和任务 worker；启动时不自动创建下载任务。"""

        if self.xhs:
            return
        self.task_queue = asyncio.Queue()
        await self._create_xhs()
        self.worker = asyncio.create_task(self._worker_loop())

    async def _create_xhs(self) -> None:
        """按当前配置创建 XHS 实例，并把核心日志导向 GUI。"""

        self.xhs = XHS(**self.settings, _print=False)
        self.xhs.print.func = GuiLogSink(self)
        self.xhs.script_task_handler = self.create_script_task
        await self.xhs.__aenter__()

    async def _close_xhs(self) -> None:
        """释放下载器的 HTTP 客户端和其他异步资源。"""

        if self.xhs:
            await self.xhs.__aexit__(None, None, None)
            self.xhs = None

    def stop(self) -> None:
        """从主线程请求后台协程停止，然后关闭事件循环线程。"""

        if not self.loop or not self.thread:
            return
        future = asyncio.run_coroutine_threadsafe(self._shutdown(), self.loop)
        with suppress(Exception):
            future.result(timeout=15)
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join(timeout=15)
        self.closed = True

    async def _shutdown(self) -> None:
        """停止剪贴板监听和任务 worker，再关闭下载器。"""

        if self.monitor_task:
            self.monitor_task.cancel()
            with suppress(CancelledError):
                await self.monitor_task
            self.monitor_task = None
        if self.worker:
            self.worker.cancel()
            with suppress(CancelledError):
                await self.worker
            self.worker = None
        await self._close_xhs()

    def call(self, coroutine):
        """把协程提交到后台循环，并同步等待 PyWebView API 的返回值。"""

        try:
            if self.closed:
                raise RuntimeError("GUI 后端未运行")
            self.wait_until_ready(timeout=30)
            if not self.loop:
                raise RuntimeError("GUI 后端未运行")
            return asyncio.run_coroutine_threadsafe(coroutine, self.loop).result(
                timeout=30
            )
        except Exception:
            with suppress(Exception):
                coroutine.close()
            raise

    def add_log(self, message: str, level: str = "info") -> None:
        """追加一条有上限的运行日志，避免长期运行时内存无限增长。"""

        self.logs.append(
            {
                "time": now_text(),
                "level": level,
                "message": str(message),
            }
        )

    async def _enqueue_links(
        self,
        content: str,
        source: str,
    ) -> list[str]:
        """提取文本中的作品链接，为每个链接建立 pending 任务并放入队列。"""

        if not self.xhs or not self.task_queue:
            return []
        links = await self.xhs.extract_links(content)
        ids = []
        for link in links:
            task_id = uuid4().hex
            self.tasks[task_id] = TaskState(
                task_id,
                link,
                source=source,
                display_text=task_display_id(link),
            )
            self.task_queue.put_nowait(task_id)
            ids.append(task_id)
        return ids

    async def create_tasks(
        self,
        content: str,
    ) -> list[dict[str, Any]]:
        """创建手动任务并返回本次新建的任务；完整队列由状态快照提供。"""

        ids = await self._enqueue_links(content, "manual")
        if not ids:
            self.add_log(_("提取小红书作品链接失败"), "warning")
        return [self.tasks[i].as_dict() for i in ids]

    async def create_script_task(
        self,
        data: dict,
        index: list | tuple | None,
    ) -> dict[str, Any] | None:
        if not self.task_queue:
            return None
        task_id = uuid4().hex
        task = TaskState(
            task_id,
            "",
            script_data=data,
            index=index,
            display_text=data.get("noteId", ""),
        )
        self.tasks[task_id] = task
        self.task_queue.put_nowait(task_id)
        return task.as_dict()

    async def _worker_loop(self) -> None:
        """串行消费任务队列；任务进入 processing 后不再允许取消。"""

        while True:
            task_id = await self.task_queue.get()
            try:
                task = self.tasks.get(task_id)
                if task and task.state != "cancelled":
                    await self._process_task(task)
            finally:
                self.task_queue.task_done()

    async def _process_task(self, task: TaskState) -> None:
        """执行单个作品的跳过判断、提取和下载，并更新最终状态。"""

        if task.state != "pending":
            return
        task.state = "processing"
        try:
            # extract() 通过回调返回汇总统计，GUI 不根据 URL 推断任务结果。
            statistics: dict[str, Any] = {}

            def capture_statistics(value: dict[str, Any]) -> None:
                statistics.update(value)

            if task.script_data is None:
                await self.xhs.extract(
                    task.url,
                    True,
                    check_record=True,
                    progress_callback=self.on_file_progress,
                    task_id=task.task_id,
                    result_callback=capture_statistics,
                )
            else:
                await self.xhs.deal_script_tasks(
                    task.script_data,
                    task.index,
                    progress_callback=self.on_file_progress,
                    task_id=task.task_id,
                    result_callback=capture_statistics,
                )
            if statistics.get("success", 0):
                task.state = "success"
            elif statistics.get("skip", 0):
                task.state = "skipped"
            else:
                task.state = "failed"
            if self.xhs.manager.download_record:
                self.history_revision += 1
        except CancelledError:
            task.state = "cancelled"
            self.cancel_task_files(task.task_id)
            raise
        except Exception as error:
            task.state = "failed"
            self.add_log(str(error), "error")

    def on_file_progress(self, event: dict[str, Any]) -> None:
        """接收下载器的实时文件事件，按“任务 ID + 文件名”更新进度。"""

        task_id = event.get("task_id") or "unknown"
        filename = event.get("filename") or "unknown"
        file_id = f"{task_id}:{filename}"
        item = self.files.setdefault(
            file_id,
            {
                "file_id": file_id,
                "task_id": task_id,
                "filename": filename,
            },
        )
        item.update(
            {
                "completed_bytes": event.get("completed_bytes", 0),
                "total_bytes": event.get("total_bytes"),
                "state": event.get("state", "downloading"),
            }
        )

    def cancel_task_files(self, task_id: str) -> None:
        """任务被取消或终止时，把仍在下载的文件标记为 cancelled。"""

        for item in self.files.values():
            if item.get("task_id") == task_id and item.get("state") == "downloading":
                item["state"] = "cancelled"

    async def cancel_task(self, task_id: str) -> bool:
        """只允许取消尚未开始的 pending 任务，processing 任务不会被中断。"""

        task = self.tasks.get(task_id)
        if not task or task.state != "pending":
            return False
        task.state = "cancelled"
        return True

    async def clear_finished(self) -> int:
        """移除已结束任务及其文件快照，并返回移除数量。"""

        finished = {"success", "failed", "skipped", "cancelled"}
        removed = [
            task_id for task_id, task in self.tasks.items() if task.state in finished
        ]
        for task_id in removed:
            self.tasks.pop(task_id, None)
        for file_id, item in list(self.files.items()):
            if item.get("task_id") in removed:
                self.files.pop(file_id, None)
        return len(removed)

    async def start_monitor(self) -> dict[str, Any]:
        """清空剪贴板后启动监听；监听创建的任务与手动任务共用同一队列。"""

        if self.monitor_task and not self.monitor_task.done():
            return self.monitor
        await asyncio.to_thread(copy, "")
        self.monitor.update(
            {
                "active": True,
                "state": "running",
                "started_at": now_text(),
                "created": 0,
            }
        )
        self.monitor_task = asyncio.create_task(self._monitor_loop())
        self.add_log(_("已启动监听剪贴板模式"), "success")
        return self.monitor

    async def stop_monitor(self) -> dict[str, Any]:
        """停止读取剪贴板，但不影响已经进入任务队列的作品继续处理。"""

        if self.monitor_task:
            self.monitor_task.cancel()
            with suppress(CancelledError):
                await self.monitor_task
            self.monitor_task = None
        self.monitor.update({"active": False, "state": "stopped"})
        self.add_log(_("已停止读取剪贴板，队列中的任务继续处理"), "info")
        return self.monitor

    async def _monitor_loop(self) -> None:
        """每秒读取一次剪贴板，只处理自上次读取后出现的新内容。"""

        clipboard_cache = ""
        while True:
            try:
                content = await asyncio.to_thread(paste)
            except Exception as error:
                self.add_log(f"{_('读取剪贴板失败')}：{error}", "warning")
                await asyncio.sleep(1)
                continue
            if content and content != clipboard_cache:
                clipboard_cache = content
                created = await self._enqueue_links(content, "monitor")
                self.monitor["created"] += len(created)
            await asyncio.sleep(1)

    async def read_clipboard(self) -> str:
        """在线程池中读取系统剪贴板，避免阻塞 asyncio 事件循环。"""

        return await asyncio.to_thread(paste)

    async def get_history_page(self, query: str = "", page: int = 1) -> dict[str, Any]:
        """从数据库查询指定页的作品 ID；搜索在数据库端执行而非前端过滤。"""

        enabled = self.xhs.manager.download_record if self.xhs else False
        query = str(query or "").strip()[:200]
        try:
            requested_page = max(1, int(page))
        except (TypeError, ValueError):
            requested_page = 1
        if not enabled:
            return {
                "enabled": False,
                "items": [],
                "total": 0,
                "page": 0,
                "page_size": HISTORY_PAGE_SIZE,
                "page_count": 0,
                "query": query,
            }

        recorder = self.xhs.id_recorder
        total = await recorder.count(query)
        page_count = (total + HISTORY_PAGE_SIZE - 1) // HISTORY_PAGE_SIZE
        current_page = min(requested_page, page_count) if page_count else 0
        items = await recorder.page(
            query,
            HISTORY_PAGE_SIZE,
            (current_page - 1) * HISTORY_PAGE_SIZE if current_page else 0,
        )
        return {
            "enabled": True,
            "items": items,
            "total": total,
            "page": current_page,
            "page_size": HISTORY_PAGE_SIZE,
            "page_count": page_count,
            "query": query,
        }

    async def delete_history_records(
        self,
        ids: list[str],
        query: str = "",
        page: int = 1,
    ) -> dict[str, Any]:
        """删除界面当前选中的作品 ID 记录，并返回删除后的当前查询页。"""

        if self.xhs and self.xhs.manager.download_record:
            values = list(dict.fromkeys(str(i).strip() for i in ids if str(i).strip()))
            if values:
                await self.xhs.id_recorder.delete(values)
                self.history_revision += 1
                self.add_log(_("删除下载记录成功"), "info")
        return await self.get_history_page(query, page)

    async def get_settings(self) -> dict[str, Any]:
        """返回当前配置及实际生效的保存根路径。"""

        return self._settings_payload()

    async def get_translations(self) -> dict[str, Any]:
        """从 GUI 文案模块获取当前语言的完整语言包。"""

        language = self.settings["language"]
        return {
            "language": language,
            "messages": get_ui_translations(language),
            "name_fields": list(NAME_FORMAT_FIELDS),
        }

    async def get_disclaimer(self) -> dict[str, bool]:
        """返回免责声明确认状态。"""

        return {
            "accepted": self.settings["disclaimer_accepted"],
        }

    async def accept_disclaimer(self) -> dict[str, bool]:
        """记录用户已同意免责声明，并在首次同意后启动下载器运行时。"""

        if not self.settings["disclaimer_accepted"]:
            self.settings["disclaimer_accepted"] = True
            self.settings_manager.update(self.settings)
        await self._start_runtime()
        return {"accepted": True}

    def _settings_payload(self, values: dict[str, Any] | None = None) -> dict[str, Any]:
        """整理配置给前端；命名字段始终使用 Manager 的中文字段值。"""

        payload = dict(self.settings if values is None else values)
        configured_path = str(payload.get("work_path") or "").strip()
        if values is None and self.xhs:
            manager = self.xhs.manager
            # Manager 是运行时配置的唯一归一化入口，界面回显以实际生效值为准。
            payload.update(
                {
                    "work_path": str(manager.path),
                    "folder_name": manager.folder.name,
                    "name_format": manager.name_format,
                    "chunk": manager.chunk,
                    "timeout": manager.timeout,
                    "max_retry": manager.retry,
                    "image_format": manager.image_format,
                    "video_preference": manager.video_preference,
                    "proxy": manager.proxy,
                    "impersonate": manager.impersonate,
                    "record_data": manager.record_data,
                    "folder_mode": manager.folder_mode,
                    "download_record": manager.download_record,
                    "image_download": manager.image_download,
                    "video_download": manager.video_download,
                    "live_download": manager.live_download,
                    "author_archive": manager.author_archive,
                    "write_mtime": manager.write_mtime,
                    "script_server": manager.script_server,
                    "note_format": manager.note_format,
                }
            )
            effective_path = manager.path
        else:
            effective_path = Path(configured_path) if configured_path else VOLUME
        payload["effective_work_path"] = str(effective_path.resolve())
        return payload

    async def save_settings(self, data: dict[str, Any]) -> dict[str, Any]:
        """保存配置并重建下载器，使 Manager 处理后的新配置立即生效。"""

        if any(task.state == "processing" for task in self.tasks.values()):
            return {"ok": False, "error": _("请等待正在处理的任务结束后再保存配置")}
        if self.monitor_task and not self.monitor_task.done():
            return {"ok": False, "error": _("请先关闭剪贴板监听再保存配置")}
        # 仅接收 Settings.default 中定义的字段，避免前端额外数据进入配置。
        updated = dict(self.settings)
        updated.update(
            {key: value for key, value in data.items() if key in Settings.default}
        )
        # 英文字段名称可能包含空格，GUI 以数组提交；旧配置字符串仍按项目格式读取。
        configured_name_format = updated.get("name_format") or ""
        fields = (
            configured_name_format
            if isinstance(configured_name_format, list)
            else configured_name_format.split()
        )
        name_fields = [normalize_name_format_field(field) for field in fields]
        updated["name_format"] = " ".join(dict.fromkeys(name_fields))
        self.settings_manager.update(updated)
        await self._close_xhs()
        self.settings = updated
        await self._create_xhs()
        self.history_revision += 1
        self.add_log(_("配置已保存，下载器已重新加载"), "success")
        return {"ok": True, "settings": self._settings_payload()}

    async def check_update(self) -> dict[str, Any]:
        """请求 GitHub 发布页并比较版本，返回成功或可展示的错误结果。"""

        if not self.xhs:
            return {"status": "error", "message": _("下载器尚未初始化")}
        try:
            async with self.xhs.html.client.stream(
                "GET",
                RELEASES,
                timeout=8,
            ) as response:
                response.raise_for_status()
                return build_update_result(str(response.url))
        except Exception as error:
            self.add_log(f"{_('检测新版本失败')}：{error}", "error")
            return {
                "status": "error",
                "message": _("无法获取最新版本，请检查网络连接后重试"),
            }

    async def open_url(self, url: str) -> bool:
        """在线程池中调用系统浏览器打开关于页允许展示的外部链接。"""

        if url not in ABOUT_URLS.values():
            return False

        return await asyncio.to_thread(open_browser, url)

    async def open_download_folder(self) -> bool:
        """打开当前配置实际生效的作品文件储存目录。"""

        if not self.xhs:
            return False

        def open_path(path: Path) -> bool:
            try:
                path.mkdir(parents=True, exist_ok=True)
                if sys.platform == "win32":
                    from os import startfile

                    startfile(str(path))
                else:
                    command = "open" if sys.platform == "darwin" else "xdg-open"
                    Popen([command, str(path)], stdout=DEVNULL, stderr=DEVNULL)
                return True
            except Exception as error:
                self.add_log(f"{_('无法打开下载文件夹')}：{error}", "error")
                return False

        return await asyncio.to_thread(open_path, self.xhs.manager.folder.resolve())

    async def snapshot(self) -> dict[str, Any]:
        """生成前端轮询所需的完整只读状态快照。"""

        tasks = [task.as_dict() for task in self.tasks.values()]
        history_enabled = self.xhs.manager.download_record if self.xhs else False
        return {
            "disclaimer_accepted": self.settings["disclaimer_accepted"],
            "tasks": tasks,
            "files": list(self.files.values()),
            "history_enabled": history_enabled,
            "history_revision": self.history_revision,
            "logs": list(self.logs),
            "monitor": dict(self.monitor),
            "settings": self._settings_payload(),
            "about": {
                "version": f"{VERSION_MAJOR}.{VERSION_MINOR}",
                "release": "Beta" if VERSION_BETA else "Stable",
                "license": LICENCE,
                "repository": REPOSITORY,
                "author": "JoeanAmier",
                "links": dict(ABOUT_URLS),
            },
        }


class GuiApi:
    """PyWebView 暴露的同步 API，内部统一转发到后台 asyncio 循环。"""

    def __init__(self, backend: GuiBackend):
        # PyWebView 会递归暴露 js_api 的公共属性；实现对象保持私有，
        # 避免创建 JavaScript 桥接时遍历到后端内部控制对象。
        self._backend = backend
        self._window: Any | None = None

    def _bind_window(self, window: Any) -> None:
        """保存窗口对象，供目录选择对话框使用。"""

        self._window = window

    def get_state(self) -> dict[str, Any]:
        """获取一次前端状态快照。"""

        return self._backend.call(self._backend.snapshot())

    def paste_content(self) -> str:
        """读取剪贴板文本。"""

        return self._backend.call(self._backend.read_clipboard())

    def browse_directory(self, directory: str = "") -> str:
        """打开系统目录选择器并返回用户选中的路径。"""

        if not self._window:
            raise RuntimeError("GUI 窗口尚未就绪")

        initial = Path(str(directory or ""))
        dialog_directory = str(initial) if initial.is_dir() else ""
        file_dialog = getattr(webview, "FileDialog", None)
        dialog_type = file_dialog.FOLDER if file_dialog else webview.FOLDER_DIALOG
        selected = self._window.create_file_dialog(
            dialog_type,
            directory=dialog_directory,
            allow_multiple=False,
        )
        return str(selected[0]) if selected else ""

    def create_tasks(
        self,
        content: str,
    ) -> list[dict[str, Any]]:
        """通过桥接创建任务。"""

        return self._backend.call(self._backend.create_tasks(content))

    def cancel_task(self, task_id: str) -> bool:
        """取消一个仍处于 pending 状态的任务。"""

        return self._backend.call(self._backend.cancel_task(task_id))

    def clear_finished(self) -> int:
        """清理已完成、失败、跳过或取消的任务。"""

        return self._backend.call(self._backend.clear_finished())

    def start_monitor(self) -> dict[str, Any]:
        """启动剪贴板监听模式。"""

        return self._backend.call(self._backend.start_monitor())

    def stop_monitor(self) -> dict[str, Any]:
        """停止剪贴板监听，但保留已创建的队列任务。"""

        return self._backend.call(self._backend.stop_monitor())

    def get_history_page(self, query: str = "", page: int = 1) -> dict[str, Any]:
        """查询下载记录的指定页。"""

        return self._backend.call(self._backend.get_history_page(query, page))

    def delete_history_records(
        self,
        ids: list[str],
        query: str = "",
        page: int = 1,
    ) -> dict[str, Any]:
        """删除界面选中的下载记录。"""

        return self._backend.call(
            self._backend.delete_history_records(ids, query, page)
        )

    def get_settings(self) -> dict[str, Any]:
        """读取当前配置。"""

        return self._backend.call(self._backend.get_settings())

    def get_translations(self) -> dict[str, Any]:
        """读取当前语言的 GUI 文案。"""

        return self._backend.call(self._backend.get_translations())

    def get_disclaimer(self) -> dict[str, bool]:
        """读取免责声明确认状态。"""

        return self._backend.call(self._backend.get_disclaimer())

    def accept_disclaimer(self) -> dict[str, bool]:
        """确认免责声明并初始化 GUI 后端运行时。"""

        return self._backend.call(self._backend.accept_disclaimer())

    def decline_disclaimer(self) -> bool:
        """不同意免责声明时关闭 GUI 窗口。"""

        if not self._window:
            return False
        self._window.destroy()
        return True

    def save_settings(self, data: dict[str, Any]) -> dict[str, Any]:
        """保存 GUI 提交的配置。"""

        return self._backend.call(self._backend.save_settings(data))

    def check_update(self) -> dict[str, Any]:
        """检查远端版本并返回可展示的结果。"""

        return self._backend.call(self._backend.check_update())

    def open_url(self, url: str) -> bool:
        """请求系统浏览器打开关于页允许展示的外部链接。"""

        return self._backend.call(self._backend.open_url(url))

    def open_download_folder(self) -> bool:
        """请求系统文件管理器打开当前下载目录。"""

        return self._backend.call(self._backend.open_download_folder())

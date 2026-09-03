from ..module import Manager
from ..translation import _, switch_language

# 记录 GUI 最近一次加载的语言，避免核心和 GUI 连续设置同一语言时重复切换。
_UI_LANGUAGE: str | None = None

# 文件命名字段的后端固定值由 Manager 统一维护，GUI 只维护英文显示名称。
NAME_FORMAT_FIELDS = Manager.NAME_KEYS
NAME_FORMAT_ENGLISH_LABELS = (
    "Favorite Count",
    "Comment Count",
    "Share Count",
    "Like Count",
    "Note Tags",
    "Note ID",
    "Note Title",
    "Note Desc",
    "Note Type",
    "Publish Time",
    "Update Time",
    "Nickname",
    "Author ID",
)

# 英文界面提交字段名称时，后端将其还原为 Manager 使用的中文字段值。
NAME_FORMAT_VALUES = dict(zip(NAME_FORMAT_ENGLISH_LABELS, NAME_FORMAT_FIELDS))


def get_ui_messages() -> dict[str, str]:
    """使用当前翻译器生成 GUI 文本字典。"""

    return {
        "nav.new_task": _("创建任务"),
        "nav.queue": _("任务队列"),
        "nav.monitor": _("剪贴板模式"),
        "nav.history": _("下载记录"),
        "nav.logs": _("运行日志"),
        "nav.settings": _("程序设置"),
        "nav.disclaimer": _("免责声明"),
        "nav.about": _("关于项目"),
        "task.link": _("请输入小红书图文/视频作品链接"),
        "task.link_placeholder": _("多个链接之间使用空格或换行分隔"),
        "task.index": _("图片序号"),
        "task.index_placeholder": _("例如：1 3 5，留空表示全部，仅限处理单个链接"),
        "task.paste": _("读取剪贴板"),
        "task.paste_process": _("读取剪贴板并处理"),
        "task.clear": _("清空输入框"),
        "task.start": _("处理任务"),
        "task.queue_empty": _("任务队列为空"),
        "task.view_queue": _("查看任务队列"),
        "monitor.start": _("开启监听"),
        "monitor.stop": _("关闭监听"),
        "monitor.status": _("运行状态"),
        "monitor.inactive": _("未开启"),
        "monitor.active": _("监听中"),
        "monitor.created": _("处理任务数量"),
        "monitor.queue": _("监听任务队列"),
        "monitor.queue_empty": _("监听任务队列为空"),
        "queue.clear_finished": _("清理已结束任务"),
        "queue.open_folder": _("打开下载文件夹"),
        "queue.pending": _("待处理"),
        "queue.processing": _("处理中"),
        "queue.success": _("成功"),
        "queue.failed": _("失败"),
        "queue.skipped": _("跳过"),
        "queue.cancelled": _("已取消"),
        "queue.all": _("全部"),
        "queue.current_filter_empty": _("当前筛选结果为空"),
        "download.files": _("文件下载进度"),
        "download.empty": _("暂无文件下载"),
        "download.unknown_size": _("未知大小"),
        "unit.item": _("项"),
        "unit.file": _("个文件"),
        "history.delete_selected": _("删除选中记录"),
        "history.search_placeholder": _("搜索作品 ID"),
        "history.select_page": _("全选本页"),
        "history.invert_page": _("反选本页"),
        "history.selected": _("已选 {0} 条"),
        "history.empty": _("暂无下载记录"),
        "history.previous": _("上一页"),
        "history.next": _("下一页"),
        "history.disabled": _("作品下载记录功能已关闭"),
        "history.range": _("第 {0}–{1} 条，共 {2} 条{3}"),
        "history.search_results": _("搜索结果"),
        "history.no_match": _("未找到匹配的作品 ID"),
        "history.read_failed": _("读取下载记录失败"),
        "history.deleted_selected": _("已删除 {0} 条下载记录"),
        "settings.discard": _("放弃更改"),
        "settings.save": _("保存配置"),
        "settings.download": _("下载设置"),
        "settings.archive": _("归档与记录"),
        "settings.network": _("网络与请求"),
        "settings.general": _("通用设置"),
        "settings.work_path": _("工作目录"),
        "settings.browse": _("浏览"),
        "settings.work_path_help": _("保存作品文件和作品数据的根目录"),
        "settings.folder_name": _("作品文件夹"),
        "settings.folder_name_help": _("工作目录下用于保存作品文件的文件夹名称"),
        "settings.name_format": _("作品文件名称格式"),
        "settings.name_format_help": _("已启用字段按顺序以下划线拼接为作品文件名称"),
        "settings.enabled_fields": _("已启用字段"),
        "settings.disabled_fields": _("未启用字段"),
        "settings.image_download": _("图文作品下载开关"),
        "settings.image_download_help": _("关闭后，跳过下载图文和图集作品文件"),
        "settings.video_download": _("视频作品下载开关"),
        "settings.video_download_help": _("关闭后，跳过下载视频作品文件"),
        "settings.live_download": _("动态图片下载开关"),
        "settings.live_download_help": _(
            "关闭后，跳过下载图文和图集作品的动态图片文件，需同时开启图文作品下载"
        ),
        "settings.image_format": _("图片下载格式"),
        "settings.video_preference": _("视频下载偏好"),
        "settings.video_preference_resolution": _("分辨率优先"),
        "settings.video_preference_bitrate": _("码率优先"),
        "settings.video_preference_size": _("文件大小优先"),
        "settings.note_format": _("作品信息保存格式"),
        "settings.note_format_none": _("不保存"),
        "settings.note_format_all": _("全部格式"),
        "settings.folder_mode": _("作品归档保存模式"),
        "settings.folder_mode_help": _("开启后，每个作品的文件使用独立的文件夹保存"),
        "settings.author_archive": _("作者归档保存模式"),
        "settings.author_archive_help": _("开启后，每个作者的作品使用独立的文件夹保存"),
        "settings.download_record": _("作品下载记录开关"),
        "settings.download_record_help": _(
            "开启后，下载成功的作品 ID 会写入 ExploreID.db（SQLite 数据库）；再次处理相同作品时跳过"
        ),
        "settings.record_data": _("作品数据记录开关"),
        "settings.record_data_help": _(
            "开启后，处理成功的作品数据会写入 ExploreData.db（SQLite 数据库）"
        ),
        "settings.write_mtime": _("同步文件修改时间"),
        "settings.write_mtime_help": _(
            "开启后，作品文件属性的修改时间会被设置为作品发布时间"
        ),
        "settings.impersonate": _("浏览器模拟目标"),
        "settings.cookie": _("Cookie"),
        "settings.proxy": _("网络代理"),
        "settings.proxy_placeholder": _("不使用代理"),
        "settings.proxy_download": _("下载文件时使用网络代理"),
        "settings.timeout": _("请求超时时间"),
        "settings.second": _("秒"),
        "settings.retry": _("请求数据失败时，重试的最大次数"),
        "settings.times": _("次"),
        "settings.chunk": _("下载数据块大小"),
        "settings.byte": _("字节"),
        "settings.chunk_help": _("每次从下载响应中读取并写入临时文件的数据量"),
        "settings.language": _("程序语言"),
        "settings.chinese": "简体中文",
        "settings.english": "English",
        "settings.script_server": _("脚本服务器开关"),
        "settings.script_server_help": _(
            "启动 WebSocket 服务，接收来自用户脚本的下载任务"
        ),
        "settings.saved": _("程序配置已保存"),
        "settings.discarded": _("已放弃未保存更改"),
        "about.description": _("小红书（XiaoHongShu、RedNote）作品采集工具"),
        "about.version": _("程序版本"),
        "about.author": _("项目作者"),
        "about.license": _("开源协议"),
        "about.repository": _("项目仓库"),
        "about.open_repository": _("跳转至项目 GitHub 仓库"),
        "about.support": _(
            "如果 XHS-Downloader 对您有帮助，请考虑为它点个 Star，感谢您的支持！"
        ),
        "about.community": _("Discord 社区"),
        "about.invite_link": _("邀请链接"),
        "about.other_projects": _("作者的其他开源项目"),
        "about.project_tk": _("DouK-Downloader (抖音 / TikTok)"),
        "about.project_ks": _("KS-Downloader (快手)"),
        "update.check": _("检查更新"),
        "update.checking": _("正在检查新版本，请稍等..."),
        "update.failed": _("检测新版本失败"),
        "disclaimer.content": _("免责声明\n"),
        "disclaimer.confirm": _("已阅读并同意"),
        "disclaimer.decline": _("不同意并退出"),
        "modal.delete_history": _("删除下载记录"),
        "modal.delete_history_confirm": _("确定删除选中的 {0} 条记录？"),
        "modal.delete_history_warning": _("此操作无法撤销，但不会删除已经下载的文件。"),
        "modal.cancel": _("取消"),
        "modal.confirm_delete": _("确认删除"),
        "toast.cannot_cancel": _("无法取消任务"),
        "toast.browser_unavailable": _("无法打开系统浏览器"),
        "toast.folder_unavailable": _("无法打开下载文件夹"),
        "toast.language_load_failed": _("语言文件加载失败"),
        "toast.operation_failed": _("操作失败"),
        "toast.no_supported_link": _("提取小红书作品链接失败"),
        "name.drag_disable": _("拖动调整顺序，点击停用"),
        "name.drag_enable": _("拖动或点击启用"),
    }


def get_ui_translations(language: str) -> dict[str, str]:
    """切换语言并生成前端使用的 GUI 语言包。"""

    global _UI_LANGUAGE
    if language != _UI_LANGUAGE:
        switch_language(language)
        _UI_LANGUAGE = language
    return get_ui_messages() | _build_name_format_labels(language)


def _build_name_format_labels(language: str) -> dict[str, str]:
    """生成命名格式字段的当前语言显示名称。"""

    return {
        field: label if language == "en_US" else field
        for field, label in zip(NAME_FORMAT_FIELDS, NAME_FORMAT_ENGLISH_LABELS)
    }


def normalize_name_format_field(field: str) -> str:
    """将前端提交的中文或英文显示名称转换为后端中文字段值。"""

    if field in NAME_FORMAT_FIELDS:
        return field
    if field in NAME_FORMAT_VALUES:
        return NAME_FORMAT_VALUES[field]
    return field

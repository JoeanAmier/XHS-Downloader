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
        "nav.queue": _("处理队列"),
        "nav.monitor": _("剪贴板模式"),
        "nav.history": _("下载记录"),
        "nav.logs": _("运行日志"),
        "nav.settings": _("程序设置"),
        "nav.about": _("关于项目"),
        "page.new_task": _("输入一个或多个小红书作品链接，并加入处理队列"),
        "page.queue": _("按状态筛选任务，并查看每个文件的实时下载进度"),
        "page.logs": _("查看当前运行期间的处理与下载日志"),
        "page.settings": _("配置下载内容、文件保存、归档记录和网络请求"),
        "task.link": _("小红书作品链接"),
        "task.link_placeholder": _("请输入小红书图文/视频作品链接"),
        "task.paste": _("读取剪贴板"),
        "task.paste_process": _("粘贴内容并处理"),
        "task.clear": _("清空输入框"),
        "task.start": _("开始处理"),
        "task.queue_empty": _("任务队列为空"),
        "task.view_queue": _("查看处理队列"),
        "monitor.description": _(
            "持续读取剪贴板，将新出现的小红书作品链接加入任务队列；停止监听不影响已创建任务"
        ),
        "monitor.reading": _(
            "正在读取剪贴板中的新链接；停止监听后，已创建任务继续处理"
        ),
        "monitor.start": _("开启监听"),
        "monitor.stop": _("关闭监听"),
        "monitor.status": _("运行状态"),
        "monitor.inactive": _("未开启"),
        "monitor.active": _("监听中"),
        "monitor.detected": _("本次识别"),
        "monitor.created": _("已创建任务"),
        "monitor.queue": _("监听任务队列"),
        "monitor.queue_empty": _("监听任务队列为空"),
        "queue.clear_finished": _("清理已结束任务"),
        "queue.open_folder": _("打开下载文件夹"),
        "queue.pending": _("待处理"),
        "queue.processing": _("处理中"),
        "queue.success": _("成功"),
        "queue.failed": _("失败"),
        "queue.skipped": _("已跳过"),
        "queue.cancelled": _("已取消"),
        "queue.all": _("全部"),
        "queue.current_filter_empty": _("当前筛选结果为空"),
        "download.files": _("文件下载"),
        "download.empty": _("暂无文件下载"),
        "download.unknown_size": _("未知大小"),
        "unit.item": _("项"),
        "unit.file": _("个文件"),
        "unit.link": _("个链接"),
        "history.summary": _("共 {0} 条记录"),
        "history.delete_selected": _("删除选中"),
        "history.search_placeholder": _("搜索作品 ID"),
        "history.select_page": _("全选本页"),
        "history.invert_page": _("反选本页"),
        "history.selected": _("已选 {0} 条"),
        "history.empty": _("暂无下载记录"),
        "history.no_records": _("暂无记录"),
        "history.previous": _("上一页"),
        "history.next": _("下一页"),
        "history.disabled": _("下载记录功能已关闭"),
        "history.disabled_description": _("在程序设置中开启“作品下载记录开关”后可用"),
        "history.query_id": _("查询 ExploreID.db 中成功下载的作品 ID"),
        "history.query_disabled": _("下载记录已关闭，当前不可用"),
        "history.found": _("找到 {0} 条记录"),
        "history.range": _("第 {0}–{1} 条，共 {2} 条{3}"),
        "history.search_results": _("搜索结果"),
        "history.no_match": _("未找到匹配的作品 ID"),
        "history.read_failed": _("读取下载记录失败"),
        "history.deleted_selected": _("已删除 {0} 条下载记录"),
        "settings.discard": _("放弃更改"),
        "settings.save": _("保存配置"),
        "settings.download": _("下载与保存"),
        "settings.format": _("下载内容与格式"),
        "settings.archive": _("归档与记录"),
        "settings.network": _("网络与请求"),
        "settings.general": _("通用"),
        "settings.work_path": _("作品数据 / 文件保存根路径"),
        "settings.browse": _("浏览"),
        "settings.work_path_help": _(
            "作品文件储存文件夹会在此路径下创建；留空时使用程序的 Volume 目录"
        ),
        "settings.folder_name": _("作品文件储存文件夹名称"),
        "settings.folder_name_help": _("作品文件保存在“保存根路径/文件夹名称”目录中"),
        "settings.name_format": _("作品文件名称格式"),
        "settings.name_format_help": _("启用字段按当前顺序以下划线连接为作品文件名"),
        "settings.enabled_fields": _("启用字段"),
        "settings.disabled_fields": _("未启用字段"),
        "settings.image_download": _("图文作品下载开关"),
        "settings.image_download_help": _("下载图文和图集作品中的图片文件"),
        "settings.video_download": _("视频作品下载开关"),
        "settings.video_download_help": _("控制视频作品文件是否下载"),
        "settings.live_download": _("动图文件下载开关"),
        "settings.live_download_help": _(
            "控制图文作品中的动图文件是否下载，需同时开启图文作品下载"
        ),
        "settings.image_format": _("图片下载格式"),
        "settings.image_format_help": _("指定图文、图集作品图片的下载格式"),
        "settings.video_preference": _("视频下载偏好"),
        "settings.video_preference_resolution": _("分辨率优先"),
        "settings.video_preference_bitrate": _("码率优先"),
        "settings.video_preference_size": _("文件大小优先"),
        "settings.video_preference_help": _(
            "作品提供多个视频资源时，按所选指标从高到低选择一个文件"
        ),
        "settings.note_format": _("作品信息保存格式"),
        "settings.note_format_none": _("不保存"),
        "settings.note_format_all": _("Markdown 与 TXT"),
        "settings.note_format_help": _("在作品文件目录中保存该作品的采集信息文件"),
        "settings.folder_mode": _("作品归档保存模式"),
        "settings.folder_mode_help": _(
            "以生成的作品文件名创建目录，再保存该作品的全部文件"
        ),
        "settings.author_archive": _("作者归档保存模式"),
        "settings.author_archive_help": _(
            "先按“作者ID_作者昵称”建立作者子目录；同时开启作品归档时，作品目录位于作者目录下"
        ),
        "settings.download_record": _("作品下载记录开关"),
        "settings.download_record_help": _(
            "成功下载的作品 ID 写入程序 Volume 目录的 ExploreID.db；已有记录的作品会跳过下载"
        ),
        "settings.record_data": _("记录作品详细数据"),
        "settings.record_data_help": _(
            "将作品数据写入“保存根目录/作品文件储存文件夹/ExploreData.db”，每个作品保存一条记录"
        ),
        "settings.write_mtime": _("文件修改时间"),
        "settings.write_mtime_help": _(
            "将已下载文件的文件系统修改时间设置为作品发布时间"
        ),
        "settings.cookie": _("小红书网页版 Cookie"),
        "settings.cookie_placeholder": _("粘贴小红书网页版 Cookie"),
        "settings.cookie_help": _("随网页请求发送；留空时不发送 Cookie"),
        "settings.user_agent_help": _("随网页请求和文件下载请求发送的 User-Agent"),
        "settings.proxy": _("网络代理"),
        "settings.proxy_placeholder": _("不使用代理"),
        "settings.proxy_help": _(
            "网页请求和文件下载请求使用的 HTTP/HTTPS 代理；留空时直连"
        ),
        "settings.timeout": _("请求超时时间"),
        "settings.second": _("秒"),
        "settings.retry": _("请求数据失败时，重试的最大次数"),
        "settings.times": _("次"),
        "settings.chunk": _("下载数据块大小"),
        "settings.byte": _("字节"),
        "settings.chunk_help": _("每次从下载响应中读取并写入临时文件的数据量"),
        "settings.language": _("程序语言"),
        "settings.chinese": _("简体中文"),
        "settings.english": _("English"),
        "settings.language_help": _(
            "使用项目现有语言文件；没有对应翻译的界面文本保留中文"
        ),
        "settings.script_server": _("脚本服务器开关"),
        "settings.script_server_help": _(
            "在 0.0.0.0:5558 启动 WebSocket 服务，接收用户脚本提交的下载任务"
        ),
        "settings.saved": _("配置已保存"),
        "settings.reloaded": _("下载器已重新加载"),
        "settings.discarded": _("已放弃未保存更改"),
        "about.description": _("小红书作品链接提取、作品数据采集与文件下载工具"),
        "about.version": _("当前版本"),
        "about.author": _("作者"),
        "about.license": _("开源协议"),
        "about.repository": _("项目仓库"),
        "about.open_repository": _("跳转至项目 GitHub 仓库"),
        "update.check": _("检查更新"),
        "update.checking": _("正在检查新版本，请稍等..."),
        "update.failed": _("检测新版本失败"),
        "disclaimer.content": _("免责声明\n"),
        "disclaimer.confirm": _("我已阅读并同意"),
        "disclaimer.decline": _("不同意并退出"),
        "modal.delete_history": _("删除下载记录"),
        "modal.delete_history_detail": _("仅删除当前选中的作品 ID 记录"),
        "modal.delete_history_confirm": _("确定删除选中的 {0} 条记录？"),
        "modal.delete_history_warning": _("此操作无法撤销，但不会删除已经下载的文件。"),
        "modal.cancel": _("取消"),
        "modal.confirm_delete": _("确认删除"),
        "toast.exit_monitor_first": _("请先退出监听模式"),
        "toast.monitor_switch_locked": _("监听期间无法切换到其他功能"),
        "toast.cannot_cancel": _("无法取消任务"),
        "toast.started_task": _("任务已经开始，只有待处理任务可以取消"),
        "toast.browser_unavailable": _("无法打开系统浏览器"),
        "toast.folder_unavailable": _("无法打开下载文件夹"),
        "toast.language_load_failed": _("语言文件加载失败"),
        "toast.operation_failed": _("操作失败"),
        "toast.no_supported_link": _("未识别到支持的作品链接"),
        "name.drag_disable": _("拖动调整顺序，点击停用"),
        "name.drag_enable": _("拖动或点击启用"),
        "state.processing_detail": _("正在处理作品"),
        "state.pending_detail": _("等待队列处理"),
        "state.success_detail": _("处理完成"),
        "state.failed_detail": _("处理失败"),
        "state.skipped_detail": _("作品文件下载任务未执行"),
    }


def get_ui_translations(language: str) -> dict[str, str]:
    """切换语言并生成前端使用的 GUI 语言包。"""

    global _UI_LANGUAGE
    if language != _UI_LANGUAGE:
        switch_language(language)
        _UI_LANGUAGE = language
    messages = get_ui_messages()
    messages.update(_build_name_format_labels(language))
    return messages


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

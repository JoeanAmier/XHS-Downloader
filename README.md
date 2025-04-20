<div align="center">
<img src="static/XHS-Downloader.png" alt="XHS-Downloader" height="256" width="256"><br>
<h1>XHS-Downloader</h1>
<p>简体中文 | <a href="README_EN.md">English</a></p>
<a href="https://trendshift.io/repositories/5435" target="_blank"><img src="https://trendshift.io/api/badge/repositories/5435" alt="JoeanAmier%2FXHS-Downloader | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
<br>
<img alt="GitHub" src="https://img.shields.io/github/license/JoeanAmier/XHS-Downloader?style=for-the-badge&color=ff7a45">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/JoeanAmier/XHS-Downloader?style=for-the-badge&color=9254de">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/JoeanAmier/XHS-Downloader?style=for-the-badge&color=ff7875">
<img alt="Static Badge" src="https://img.shields.io/badge/UserScript-ffec3d?style=for-the-badge&logo=tampermonkey&logoColor=%2300485B">
<br>
<img alt="Static Badge" src="https://img.shields.io/badge/Python-3.12-3498db?style=for-the-badge&logo=python&labelColor=fffa65">
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/JoeanAmier/XHS-Downloader?style=for-the-badge&color=73d13d">
<img alt="GitHub release (with filter)" src="https://img.shields.io/github/v/release/JoeanAmier/XHS-Downloader?style=for-the-badge&color=40a9ff">
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/JoeanAmier/XHS-Downloader/total?style=for-the-badge&color=f759ab">
</div>
<br>
<p>🔥 <b>小红书链接提取/作品采集工具</b>：提取账号发布、收藏、点赞、专辑作品链接；提取搜索结果作品链接、用户链接；采集小红书作品信息；提取小红书作品下载地址；下载小红书无水印作品文件！</p>
<p>🔥 “小红书”、“XiaoHongShu”、“RedNote” 含义相同，本项目统称为 “小红书”</p>
<p>⭐ 本项目完全免费开源，无任何收费功能，请勿上当受骗！</p>
<h1>📑 项目功能</h1>
<ul><b>程序功能</b>
<li>✅ 采集小红书作品信息</li>
<li>✅ 提取小红书作品下载地址</li>
<li>✅ 下载小红书无水印作品文件</li>
<li>✅ 下载小红书 livePhoto 文件(非无水印)</li>
<li>✅ 自动跳过已下载的作品文件</li>
<li>✅ 作品文件完整性处理机制</li>
<li>✅ 自定义图文作品文件下载格式</li>
<li>✅ 持久化储存作品信息至文件</li>
<li>✅ 作品文件储存至单独文件夹</li>
<li>✅ 后台监听剪贴板下载作品</li>
<li>✅ 记录已下载作品 ID</li>
<li>✅ 支持命令行下载作品文件</li>
<li>✅ 从浏览器读取 Cookie</li> 
<li>✅ 自定义文件名称格式</li> 
<li>✅ 支持 API 调用功能</li>
<li>✅ 支持文件断点续传下载</li>
<li>✅ 智能识别作品文件类型</li>
<li>✅ 支持设置作者备注</li>
<li>✅ 自动更新作者昵称</li>
</ul>
<ul><a href="#user-scripts"><b>脚本功能</b></a>
<li>✅ 下载小红书无水印作品文件</li>
<li>✅ 提取推荐页面作品链接</li>
<li>✅ 提取账号发布作品链接</li>
<li>✅ 提取账号收藏作品链接</li>
<li>✅ 提取账号点赞作品链接</li>
<li>✅ 提取账号专辑作品链接</li>
<li>✅ 提取搜索结果作品链接</li>
<li>✅ 提取搜索结果用户链接</li>
</ul>
<p>⭐ XHS-Downloader 开发计划及进度可前往 <a href="https://github.com/users/JoeanAmier/projects/5">Projects</a> 查阅</p>
<h1>📸 程序截图</h1>
<p><b>🎥 点击图片观看演示视频</b></p>
<a href="https://www.bilibili.com/video/BV1c56BYJEFm/"><img src="static/screenshot/程序运行截图CN1.png" alt=""></a>
<hr>
<a href="https://www.bilibili.com/video/BV1c56BYJEFm/"><img src="static/screenshot/程序运行截图CN2.png" alt=""></a>
<hr>
<a href="https://www.bilibili.com/video/BV1c56BYJEFm/"><img src="static/screenshot/程序运行截图CN3.png" alt=""></a>
<h1>🔗 支持链接</h1>
<ul>
<li><code>https://www.xiaohongshu.com/explore/作品ID?xsec_token=XXX</code></li>
<li><code>https://www.xiaohongshu.com/discovery/item/作品ID?xsec_token=XXX</code></li>
<li><code>https://xhslink.com/分享码</code></li>
<br/>
<p><b>支持单次输入多个作品链接，链接之间使用空格分隔；程序会自动提取有效链接，无需额外处理！</b></p>
</ul>
<h1>🪟 关于终端</h1>
<p>⭐ 推荐使用 <a href="https://learn.microsoft.com/zh-cn/windows/terminal/install">Windows 终端</a> （Windows 11 默认终端）运行程序以便获得最佳显示效果！</p>
<h1>🥣 使用方法</h1>
<p>如果仅需下载无水印作品文件，建议选择 <b>程序运行</b> 或 <b>Docker 运行</b>；如果有其他需求，建议选择 <b>源码运行</b>！</p>
<p><code>2.2</code> 版本开始，项目功能无异常的情况下，无需额外处理 Cookie！</p>
<h2>🖱 程序运行</h2>
<p>⭐ Mac OS、Windows 10 及以上用户可前往 <a href="https://github.com/JoeanAmier/XHS-Downloader/releases/latest">Releases</a> 或者 <a href="https://github.com/JoeanAmier/XHS-Downloader/actions">Actions</a> 下载程序压缩包，解压后打开程序文件夹，双击运行 <code>main</code> 即可使用。</p>
<p>⭐ 本项目包含自动构建可执行文件的 GitHub Actions，使用者可以随时使用 GitHub Actions 将最新源码构建为可执行文件！</p>
<p><strong>注意：Mac OS 平台可执行文件 <code>main</code> 可能需要从终端命令行启动；受设备限制，Mac OS 平台可执行文件尚未经过测试，无法保证可用性！</strong></p>
<p>若通过此方式使用程序，文件默认下载路径为：<code>.\_internal\Download</code>；配置文件路径为：<code>.\_internal\settings.json</code></p>
<h2>⌨️ Docker 运行</h2>
<ol>
<li>获取镜像</li>
<ul>
<li>方式一：使用 <code>Dockerfile</code> 文件构建镜像</li>
<li>方式二：使用 <code>docker pull joeanamier/xhs-downloader</code> 命令拉取镜像</li>
</ul>
<li>创建容器</li>
<ul>
<li>TUI 模式：<code>docker run --name 容器名称(可选) -p 主机端口号:6666 -it joeanamier/xhs-downloader</code></li>
<li>API 模式：<code>docker run --name 容器名称(可选) -p 主机端口号:6666 -it joeanamier/xhs-downloader python main.py server</code></li>
</ul>
<li>运行容器
<ul>
<li>启动容器：<code>docker start -i 容器名称/容器 ID</code></li>
<li>重启容器：<code>docker restart -i 容器名称/容器 ID</code></li>
</ul>
</li>
</ol>
<p>Docker 运行项目时不支持 <b>命令行调用模式</b>，无法使用 <b>读取剪贴板</b> 与 <b>监听剪贴板</b> 功能，可以正常粘贴内容，其他功能如有异常请反馈！</p>
<h2>⌨️ 源码运行</h2>
<ol>

[//]: # (<li>安装版本号不低于 <code>3.12</code> 的 Python 解释器</li>)
<li>安装版本号为 <code>3.12</code> 的 Python 解释器</li>
<li>下载本项目最新的源码或 <a href="https://github.com/JoeanAmier/XHS-Downloader/releases/latest">Releases</a> 发布的源码至本地</li>
<li>打开终端，切换至项目根路径</li>
<li>运行 <code>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt</code> 命令安装程序所需模块</li>
<li>运行 <code>main.py</code> 即可使用</li>
</ol>
<h1>🛠 命令行模式</h1>
<p>项目支持命令行运行模式，若想要下载图文作品的部分图片，可以使用此模式设置需要下载的图片序号！</p>
<p>可以使用命令行 <b>从浏览器读取 Cookie 并写入配置文件！</b></p>
<p>命令示例：<code>python .\main.py --browser_cookie Chrome --update_settings</code></p>
<p><code>bool</code> 类型参数支持使用 <code>true</code>、<code>false</code>、<code>1</code>、<code>0</code>、<code>yes</code>、<code>no</code>、<code>on</code> 或 <code>off</code>（不区分大小写）来设置。</p>
<hr>
<img src="static/screenshot/命令行模式截图CN1.png" alt="">
<hr>
<img src="static/screenshot/命令行模式截图CN2.png" alt="">
<h1>🖥 服务器模式</h1>
<p><b>启动：</b>运行命令：<code>python .\main.py server</code></p>
<p><b>关闭：</b>按下 <code>Ctrl</code> + <code>C</code> 关闭服务器</p>
<p>访问 <code>http://127.0.0.1:6666/docs</code> 或者 <code>http://127.0.0.1:6666/redoc</code>；你会看到自动生成的交互式 API 文档！</p>
<p><b>请求接口：</b><code>/xhs/</code></p>
<p><b>请求方法：</b><code>POST</code></p>
<p><b>请求格式：</b><code>JSON</code></p>
<p><b>请求参数：</b></p>
<table>
<thead>
<tr>
<th align="center">参数</th>
<th align="center">类型</th>
<th align="center">含义</th>
<th align="center">默认值</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">url</td>
<td align="center">str</td>
<td align="center">小红书作品链接，自动提取，不支持多链接；必需参数</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">download</td>
<td align="center">bool</td>
<td align="center">是否下载作品文件；设置为 <code>true</code> 将会耗费更多时间；可选参数</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">index</td>
<td align="center">list[int]</td>
<td align="center">下载指定序号的图片文件，仅对图文作品生效；<code>download</code> 参数设置为 <code>false</code> 时不生效；可选参数</td>
<td align="center">null</td>
</tr>
<tr>
<td align="center">cookie</td>
<td align="center">str</td>
<td align="center">请求数据时使用的 Cookie；可选参数</td>
<td align="center">配置文件 cookie 参数</td>
</tr>
<tr>
<td align="center">proxy</td>
<td align="center">str</td>
<td align="center">请求数据时使用的代理；可选参数</td>
<td align="center">配置文件 proxy 参数</td>
</tr>
<tr>
<td align="center">skip</td>
<td align="center">bool</td>
<td align="center">是否跳过存在下载记录的作品；设置为 <code>true</code> 将不会返回存在下载记录的作品数据；可选参数</td>
<td align="center">false</td>
</tr>
</tbody>
</table>
<p><b>代码示例：</b></p>
<pre>
async def example_api():
    """通过 API 设置参数，适合二次开发"""
    server = "http://127.0.0.1:6666/xhs/"
    data = {
        "url": "",  # 必需参数
        "download": True,
        "index": [
            3,
            6,
            9,
        ],
        "proxy": "http://127.0.0.1:10808",
    }
    response = post(server, json=data, timeout=10)
    print(response.json())
</pre>
<h1>📜 其他说明</h1>
<ul>
<li>由于作品链接携带日期信息，使用先前日期获取的作品链接可能会被风控，建议下载作品文件时使用最新获取的作品链接</li>
<li>Windows 系统需要以管理员身份运行程序才能读取 Chromium、Chrome、Edge 浏览器 Cookie</li>
<li>如果开启保存作品数据至文件功能，作品数据默认储存至 <code>./Download/ExploreData.db</code> 文件</li>
<li>程序下载记录数据储存至 <code>./ExploreID.db</code> 文件</li>
</ul>
<h1 id="user-scripts">🕹 用户脚本</h1>
<p>如果您的浏览器安装了 <a href="https://www.tampermonkey.net/">Tampermonkey</a> 浏览器扩展程序，可以添加 <a href="https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js">用户脚本</a>(右键单击复制链接)，无需下载安装即可体验项目功能！</p>
<img src="static/screenshot/脚本安装教程.png" alt="">
<hr>
<img src="static/screenshot/用户脚本截图1.png" alt="">
<hr>
<img src="static/screenshot/用户脚本截图2.png" alt="">
<hr>
<img src="static/screenshot/用户脚本截图3.png" alt="">
<p>提示：使用 XHS-Downloader 用户脚本批量提取作品链接，搭配 XHS-Downloader 程序可以实现批量下载无水印作品文件！</p>
<h2>📜 脚本说明</h2>
<ul>
<li>下载小红书无水印作品文件时，脚本需要花费时间处理文件，请等待片刻，请勿多次点击下载按钮</li>
<li>无水印图片文件为 PNG 格式；无水印视频文件较大，可能需要较长的时间处理，页面跳转可能会导致下载失败</li>
<li>提取账号发布、收藏、点赞、专辑作品链接时，脚本可以自动滚动页面直至加载全部作品</li>
<li>提取推荐作品链接、搜索作品、用户链接时，脚本可以自动滚动指定次数加载更多内容，默认滚动次数：50 次</li>
<li>自动滚动页面功能默认关闭；用户可以自由开启，并修改滚动页面次数，修改后立即生效</li>
<li>如果未开启自动滚动页面功能，用户需要手动滚动页面以便加载更多内容后再进行其他操作</li>
<li>支持作品文件打包下载；该功能默认开启，多个文件的作品将会以压缩包格式下载</li>
<li>使用全局代理工具可能会导致脚本下载文件失败，如有异常，请尝试关闭代理工具，必要时向作者反馈</li>
<li>XHS-Downloader 用户脚本仅实现可见即可得的数据采集功能，无任何收费功能和破解功能</li>
</ul>
<p><strong>自动滚动页面功能代码已重构，该功能默认关闭！启用该功能可能会被小红书检测为自动化操作，从而导致账号受到风控或封禁风险！</strong></p>
<h1>💻 二次开发</h1>
<p>如果有其他需求，可以根据 <code>example.py</code> 的注释提示进行代码调用或修改！</p>
<pre>
async def example():
    """通过代码设置参数，适合二次开发"""
    # 示例链接
    demo_link = "https://www.xiaohongshu.com/explore/XXX?xsec_token=XXX"

    # 实例对象
    work_path = "D:\\"  # 作品数据/文件保存根路径，默认值：项目根路径
    folder_name = "Download"  # 作品文件储存文件夹名称（自动创建），默认值：Download
    name_format = "作品标题 作品描述"
    user_agent = ""  # User-Agent
    cookie = ""  # 小红书网页版 Cookie，无需登录，可选参数，登录状态对数据采集有影响
    proxy = None  # 网络代理
    timeout = 5  # 请求数据超时限制，单位：秒，默认值：10
    chunk = 1024 * 1024 * 10  # 下载文件时，每次从服务器获取的数据块大小，单位：字节
    max_retry = 2  # 请求数据失败时，重试的最大次数，单位：秒，默认值：5
    record_data = False  # 是否保存作品数据至文件
    image_format = "WEBP"  # 图文作品文件下载格式，支持：AUTO、PNG、WEBP、JPEG、HEIC
    folder_mode = False  # 是否将每个作品的文件储存至单独的文件夹
    image_download = True  # 图文作品文件下载开关
    video_download = True  # 视频作品文件下载开关
    live_download = False  # 图文动图文件下载开关
    download_record = True  # 是否记录下载成功的作品 ID
    language = "zh_CN"  # 设置程序提示语言
    author_archive = True  # 是否将每个作者的作品存至单独的文件夹
    write_mtime = True  # 是否将作品文件的 修改时间 修改为作品的发布时间
    read_cookie = None  # 读取浏览器 Cookie，支持设置浏览器名称（字符串）或者浏览器序号（整数），设置为 None 代表不读取

    # async with XHS() as xhs:
    #     pass  # 使用默认参数

    async with XHS(
        work_path=work_path,
        folder_name=folder_name,
        name_format=name_format,
        user_agent=user_agent,
        cookie=cookie,
        proxy=proxy,
        timeout=timeout,
        chunk=chunk,
        max_retry=max_retry,
        record_data=record_data,
        image_format=image_format,
        folder_mode=folder_mode,
        image_download=image_download,
        video_download=video_download,
        live_download=live_download,
        download_record=download_record,
        language=language,
        read_cookie=read_cookie,
        author_archive=author_archive,
        write_mtime=write_mtime,
    ) as xhs:  # 使用自定义参数
        download = True  # 是否下载作品文件，默认值：False
        # 返回作品详细信息，包括下载地址
        # 获取数据失败时返回空字典
        print(
            await xhs.extract(
                demo_link,
                download,
                index=[
                    1,
                    2,
                    5,
                ],
            )
        )
</pre>
<h1>📋 读取剪贴板</h1>
<p>项目使用 <code>pyperclip</code> 实现读取剪贴板功能，该模块在不同的系统上会有差异。</p>
<p>在 Windows 上，不需要额外的模块。</p>
<p>在 Mac 上，该模块使用 pbcopy 和 pbpaste 命令，这些命令应该随操作系统一起提供。</p>
<p>在 Linux 上，该模块使用 xclip 或 xsel 命令，这些命令应该随操作系统一起提供。否则，请运行 "sudo apt-get install xclip" 或 "sudo apt-get install xsel"（注意：xsel 似乎并不总是有效）</p>
<p>在其他 Linux 系统上，你需要安装 qtpy 或 PyQT5 模块。</p>
<h1>⚙️ 配置文件</h1>
<p>项目根目录下的 <code>settings.json</code> 文件，首次运行自动生成，可以自定义部分运行参数。</p>
<p>如果设置了无效的参数值，程序将会使用参数默认值！</p>
<table>
<thead>
<tr>
<th align="center">参数</th>
<th align="center">类型</th>
<th align="center">含义</th>
<th align="center">默认值</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">mapping_data</td>
<td align="center">str: str</td>
<td align="center"><sup><a href="#author_archive">#</a></sup>作者别名映射表，格式：<code>作者ID: 作者别名</code></td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">work_path</td>
<td align="center">str</td>
<td align="center">作品数据 / 文件保存根路径</td>
<td align="center">项目根路径</td>
</tr>
<tr>
<td align="center">folder_name</td>
<td align="center">str</td>
<td align="center">作品文件储存文件夹名称</td>
<td align="center">Download</td>
</tr>
<tr>
<td align="center">name_format</td>
<td align="center">str</td>
<td align="center">作品文件名称格式，字段之间使用空格分隔，支持字段：<code>收藏数量</code>、<code>评论数量</code>、<code>分享数量</code>、<code>点赞数量</code>、<code>作品标签</code>、<code>作品ID</code>、<code>作品标题</code>、<code>作品描述</code>、<code>作品类型</code>、<code>发布时间</code>、<code>最后更新时间</code>、<code>作者昵称</code>、<code>作者ID</code></td>
<td align="center"><code>发布时间 作者昵称 作品标题</code></td>
</tr>
<tr>
<td align="center">user_agent</td>
<td align="center">str</td>
<td align="center">浏览器 User Agent</td>
<td align="center">内置 Chrome User Agent</td>
</tr>
<tr>
<td align="center">cookie</td>
<td align="center">str</td>
<td align="center">小红书网页版 Cookie，<b>无需登录，非必需参数！</b></td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">proxy</td>
<td align="center">str</td>
<td align="center">设置程序代理</td>
<td align="center">null</td>
</tr>
<tr>
<td align="center">timeout</td>
<td align="center">int</td>
<td align="center">请求数据超时限制，单位：秒</td>
<td align="center">10</td>
</tr>
<tr>
<td align="center">chunk</td>
<td align="center">int</td>
<td align="center">下载文件时，每次从服务器获取的数据块大小，单位：字节</td>
<td align="center">2097152(2 MB)</td>
</tr>
<tr>
<td align="center">max_retry</td>
<td align="center">int</td>
<td align="center">请求数据失败时，重试的最大次数，单位：秒</td>
<td align="center">5</td>
</tr>
<tr>
<td align="center">record_data</td>
<td align="center">bool</td>
<td align="center">是否保存作品数据至文件，保存格式：<code>SQLite</code></td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">image_format</td>
<td align="center">str</td>
<td align="center">图文作品文件下载格式，支持：<code>AUTO</code>、<code>PNG</code>、<code>WEBP</code>、<code>JPEG</code>、<code>HEIC</code><br><strong>部分作品没有 <code>HEIC</code> 格式的文件，此时下载的文件可能为 <code>WEBP</code> 格式！</strong><br><strong>设置为 <code>AUTO</code> 时表示动态格式，实际格式取决于服务器响应数据！</strong></td>
<td align="center">PNG</td>
</tr>
<tr>
<td align="center">image_download</td>
<td align="center">bool</td>
<td align="center">图文作品文件下载开关</td>
<td align="center">true</td>
</tr>
<tr>
<td align="center">video_download</td>
<td align="center">bool</td>
<td align="center">视频作品文件下载开关</td>
<td align="center">true</td>
</tr>
<tr>
<td align="center">live_download</td>
<td align="center">bool</td>
<td align="center">图文动图文件下载开关</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">folder_mode</td>
<td align="center">bool</td>
<td align="center">是否将每个作品的文件储存至单独的文件夹；文件夹名称与文件名称保持一致</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">download_record</td>
<td align="center">bool</td>
<td align="center">是否记录下载成功的作品 ID，如果开启，程序将会自动跳过下载存在记录的作品</td>
<td align="center">true</td>
</tr>
<tr>
<td align="center">author_archive</td>
<td align="center">bool</td>
<td align="center"><sup><a href="#author_archive">#</a></sup>是否将每个作者的作品储存至单独的文件夹；文件夹名称为 <code>作者ID_作者昵称</code></td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">write_mtime</td>
<td align="center">bool</td>
<td align="center">是否将作品文件的 <code>修改时间</code> 属性修改为作品的发布时间</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">language</td>
<td align="center">str</td>
<td align="center">设置程序语言，目前支持：<code>zh_CN</code>、<code>en_US</code></td>
<td align="center">zh_CN</td>
</tr>
</tbody>
</table>
<hr>
<div id="author_archive">
<p>如果 <code>author_archive</code> 参数设置为 <code>true</code>，程序会把每个作者的作品储存至单独的文件夹；当作者的昵称发生变化时，程序会自动更新已下载作品文件名称中的作者昵称部分！</p>
<p>除此之外，你还可以通过设置 <code>mapping_data</code> 参数为某个作者设置别名；如果对某个作者设置了别名，程序会使用你设置的作者别名去替代作者昵称！</p>
</div>
<hr>
<p><b>其他说明：<code>user_agent</code>参数获取示例；强烈建议根据实际浏览器信息进行设置！</b></p>
<img src="static/screenshot/请求头示例图.png" alt="">
<h1>🌐 Cookie</h1>
<p><code>2.2</code> 版本开始，项目功能无异常的情况下，无需额外处理 Cookie！</p>
<ol>
<li>打开浏览器（可选无痕模式启动），访问 <code>https://www.xiaohongshu.com/explore</code></li>
<li>登录小红书账号（可跳过）</li>
<li>按下 <code>F12</code> 打开开发人员工具</li>
<li>选择 <code>网络</code> 选项卡</li>
<li>勾选 <code>保留日志</code></li>
<li>在 <code>过滤</code> 输入框输入 <code>cookie-name:web_session</code></li>
<li>选择 <code>Fetch/XHR</code> 筛选器</li>
<li>点击小红书页面任意作品</li>
<li>在 <code>网络</code> 选项卡选择任意数据包（如果无数据包，重复步骤7）</li>
<li>全选复制 Cookie 写入程序或配置文件</li>
</ol>
<br>
<img src="static/screenshot/获取Cookie示意图.png" alt="">
<h1>🗳 下载记录</h1>
<p>XHS-Downloader 会将下载过的作品 ID 储存至数据库，当重复下载相同的作品时，XHS-Downloader 会自动跳过该作品的文件下载（即使作品文件不存在），如果想要重新下载作品文件，请先删除数据库中对应的作品 ID，再使用 XHS-Downloader 下载作品文件！</p>
<p>该功能默认开启，如果关闭该功能，XHS-Downloader 会检查文件是否存在，若文件存在则跳过下载！</p>

# 📦 构建可执行文件指南

本指南将引导您通过 Fork 本仓库并执行 GitHub Actions 自动完成基于最新源码的程序构建和打包！

---

## 使用步骤

### 1. Fork 本仓库

1. 点击项目仓库右上角的 **Fork** 按钮，将本仓库 Fork 到您的个人 GitHub 账户中
2. 您的 Fork 仓库地址将类似于：`https://github.com/your-username/this-repo`

---

### 2. 启用 GitHub Actions

1. 前往您 Fork 的仓库页面
2. 点击顶部的 **Settings** 选项卡
3. 点击右侧的 **Actions** 选项卡
4. 点击 **General** 选项
5. 在 **Actions permissions** 下，选择 **Allow all actions and reusable workflows** 选项，点击 **Save** 按钮

---

### 3. 手动触发打包流程

1. 在您 Fork 的仓库中，点击顶部的 **Actions** 选项卡
2. 找到名为 **构建可执行文件** 的工作流
3. 点击右侧的 **Run workflow** 按钮：
    - 选择 **master** 或者 **develop** 分支
    - 点击 **Run workflow**

---

### 4. 查看打包进度

1. 在 **Actions** 页面中，您可以看到触发的工作流运行记录
2. 点击运行记录，查看详细的日志以了解打包进度和状态

---

### 5. 下载打包结果

1. 打包完成后，进入对应的运行记录页面
2. 在页面底部的 **Artifacts** 部分，您将看到打包的结果文件
3. 点击下载并保存到本地，即可获得打包好的程序

---

## 注意事项

1. **资源使用**：
    - Actions 的运行环境由 GitHub 免费提供，普通用户每月有一定的免费使用额度（2000 分钟）

2. **代码修改**：
    - 您可以自由修改 Fork 仓库中的代码以定制程序打包流程
    - 修改后重新触发打包流程，您将得到自定义的构建版本

3. **与主仓库保持同步**：
    - 如果主仓库更新了代码或工作流，建议您定期同步 Fork 仓库以获取最新功能和修复

---

## Actions 常见问题

### Q1: 为什么我无法触发工作流？

A: 请确认您已按照步骤 **启用 Actions**，否则 GitHub 会禁止运行工作流

### Q2: 打包流程失败怎么办？

A:

- 检查运行日志，了解失败原因
- 确保代码没有语法错误或依赖问题
- 如果问题仍未解决，可以在本仓库的 [Issues 页面](https://github.com/JoeanAmier/XHS-Downloader/issues) 提出问题

### Q3: 我可以直接使用主仓库的 Actions 吗？

A: 由于权限限制，您无法直接触发主仓库的 Actions。请通过 Fork 仓库的方式执行打包流程

<h1>♥️ 支持项目</h1>
<p>如果 <b>XHS-Downloader</b> 对您有帮助，请考虑为它点个 <b>Star</b> ⭐，感谢您的支持！</p>
<table>
<thead>
<tr>
<th align="center">微信(WeChat)</th>
<th align="center">支付宝(Alipay)</th>
</tr>
</thead>
<tbody><tr>
<td align="center"><img src="./static/微信赞助二维码.png" alt="微信赞助二维码" height="200" width="200"></td>
<td align="center"><img src="./static/支付宝赞助二维码.png" alt="支付宝赞助二维码" height="200" width="200"></td>
</tr>
</tbody>
</table>
<p>如果您愿意，可以考虑提供资助为 <b>XHS-Downloader</b> 提供额外的支持！</p>
<h1>🌟 贡献指南</h1>
<p><strong>欢迎对本项目做出贡献！为了保持代码库的整洁、高效和易于维护，请仔细阅读以下指南，以确保您的贡献能够顺利被接受和整合。</strong></p>
<ul>
<li>在开始开发前，请从 <code>develop</code> 分支拉取最新的代码，以此为基础进行修改；这有助于避免合并冲突并保证您的改动基于最新的项目状态。</li>
<li>如果您的更改涉及多个不相关的功能或问题，请将它们分成多个独立的提交或拉取请求。</li>
<li>每个拉取请求应尽可能专注于单一功能或修复，以便于代码审查和测试。</li>
<li>遵循现有的代码风格；请确保您的代码与项目中已有的代码风格保持一致；建议使用 Ruff 工具保持代码格式规范。</li>
<li>编写可读性强的代码；添加适当的注释帮助他人理解您的意图。</li>
<li>每个提交都应该包含一个清晰、简洁的提交信息，以描述所做的更改。提交信息应遵循以下格式：<code>&lt;类型&gt;: &lt;简短描述&gt;</code></li>
<li>当您准备提交拉取请求时，请优先将它们提交到 <code>develop</code> 分支；这是为了给维护者一个缓冲区，在最终合并到 <code>master</code>
分支之前进行额外的测试和审查。</li>
</ul>
<p><strong>参考资料：</strong></p>
<ul>
<li><a href="https://www.contributor-covenant.org/zh-cn/version/2/1/code_of_conduct/">贡献者公约</a></li>
<li><a href="https://opensource.guide/zh-hans/how-to-contribute/">如何为开源做贡献</a></li>
</ul>
<h1>✉️ 联系作者</h1>
<ul>
<li>作者邮箱：yonglelolu@foxmail.com</li>
<li>作者微信: Downloader_Tools</li>
<li>微信公众号: Downloader Tools</li>
<li><b>Discord 社区</b>: <a href="https://discord.com/invite/ZYtmgKud9Y">点击加入社区</a></li>
<li>QQ 群聊: <a href="https://github.com/JoeanAmier/XHS-Downloader/blob/master/static/QQ%E7%BE%A4%E8%81%8A%E4%BA%8C%E7%BB%B4%E7%A0%81.png">扫码加入群聊</a></li>
</ul>
<p><b>说明：</b>QQ 群聊仅限于讨论项目使用问题，严禁发布任何广告，严禁讨论任何账号交易、账号流量、流量变现、灰色产业等相关的内容！</p>
<p>✨ <b>作者的其他开源项目：</b></p>
<ul>
<li><b>TikTokDownloader（抖音、TikTok）</b>：<a href="https://github.com/JoeanAmier/TikTokDownloader">https://github.com/JoeanAmier/TikTokDownloader</a></li>
<li><b>KS-Downloader（快手、KuaiShou）</b>：<a href="https://github.com/JoeanAmier/KS-Downloader">https://github.com/JoeanAmier/KS-Downloader</a></li>
</ul>

# 💰 项目赞助

## JetBrains 工具

![PyCharm logo](https://resources.jetbrains.com/storage/products/company/brand/logos/PyCharm.svg)

**JetBrains** 支持全球开源社区认可的活跃项目，并为非商业开发提供免费许可证。

***

## TikHub

<img src="static/赞助商_TikHub_Logo.png" alt="TikHub">
<p><a href="https://tikhub.io/">TikHub</a> 是一家领先的数据接口服务供应商，专注于提供高质量的数据接口，涵盖了多个热门平台，包括 抖音、TikTok、小红书、Instagram、Twitter 和 快手 等平台。</p>
<p>TikHub 还提供定制化的服务，如直播间监控、作品监控和达人监控，以满足不同业务场景的需求。</p>
<p>通过每日签到，用户可以免费获取一定额度的使用量；可以使用我的 <strong>推荐链接</strong>：<a href="https://user.tikhub.io/users/signup?referral_code=ZrdH8McC">https://user.tikhub.io/users/signup?referral_code=ZrdH8McC</a> 或 <strong>推荐码</strong>：<code>ZrdH8McC</code>，注册并充值即可获得 <code>$2</code> 额度！</p>
<p><a href="https://tikhub.io/">TikHub</a> 提供以下服务：</p>
<ul>
<li>丰富的数据接口</li>
<li>每日签到免费获取额度</li>
<li>高质量的 API 服务</li>
<li>官网：<a href="https://tikhub.io/">https://tikhub.io/</a></li>
<li>用户登陆地址：<a href="https://user.tikhub.io/">https://user.tikhub.io/</a></li>
</ul>
<h1>⚠️ 免责声明</h1>
<ul>
<li>使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项目所产生的任何损失、责任、或风险概不负责。</li>
<li>本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者尽力确保代码的正确性和安全性，但不保证代码完全没有错误或缺陷。</li>
<li>使用者在使用本项目时必须严格遵守 <a href="https://github.com/JoeanAmier/XHS-Downloader/blob/master/LICENSE">GNU
    General Public License v3.0</a> 的要求，并在适当的地方注明使用了 <a
        href="https://github.com/JoeanAmier/XHS-Downloader/blob/master/LICENSE">GNU General Public License
    v3.0</a> 的代码。
</li>
<li>使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。</li>
<li>使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。</li>
<li>本项目的作者不会提供 XHS-Downloader 项目的付费版本，也不会提供与 XHS-Downloader 项目相关的任何商业服务。</li>
<li>基于本项目进行的任何二次开发、修改或编译的程序与原创作者无关，原创作者不承担与二次开发行为或其结果相关的任何责任，使用者应自行对因二次开发可能带来的各种情况负全部责任。</li>
</ul>
<b>在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声明有任何疑问或不同意，请不要使用本项目的代码和功能。如果您使用了本项目的代码和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险和后果。</b>

# 💡 项目参考

* https://github.com/encode/httpx/
* https://github.com/tiangolo/fastapi
* https://github.com/textualize/textual/
* https://github.com/omnilib/aiosqlite
* https://github.com/thewh1teagle/rookie
* https://github.com/carpedm20/emoji/
* https://github.com/asweigart/pyperclip
* https://github.com/lxml/lxml
* https://github.com/yaml/pyyaml
* https://github.com/pallets/click/
* https://github.com/encode/uvicorn
* https://github.com/Tinche/aiofiles

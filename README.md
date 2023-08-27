<div align="center">
<img src="static/XHS_Downloader.png" alt="TikTokDownloader" height="256" width="256"><br>
<h1>小红书作品采集工具</h1>
</div>
<p>采集小红书图文/视频作品信息，提取图片/视频下载地址，下载图片/视频。</p>
<h1>使用示例</h1>
<pre>
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
cookie = ""  # 小红书网页 cookie，获取数据失败时可以尝试手动设置
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
</pre>
<h1>免责声明</h1>
<ul>
    <li>
        使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项目所产生的任何损失、责任、或风险概不负责。
    </li>
    <li>
        本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者尽力确保代码的正确性和安全性，但不保证代码完全没有错误或缺陷。
    </li>
    <li>使用者在使用本项目时必须严格遵守 <a href="https://github.com/JoeanAmier/XHS_Downloader/blob/master/LICENSE">GNU
        General Public License v3.0</a> 的要求，并在适当的地方注明使用了 <a
            href="https://github.com/JoeanAmier/XHS_Downloader/blob/master/LICENSE">GNU General Public License
        v3.0</a> 的代码。
    </li>
    <li>
        使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。
    </li>
    <li>
        使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。
    </li>
</ul>
<b>在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声明有任何疑问或不同意，请不要使用本项目的代码和功能。如果您使用了本项目的代码和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险和后果。</b>

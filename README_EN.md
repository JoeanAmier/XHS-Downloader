<div align="center">
<img src="static/XHS-Downloader.png" alt="" height="256" width="256"><br>
<h1>XHS-Downloader</h1>
<p><a href="README.md">简体中文</a> | English</p>
<img alt="GitHub" src="https://img.shields.io/github/license/JoeanAmier/XHS-Downloader?style=for-the-badge&color=ff7a45">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/JoeanAmier/XHS-Downloader?style=for-the-badge&color=9254de">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/JoeanAmier/XHS-Downloader?style=for-the-badge&color=ff7875">
<img alt="Static Badge" src="https://img.shields.io/badge/UserScript-ffec3d?style=for-the-badge&logo=tampermonkey&logoColor=%2300485B">
<br>
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/JoeanAmier/XHS-Downloader?style=for-the-badge&color=73d13d">
<img alt="GitHub release (with filter)" src="https://img.shields.io/github/v/release/JoeanAmier/XHS-Downloader?style=for-the-badge&color=40a9ff">
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/JoeanAmier/XHS-Downloader/total?style=for-the-badge&color=f759ab">
</div>
<br>
<div align="center">
<p>🔥 <b>Xiaohongshu Artwork Collection Tool</b>: Collect information on Xiaohongshu artworks; Extract the download address of Xiaohongshu artworks; Download the Xiaohongshu watermark-free artwork files!</p>
<p>❤️ The author only releases XHS-Downloader on GitHub, without collaborating with any individuals or websites. Additionally, there are no charging plans for the tool!</p>
</div>
<h1>📑 The Project Features:</h1>
<ul>
<li>✅ Collect Xiaohongshu graphic/text or video artworks' information</li>
<li>✅ Extract Xiaohongshu graphic/text or video artworks' download addresses</li>
<li>✅ Download Xiaohongshu graphic/text or video artworks without watermarks</li>
<li>✅ Supports Tampermonkey user scripts</li>
<li>✅ Batch download account artworks (with user scripts)</li>
<li>✅ Automatically skip already downloaded artworks</li>
<li>✅ Mechanism for handling the integrity of artwork files</li>
<li>✅ Customize the download format for graphic and text artworks</li>
<li>✅ Persistently store artwork information to a file</li>
<li>✅ Store artwork files in a separate folder</li>
<li>☑️ Background monitoring of clipboard for downloading artworks</li>
<li>☑️ Supports API calling functionality</li>
</ul>
<h1>📸 Program Screenshot</h1>
<br>
<p><b>🎥 Click on the image to watch the demo video</b></p>
<a href="https://www.bilibili.com/video/BV1nQ4y137it/"><img src="static/screenshot/程序运行截图EN1.png" alt=""></a>
<hr>
<a href="https://www.bilibili.com/video/BV1nQ4y137it/"><img src="static/screenshot/程序运行截图EN2.png" alt=""></a>
<h1>🔗 Support Hyperlinks</h1>
<ul>
<li><code>https://www.xiaohongshu.com/explore/artwork's ID</code></li>
<li><code>https://www.xiaohongshu.com/discovery/item/artwork's ID</code></li>
<li><code>https://xhslink.com/share code</code></li>
<br/>
<p><b>The program supports entering multiple artwork links in a single input box, separated by spaces.</b></p>
</ul>
<h1>🪟 About the Terminal</h1>
<p>⭐ <a href="https://learn.microsoft.com/zh-cn/windows/terminal/install">Windows Terminal</a> (Default terminal in Windows 11) is recommended to run the program for optimal display performance!</p>
<h1>🥣 How to Use</h1>
<p>If you only need to download watermark-free artwork files, <b>Program Running</b> is recommended; If you have other needs, <b>Source Code Running</b> is recommended!</p>
<h2>🖱 Program Running</h2>
<p>Users with Windows 10 or above can go to <a href="https://github.com/JoeanAmier/XHS-Downloader/releases/latest">Releases</a> download the program zip file, unzip it, open the program folder, and double-click <code>main.exe</code> to run the program</p>
<p>If you use the program this way, the default download path for files is: <code>.\_internal\Download</code>; configuration file path: <code>.\_internal\settings.json</code></p>
<h2>⌨️ Source Code Running</h2>
<ol>
<li>Install Python Interpreter with version >= <code>3.12</code></li>
<li>Execute <code>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt</code> to install the required modules for the program</li>
<li>Download the latest source code or code released in <a href="https://github.com/JoeanAmier/XHS-Downloader/releases/latest">Releases</a> to your local workplace</li>
<li>Run <code>main.py</code> to use the program</li>
</ol>
<h1>🕹 User Script</h1>
<p>If your browser has installed <a href="https://www.tampermonkey.net/">Tampermonkey</a> extension, add <a href="https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js">User script</a>, and you can experience the project's functionalities without downloading the program!</p>
<p>Tip: You can use the XHS-Downloader user script to extract artwork links in batches from web pages. Combine it with the XHS-Downloader program to achieve batch downloading of watermark-free artwork files!</p>
<h2>Script Functionality</h2>
<ul>
<li>Download Xiaohongshu watermark-free artwork files</li>
<li>Extract artwork links from the discovery page</li>
<li>Extract artwork links from account-published content</li>
<li>Extract artwork links from account-collected content</li>
<li>Extract artwork links from account-liked content</li>
</ul>
<h2>Script Screenshot</h2>
<img src="static/screenshot/用户脚本截图1.png" alt="">
<hr>
<img src="static/screenshot/用户脚本截图2.png" alt="">
<h1>💻 Secondary Development</h1>
<p>If there are other requirements, you can call or modify the program refer to the comments in <code>main.py</code></p>
<pre>
# Example links
error_link = "https://github.com/JoeanAmier/XHS_Downloader"
demo_link = "https://www.xiaohongshu.com/explore/xxxxxxxxxx"
multiple_links = f"{demo_link} {demo_link} {demo_link}"
# Instance object
work_path = "D:\\"  # Artwork data/file save root path, default value: project root path
folder_name = "Download"  # Artwork file storage folder name (automatically created), default value: Download
user_agent = ""  # Request Header: User-Agent
cookie = ""  # Xiaohongshu web version Cookie, no need to log in
proxy = None  # Network proxy
timeout = 5  # Request data timeout limit, unit: seconds, default value: 10
chunk = 1024 * 1024 * 10  # When downloading files, the size of each data block obtained from the server each time, unit: bytes
max_retry = 2  # Maximum number of retries when requesting data fails, unit: seconds, default value: 5
record_data = False  # Whether to record artwork data to a file
image_format = "WEBP"  # Graphic artwork file download format, supports: PNG, WEBP
folder_mode = False  # Whether to store each artwork's file in a separate folder
async with XHS() as xhs:
    pass  # Use default parameters
async with XHS(work_path=work_path,
               folder_name=folder_name,
               user_agent=user_agent,
               cookie=cookie,
               proxy=proxy,
               timeout=timeout,
               chunk=chunk,
               max_retry=max_retry,
               record_data=record_data,
               image_format=image_format,
               folder_mode=folder_mode,
               ) as xhs:  # Use custom parameters
    download = True  # Whether to download artwork files, default value: False
    # Return detailed information about the artwork, including download addresses
    print(await xhs.extract(error_link, download))  # Return an empty dictionary when data retrieval fails
    print(await xhs.extract(demo_link, download))
    print(await xhs.extract(multiple_links, download))  # Support input of multiple artwork links
</pre>
<h1>⚙️ Configuration File</h1>
<p><code>settings.json</code> in the project's root directory, generated automatically on the first run, and allows customization of certain runtime parameters</p>
<p>If your computer doesn't have a suitable program to edit JSON files, it is recommended to use <a href="https://try8.cn/tool/format/json">JSON Online Tool</a> to edit the content of the configuration file</p>
<table>
<thead>
<tr>
<th align="center">Parameters</th>
<th align="center">Type</th>
<th align="center">Meaning</th>
<th align="center">Default Value</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">work_path</td>
<td align="center">str</td>
<td align="center">Artwork data/file save root path</td>
<td align="center">Project root path</td>
</tr>
<tr>
<td align="center">folder_name</td>
<td align="center">str</td>
<td align="center">Artwork file storage folder name</td>
<td align="center">Download</td>
</tr>
<tr>
<td align="center">user_agent</td>
<td align="center">str</td>
<td align="center">Request Header: User-Agent</td>
<td align="center">Default UA</td>
</tr>
<tr>
<td align="center">cookie</td>
<td align="center">str</td>
<td align="center">Xiaohongshu web version Cookie，<b>No need to log in, modification recommended</b></td>
<td align="center">Default Cookie</td>
</tr>
<tr>
<td align="center">proxy</td>
<td align="center">str</td>
<td align="center">Set program proxy</td>
<td align="center">null</td>
</tr>
<tr>
<td align="center">timeout</td>
<td align="center">int</td>
<td align="center">Request data timeout limit, unit: seconds</td>
<td align="center">10</td>
</tr>
<tr>
<td align="center">chunk</td>
<td align="center">int</td>
<td align="center">Size of each data block obtained from the server when downloading files, unit: bytes</td>
<td align="center">1048576(1 MB)</td>
</tr>
<tr>
<td align="center">max_retry</td>
<td align="center">int</td>
<td align="center">Maximum number of retries when requesting data fails, unit: seconds</td>
<td align="center">5</td>
</tr>
<tr>
<td align="center">record_data</td>
<td align="center">bool</td>
<td align="center">Whether to record artwork data to <code>TXT</code> file</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">image_format</td>
<td align="center">str</td>
<td align="center">Graphic and text artwork file download format, support: <code>PNG</code>、<code>WEBP</code></td>
<td align="center">PNG</td>
</tr>
<tr>
<td align="center">folder_mode</td>
<td align="center">bool</td>
<td align="center">Whether to store each artwork's file in a separate folder; folder names are consistent with file names</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">language</td>
<td align="center">str</td>
<td align="center">Set programming language, currently support: <code>zh-CN</code>, <code>en-GB</code></td>
<td align="center">zh-CN</td>
</tr>
</tbody>
</table>
<h1>🌐 Cookie</h1>
<ol>
<li>Open the browser (optional in incognito mode), visit any page on Xiaohongshu</li>
<li>Press <code>F12</code> to open developer tools</li>
<li>Click the <code>Console</code></li>
<li>Input <code>document.cookie</code> then press Enter to confirm</li>
<li>The output content is the Cookie</li>
</ol>
<br>
<img src="static/screenshot/获取Cookie示意图.png" alt="">
<h1>♥️ Support the Project</h1>
<p>If <b>XHS-Downloader</b> is helpful, please consider giving it a <b>Star</b> ⭐, thank you for your support!</p>
<table>
<thead>
<tr>
<th align="center">WeChat</th>
<th align="center">Alipay</th>
</tr>
</thead>
<tbody><tr>
<td align="center"><img src="./static/微信赞助二维码.png" alt="微信赞助二维码" height="200" width="200"></td>
<td align="center"><img src="./static/支付宝赞助二维码.png" alt="支付宝赞助二维码" height="200" width="200"></td>
</tr>
</tbody>
</table>
<p>If you wish, consider funding additional support for the <b>XHS-Downloader</b>!</p>
<h1>✉️ Contact us</h1>
<ul>
<li>QQ: 2437596031 (please inform intent)</li>
<li>QQ Group: <a href="https://github.com/JoeanAmier/XHS-Downloader/blob/master/static/QQ%E7%BE%A4%E8%81%8A%E4%BA%8C%E7%BB%B4%E7%A0%81.png">Click to obtain the group QR code</a></li>
<li>Email: yonglelolu@gmail.com</li>
</ul>
<p>
<b>If you contact me via email, I may not be able to check and respond promptly. I will do my best to reply to your email within seven days. If there are urgent matters or you need a faster response, please contact me through other means. Thank you for your understanding!</b>
</p>
<p><b>If you're interested in DouYin / TikTok, you can check out my other open-source project <a href="https://github.com/JoeanAmier/TikTokDownloader">TikTokDownloader</a></b></p>
<h1>⚠️ Disclaimer</h1>
<ul>
<li>Users decide on their own how to use this project and bear the risks themselves. The author is not responsible for any losses, liabilities, or risks incurred by users in the use of this project</li>
<li>The code and functionalities provided by the author of this project are developed based on existing knowledge and technology. The author strives to ensure the correctness and security of the code but does not guarantee that the code is completely error-free or defect-free.</li>
<li>Users must strictly adhere to the provisions in <a href="https://github.com/JoeanAmier/XHS-Downloader/blob/master/LICENSE">GNU
    General Public License v3.0</a> , and appropriately mention the use of code adhering <a
        href="https://github.com/JoeanAmier/XHS-Downloader/blob/master/LICENSE">GNU General Public License
    v3.0</a>.
</li>
<li>Under no circumstances shall users associate the author of this project, contributors, or other related parties with the user's usage behavior, or demand that they be held responsible for any losses or damages incurred by the user's use of this project.</li>
<li>Users must independently study relevant laws and regulations when using the code and functionalities of this project and ensure that their usage is legal and compliant. Users are solely responsible for any legal liability and risks resulting from violations of laws and regulations.</li>
<li>The author of this project will not provide a paid version of the XHS-Downloader project, nor will they offer any commercial services related to the XHS-Downloader project.</li>
<li>Any secondary development, modification, or compilation of the program based on this project is unrelated to the original author. The original author is not responsible for any consequences related to secondary development or its results. Users should take full responsibility for any situations that may arise from secondary development on their own.</li>
</ul>
<b>Before using the code and functionalities of this project, please carefully consider and accept the above disclaimer. If you have any questions or disagree with the statement, please do not use the code and functionalities of this project. If you use the code and functionalities of this project, it is considered that you fully understand and accept the above disclaimer, and willingly assume all risks and consequences associated with the use of this project.</b>

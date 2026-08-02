// ==UserScript==
// @name           XHS-Downloader
// @namespace      xhs_downloader
// @homepage       https://github.com/JoeanAmier/XHS-Downloader
// @version        2.4.4
// @tag            小红书
// @tag            RedNote
// @tag            XiaoHongShu
// @description    提取小红书作品/用户链接，下载小红书图文/视频作品文件
// @description:en Extract RedNote works/user links, Download images/videos files
// @author         JoeanAmier
// @match          http*://www.xiaohongshu.com/explore*
// @match          http*://www.xiaohongshu.com/discovery/item/*
// @match          http*://www.xiaohongshu.com/user/profile/*
// @match          http*://www.xiaohongshu.com/search_result*
// @match          http*://www.xiaohongshu.com/board/*
// @match          http*://www.rednote.com/explore*
// @match          http*://www.rednote.com/discovery/item/*
// @match          http*://www.rednote.com/user/profile/*
// @match          http*://www.rednote.com/search_result*
// @match          http*://www.rednote.com/board/*
// @icon64         data:image/png;base64,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
// @grant          GM_getValue
// @grant          GM_setValue
// @grant          unsafeWindow
// @grant          GM_setClipboard
// @grant          GM_registerMenuCommand
// @grant          GM_unregisterMenuCommand
// @license        GNU General Public License v3.0
// @run-at         document-end
// @updateURL      https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js
// @downloadURL    https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js
// @supportURL     https://github.com/JoeanAmier/XHS-Downloader/issues
// @require        https://cdnjs.cloudflare.com/ajax/libs/jszip/3.9.1/jszip.min.js
// ==/UserScript==

(function () {
    'use strict';

    const i18n = {
        'CN': {
            instructionsText: `功能清单：
1. 下载小红书作品文件
2. 提取推荐页面作品链接
3. 提取账号发布作品链接
4. 提取账号收藏作品链接
5. 提取账号专辑作品链接
6. 提取账号点赞作品链接
7. 提取搜索结果作品链接
8. 提取搜索结果用户链接

注意事项：
1. 下载小红书作品文件时，脚本需要花费时间处理文件，请等待片刻，请勿多次点击下载按钮
2. 提取账号发布、收藏、点赞、专辑作品链接时，脚本可以自动滚动页面直至加载全部作品
3. 提取推荐作品链接、搜索作品、用户链接时，脚本可以自动滚动指定次数加载更多内容，默认滚动次数：50 次
4. 自动滚动页面功能默认关闭；用户可以自由开启，并修改滚动页面次数，修改后立即生效
5. 如果未开启自动滚动页面功能，用户需要手动滚动页面以便加载更多内容后再进行其他操作
6. 支持作品文件打包下载；该功能默认开启，多个文件的作品将会以压缩包格式下载
7. 向服务器推送下载任务时，文件格式、名称规则等设置以服务器配置文件中的设置为准
8. 使用全局代理工具可能会导致脚本下载文件失败，如有异常，请尝试关闭代理工具，必要时向作者反馈
9. XHS-Downloader 用户脚本仅实现可见即可得的数据采集功能，无任何收费功能和破解功能

项目开源地址：https://github.com/JoeanAmier/XHS-Downloader
`,
            disclaimerText: `1. 使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项目所产生的任何损失、责任、或风险概不负责。
2. 本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者按现有技术水平努力确保代码的正确性和安全性，但不保证代码完全没有错误或缺陷。
3. 本项目依赖的所有第三方库、插件或服务各自遵循其原始开源或商业许可，使用者需自行查阅并遵守相应协议，作者不对第三方组件的稳定性、安全性及合规性承担任何责任。
4. 使用者在使用本项目时必须严格遵守 GNU General Public License v3.0 的要求，并在适当的地方注明使用了 GNU General Public License v3.0 的代码。
5. 使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。
6. 使用者不得使用本工具从事任何侵犯知识产权的行为，包括但不限于未经授权下载、传播受版权保护的内容，开发者不参与、不支持、不认可任何非法内容的获取或分发。
7. 本项目不对使用者涉及的数据收集、存储、传输等处理活动的合规性承担责任。使用者应自行遵守相关法律法规，确保处理行为合法正当；因违规操作导致的法律责任由使用者自行承担。
8. 使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。
9. 本项目的作者不会提供 XHS-Downloader 项目的付费版本，也不会提供与 XHS-Downloader 项目相关的任何商业服务。
10. 基于本项目进行的任何二次开发、修改或编译的程序与原创作者无关，原创作者不承担与二次开发行为或其结果相关的任何责任，使用者应自行对因二次开发可能带来的各种情况负全部责任。
11. 本项目不授予使用者任何专利许可；若使用本项目导致专利纠纷或侵权，使用者自行承担全部风险和责任。未经作者或权利人书面授权，不得使用本项目进行任何商业宣传、推广或再授权。
12. 作者保留随时终止向任何违反本声明的使用者提供服务的权利，并可能要求其销毁已获取的代码及衍生作品。
13. 作者保留在不另行通知的情况下更新本声明的权利，使用者持续使用即视为接受修订后的条款。

在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声明有任何疑问或不同意，请不要使用本项目的代码和功能。如果您使用了本项目的代码和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险和后果。
`,
            readmeTitle: 'XHS-Downloader 脚本说明',
            disclaimerTitle: 'XHS-Downloader 免责声明',
            disclaimerConfirm: '我已知晓',
            readmeMenuTitle: "阅读脚本说明和免责声明",
            switchToLanguageMenuText: "切换到中文",
            aboutText: `项目开源协议：GNU General Public License v3.0
项目开源地址：https://github.com/JoeanAmier/XHS-Downloader

如果 XHS-Downloader 对您有帮助，请考虑为它点个 Star ⭐，感谢您的支持！

✨ 作者的其他开源项目：

DouK-Downloader（抖音、DouYin、TikTok）：https://github.com/JoeanAmier/TikTokDownloader
KS-Downloader（快手、KuaiShou）：https://github.com/JoeanAmier/KS-Downloader

项目 Discord 社区：https://discord.com/invite/ZYtmgKud9Y
`,
            aboutTitle: '关于 XHS-Downloader',
            errorTitle: '发生异常',
            errorText: (text) => `${text}请向作者反馈！\n项目开源地址：https://github.com/JoeanAmier/XHS-Downloader`,
            imageExtractError: "解析图文作品数据发生异常！",
            downloadLinkError: "处理下载链接发生异常！",
            downloadTips: "正在下载文件，请稍等...",
            downloadError: "下载作品文件发生异常！",
            extractError: "读取作品数据发生异常！",
            linkExtractSuccess: '作品/用户链接已复制到剪贴板！',
            linkExtractError: "未提取到任何作品/用户链接！",
            videoDownloadError: "下载视频作品文件发生异常！",
            imageDownloadError: "下载图文作品文件发生异常！",
            signInPrompt: "提取作品链接失败！受平台限制，未登录状态下无法通过账号主页浏览作品详情！请登录后重试！",
            jsZipError: "XHS-Downloader 用户脚本依赖库 JSZip 加载失败，作品文件打包下载功能无法使用，请尝试刷新网页或者向作者反馈！",
            tipsTitle: '脚本提示',
            confirmButton: '确认',
            closeButton: '关闭',
            autoScrollLabel: '自动滚动页面',
            autoScrollDesc: '启用后，页面将根据规则自动滚动以便加载更多内容',
            filePackLabel: '文件打包下载',
            filePackDesc: '启用后，多个文件的作品将会以压缩包格式下载',
            scrollCountLabel: '自动滚动次数',
            scrollCountDesc: '自动滚动页面的次数（仅在启用自动滚动页面时可用）',
            linkCheckboxSwitchLabel: '链接提取选择模式',
            linkCheckboxSwitchDesc: '关闭后，提取作品链接时无需确认直接提取全部链接',
            imageCheckboxSwitchLabel: '图片下载选择模式',
            imageCheckboxSwitchDesc: '关闭后，下载图文作品时无需确认直接下载全部文件',
            keepMenuVisibleLabel: '菜单保持显示',
            keepMenuVisibleDesc: '启用后，功能菜单无需鼠标悬停始终保持显示',
            scriptServerURLLabel: 'WebSocket 服务器地址',
            scriptServerURLDesc: '用户脚本连接的 WebSocket 服务器',
            scriptServerSwitchLabel: '连接服务器',
            scriptServerSwitchDesc: '启用后，可以把作品下载任务推送至服务器',
            imageDownloadFormatLabel: '图片下载格式',
            imageDownloadFormatDesc: '图文作品文件下载格式',
            videoPreferenceLabel: '视频下载偏好',
            videoPreferenceDesc: '视频作品文件下载策略',
            videoPreferenceOptions: {
                manual: '手动选择',
                resolution: '分辨率优先',
                bitrate: '码率优先',
                size: '文件大小优先',
            },
            videoQualityTitle: '选择视频下载质量',
            videoQualityOriginal: '最高质量',
            videoQualityBitrate: '码率',
            videoQualityFps: '帧率',
            videoQualitySize: '大小',
            fileNameFormatLabel: '作品文件名称格式',
            fileNameFormatDesc: '点击可选字段添加，拖拽已选字段调整顺序',
            fileNameSelectedLabel: '已选字段',
            fileNameAvailableLabel: '可选字段',
            fileNameRemoveTip: '移除字段',
            fileNameKeyLabels: {
                "收藏数量": "收藏数量",
                "评论数量": "评论数量",
                "分享数量": "分享数量",
                "点赞数量": "点赞数量",
                "作品标签": "作品标签",
                "作品ID": "作品ID",
                "作品标题": "作品标题",
                "作品描述": "作品描述",
                "作品类型": "作品类型",
                "发布时间": "发布时间",
                "更新时间": "更新时间",
                "作者昵称": "作者昵称",
                "作者ID": "作者ID",
            },
            downloadSettingsGroup: '下载设置',
            extractSettingsGroup: '提取设置',
            displaySettingsGroup: '菜单设置',
            serverSettingsGroup: '服务器设置',
            saveSettingsButton: '保存设置',
            cancelSettingsButton: '放弃修改',
            selectAllButton: '全部选中',
            deselectAllButton: '全部取消',
            startDownloadButton: '开始下载',
            closeDownloadButton: '取消下载',
            imageSelectionTip: '请至少选择一张图片！',
            itemsExtractTip: '请选择需要提取的项目',
            itemsExtractConfirm: '提取链接',
            itemsExtractCancel: '放弃',
            extractRecommendLinksText: '提取推荐作品链接',
            extractRecommendLinksDescription: '提取推荐页面的作品链接至剪贴板',
            downloadNoteFilesText: '下载作品文件',
            downloadNoteFilesDescription: '下载当前作品文件',
            pushDownloadTaskText: '推送下载任务',
            pushDownloadTaskDescription: '向服务器发送下载请求',
            extractPublishedLinksText: '提取发布作品链接',
            extractPublishedLinksDescription: '提取账号发布作品链接至剪贴板',
            extractLikedLinksText: '提取点赞作品链接',
            extractLikedLinksDescription: '提取账号点赞作品链接至剪贴板',
            extractSavedLinksText: '提取收藏作品链接',
            extractSavedLinksDescription: '提取账号收藏作品链接至剪贴板',
            extractSearchNoteLinksText: '提取作品链接',
            extractSearchNoteLinksDescription: '提取搜索结果的作品链接至剪贴板',
            extractSearchUsersLinksText: '提取用户链接',
            extractSearchUsersLinksDescription: '提取搜索结果的用户链接至剪贴板',
            extractAlbumNotesLinksText: '提取专辑作品链接',
            extractAlbumNotesLinksDescription: '提取当前专辑的作品链接至剪贴板',
            modifyScriptSettingsText: '修改用户脚本设置',
            modifyScriptSettingsDescription: '修改用户脚本设置',
            aboutXHSText: '关于 XHS-Downloader',
            aboutXHSDescription: '查看 XHS-Downloader 更多信息',
            imageCheckboxTitle: '请选中需要下载的图片',
            scriptServerError: '脚本服务器连接出错，请检查网络连接或脚本服务器状态是否正常！',
            pushTaskError: '脚本服务器未连接，请检查网络连接或脚本服务器状态是否正常！',
            pushTaskSuccess: "已向服务器发送下载请求",
            resetIconPositionMenuText: '重置图标位置',
            resetIconPositionTip: '图标位置已重置',
            settingsTitle: '用户脚本设置',
            scriptInternalError: '脚本内部发生错误',
        }, 'EN': {
            instructionsText: `Features:
1. Download RedNote note files
2. Extract note links from the Recommendation page
3. Extract note links from an account's Published tab
4. Extract note links from an account's Collections tab
5. Extract note links from an account's Albums
6. Extract note links from an account's Liked tab
7. Extract note links from search results
8. Extract user links from search results

Notes:
1. When downloading note files, the script needs time to process. Please wait a moment and do not click the download button repeatedly.
2. When extracting links from Published, Collections, Liked, or Albums, the script can automatically scroll the page until all notes are loaded.
3. When extracting Recommendation, Search Notes, or User links, the script can automatically scroll a specified number of times. Default: 50 times.
4. Auto-scroll is disabled by default; users can enable it and modify the scroll count. Changes take effect immediately.
5. If auto-scroll is disabled, users must manually scroll the page to load more content before performing extractions.
6. Supports batch downloading (ZIP format); this feature is enabled by default. Notes with multiple files will be downloaded as a compressed package.
7. When pushing tasks to a server, settings such as file format and naming rules are determined by the server's configuration file.
8. Using global proxy tools may cause download failures. If issues occur, try disabling the proxy and provide feedback to the author if necessary.
9. The XHS-Downloader userscript only provides "what you see is what you get" data collection; it contains no paid features or decryption/cracking functions.

Open Source: https://github.com/JoeanAmier/XHS-Downloader
`,
            disclaimerText: `1. The use of this project is at the user's own discretion and risk. The author is not responsible for any loss, liability, or risk arising from its use.
2. The code and functions provided are based on existing knowledge and technology. While efforts are made to ensure correctness and security, the author does not guarantee that the code is entirely error-free.
3. All third-party libraries, plugins, or services relied upon by this project follow their own original open-source or commercial licenses. Users must consult and comply with those agreements.
4. Users must strictly adhere to the GNU General Public License v3.0 requirements and credit the use of GPL v3.0 code where appropriate.
5. Users must research relevant laws and regulations to ensure their use of this project is legal and compliant. Any legal liability arising from violations is borne solely by the user.
6. Users must not use this tool for any acts that infringe on intellectual property rights, including but not limited to unauthorized downloading or distribution of copyrighted content.
7. This project assumes no responsibility for the compliance of data collection, storage, or transmission activities performed by the user.
8. Under no circumstances shall the author or contributors be held liable for any damages or losses related to the user's actions.
9. The author will not provide a paid version of XHS-Downloader, nor any commercial services related to the project.
10. Any secondary development, modification, or compilation of this program is unrelated to the original author. The user is solely responsible for any consequences of such actions.
11. This project does not grant any patent licenses. The user assumes all risks regarding patent disputes. Commercial promotion or sub-licensing without written authorization is prohibited.
12. The author reserves the right to terminate service to any user violating this disclaimer and may request the destruction of obtained code.
13. The author reserves the right to update this disclaimer without notice. Continued use constitutes acceptance of the revised terms.

Before using this project, please carefully consider and accept the above disclaimer. If you have any doubts or disagree, do not use the code or functions. Use of the project implies full understanding and acceptance of these terms.
`,
            readmeTitle: 'XHS-Downloader Instructions',
            disclaimerTitle: 'XHS-Downloader Disclaimer',
            disclaimerConfirm: 'I acknowledge',
            readmeMenuTitle: "Read Instructions and Disclaimer",
            switchToLanguageMenuText: "Switch to English",
            aboutText: `License: GNU General Public License v3.0
GitHub: https://github.com/JoeanAmier/XHS-Downloader

If XHS-Downloader helps you, please consider giving it a Star ⭐. Thanks for your support!

✨ Other Projects by the Author:

DouK-Downloader (DouYin, TikTok): https://github.com/JoeanAmier/TikTokDownloader
KS-Downloader (KuaiShou): https://github.com/JoeanAmier/KS-Downloader

Discord Community: https://discord.com/invite/ZYtmgKud9Y
`,
            aboutTitle: 'About XHS-Downloader',
            errorTitle: 'Exception Occurred',
            errorText: (text) => `${text} Please report this to the author!\nGitHub: https://github.com/JoeanAmier/XHS-Downloader`,
            imageExtractError: "Error parsing image note data!",
            downloadLinkError: "Error processing download links!",
            downloadTips: "Downloading file, please wait...",
            downloadError: "Error downloading note files!",
            extractError: "Error reading note data!",
            linkExtractSuccess: 'Note/User links copied to clipboard!',
            linkExtractError: "No Note/User links extracted!",
            videoDownloadError: "Error downloading video note!",
            imageDownloadError: "Error downloading image note!",
            signInPrompt: "Failed to extract links! Due to platform restrictions, note details cannot be viewed via account pages without logging in. Please log in and try again!",
            jsZipError: "JSZip library failed to load. ZIP packaging is unavailable. Please refresh or contact the author!",
            tipsTitle: 'Script Tips',
            confirmButton: 'Confirm',
            closeButton: 'Close',
            autoScrollLabel: 'Auto-scroll Page',
            autoScrollDesc: 'When enabled, the page will automatically scroll to load more content',
            filePackLabel: 'Package Files for Download',
            filePackDesc: 'When enabled, notes with multiple files will be downloaded as a ZIP archive',
            scrollCountLabel: 'Auto-scroll Count',
            scrollCountDesc: 'Number of times to scroll (only active when Auto-scroll is enabled)',
            linkCheckboxSwitchLabel: 'Link Extraction Selection Mode',
            linkCheckboxSwitchDesc: 'If disabled, all links will be extracted immediately without confirmation',
            imageCheckboxSwitchLabel: 'Image Download Selection Mode',
            imageCheckboxSwitchDesc: 'If disabled, all images will be downloaded immediately without confirmation',
            keepMenuVisibleLabel: 'Keep Menu Visible',
            keepMenuVisibleDesc: 'When enabled, the menu stays visible without needing a mouse hover',
            scriptServerURLLabel: 'WebSocket Server URL',
            scriptServerURLDesc: 'The WebSocket server address the script connects to',
            scriptServerSwitchLabel: 'Connect to Server',
            scriptServerSwitchDesc: 'When enabled, download tasks can be pushed to the server',
            imageDownloadFormatLabel: 'Image Download Format',
            imageDownloadFormatDesc: 'Preferred file format for downloading images',
            videoPreferenceLabel: 'Video download preferences',
            videoPreferenceDesc: 'Video Notes File Download Strategy',
            videoPreferenceOptions: {
                manual: 'Manual select',
                resolution: 'Resolution priority',
                bitrate: 'Bitrate priority',
                size: 'File size priority',
            },
            videoQualityTitle: 'Select Video Download Quality',
            videoQualityOriginal: 'Highest quality',
            videoQualityBitrate: 'Bitrate',
            videoQualityFps: 'Frame rate',
            videoQualitySize: 'Size',
            fileNameFormatLabel: 'Note File Name Format',
            fileNameFormatDesc: 'Click available fields to add them. Drag selected fields to reorder.',
            fileNameSelectedLabel: 'Selected Fields',
            fileNameAvailableLabel: 'Available Fields',
            fileNameRemoveTip: 'Remove field',
            fileNameKeyLabels: {
                "收藏数量": "Favorite Count",
                "评论数量": "Comment Count",
                "分享数量": "Share Count",
                "点赞数量": "Like Count",
                "作品标签": "Note Tags",
                "作品ID": "Note ID",
                "作品标题": "Note Title",
                "作品描述": "Note Desc",
                "作品类型": "Note Type",
                "发布时间": "Publish Time",
                "更新时间": "Update Time",
                "作者昵称": "Nickname",
                "作者ID": "Author ID",
            },
            downloadSettingsGroup: 'Download Settings',
            extractSettingsGroup: 'Extraction Settings',
            displaySettingsGroup: 'Menu Settings',
            serverSettingsGroup: 'Server Settings',
            saveSettingsButton: 'Save Settings',
            cancelSettingsButton: 'Discard Changes',
            selectAllButton: 'Select All',
            deselectAllButton: 'Deselect All',
            startDownloadButton: 'Start Download',
            closeDownloadButton: 'Cancel Download',
            imageSelectionTip: 'Please select at least one image!',
            itemsExtractTip: 'Please select items to extract',
            itemsExtractConfirm: 'Extract Links',
            itemsExtractCancel: 'Cancel',
            extractRecommendLinksText: 'Extract Recommended Note Links',
            extractRecommendLinksDescription: '',
            downloadNoteFilesText: 'Download Note Files',
            downloadNoteFilesDescription: '',
            pushDownloadTaskText: 'Push Download Task',
            pushDownloadTaskDescription: 'Send download request to the server',
            extractPublishedLinksText: 'Extract Published Note Links',
            extractPublishedLinksDescription: '',
            extractLikedLinksText: 'Extract Liked Note Links',
            extractLikedLinksDescription: '',
            extractSavedLinksText: 'Extract Collected Note Links',
            extractSavedLinksDescription: '',
            extractSearchNoteLinksText: 'Extract Note Links',
            extractSearchNoteLinksDescription: 'Extract note links from search results',
            extractSearchUsersLinksText: 'Extract User Links',
            extractSearchUsersLinksDescription: 'Extract user links from search results',
            extractAlbumNotesLinksText: 'Extract Album Note Links',
            extractAlbumNotesLinksDescription: 'Extract note links from the current album',
            modifyScriptSettingsText: 'Modify Script Settings',
            modifyScriptSettingsDescription: '',
            aboutXHSText: 'About XHS-Downloader',
            aboutXHSDescription: '',
            imageCheckboxTitle: 'Please select images to download',
            scriptServerError: 'Server connection error. Please check your network or server status!',
            pushTaskError: 'Server not connected. Please check your network or server status!',
            pushTaskSuccess: "Download request sent to server successfully",
            resetIconPositionMenuText: 'Reset icon position',
            resetIconPositionTip: 'Icon position reset',
            settingsTitle: 'Script Settings',
            scriptInternalError: 'An internal error occurred in the script',
        },
    };

    let lang = GM_getValue("language", undefined);
    if (!lang) {
        lang = navigator.language.toLowerCase().includes('zh') ? 'CN' : 'EN';
        GM_setValue("language", lang);
    }

    let t = i18n[lang];

    const iconBase64 = "data:image/png;base64,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";

    const defaultsWebSocketURL = "ws://127.0.0.1:5558";
    const NAME_KEYS = [
        "收藏数量",
        "评论数量",
        "分享数量",
        "点赞数量",
        "作品标签",
        "作品ID",
        "作品标题",
        "作品描述",
        "作品类型",
        "发布时间",
        "更新时间",
        "作者昵称",
        "作者ID",
    ];
    const defaultFileNameFormatKeys = ["发布时间", "作者昵称", "作品标题"];
    const fileNameInvalidCharPattern = /[<>:"/\\|?*\x00-\x1F\x7F]/g;
    const fileNameBlankPattern = /\s+/g;
    const fileNameTrailingDotBlankPattern = /[. ]+$/g;
    const fileNameTopicMarkerPattern = /\[话题]#/g;
    const reservedFileNamePattern = /^(con|prn|aux|nul|com[1-9]|lpt[1-9])(\..*)?$/i;
    const fileNameDescriptionMaxLength = 64;
    const fileNameMaxLength = 128;

    // 解析文件名格式字段。
    const parseFileNameFormat = (value) => {
        const keys = Array.isArray(value) ? value : `${value || ""}`.trim().split(/\s+/).filter(Boolean);
        const validKeys = [];
        if (keys.length === 0) {
            return [...defaultFileNameFormatKeys];
        }
        for (const key of keys) {
            if (!NAME_KEYS.includes(key)) {
                return [...defaultFileNameFormatKeys];
            }
            if (!validKeys.includes(key)) {
                validKeys.push(key);
            }
        }
        return validKeys;
    };

    // 获取文件名字段显示名称。
    const getFileNameKeyLabel = (key) => t.fileNameKeyLabels[key] || key;

    const storedFileNameFormatKeys = parseFileNameFormat(GM_getValue("fileNameFormat", defaultFileNameFormatKeys));

    let config = {
        disclaimer: GM_getValue("disclaimer", false),
        packageDownloadFiles: GM_getValue("packageDownloadFiles", true),
        autoScrollSwitch: GM_getValue("autoScrollSwitch", false),
        maxScrollCount: GM_getValue("maxScrollCount", 50),
        keepMenuVisible: GM_getValue("keepMenuVisible", false),
        linkCheckboxSwitch: GM_getValue("linkCheckboxSwitch", true),
        imageCheckboxSwitch: GM_getValue("imageCheckboxSwitch", true),
        imageDownloadFormat: GM_getValue("imageDownloadFormat", "jpeg"),
        videoPreference: GM_getValue("videoPreference", "resolution"),
        scriptServerURL: GM_getValue("scriptServerURL", defaultsWebSocketURL),
        scriptServerSwitch: GM_getValue("scriptServerSwitch", false),
        fileNameFormatKeys: storedFileNameFormatKeys,
        icon: {
            type: 'image', // 可选: image/svg/font
            image: {
                url: iconBase64, // 图片URL或Base64
                size: 64, // 图标尺寸
                borderRadius: '50%' // 形状（50%为圆形）
            },
        }, // 位置配置
        position: {
            top: '6rem', right: '6rem'
        }, // 动画配置
        animation: {
            duration: 0.25, // 动画时长(s)
            easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
        }
    };

    const readme = async () => {
        await showTextModal({
                                title: t.readmeTitle, text: t.instructionsText, mode: 'info', closeText: t.closeButton
                            });
        if (!config.disclaimer) {
            showTextModal({
                              title: t.disclaimerTitle,
                              text: t.disclaimerText,
                              mode: 'confirm',
                              confirmText: t.disclaimerConfirm,
                              closeText: t.closeButton
                          }).then(answer => {
                GM_setValue("disclaimer", answer);
                config.disclaimer = answer;
            });
        }
    };

    if (!config.disclaimer) {
        readme().then();
    }

    console.info("用户接受 XHS-Downloader 免责声明", config.disclaimer)

    let registeredMenuCommandIds = [];

    const unregisterMenuCommands = () => {
        if (typeof GM_unregisterMenuCommand !== 'function') {
            registeredMenuCommandIds = [];
            return;
        }
        registeredMenuCommandIds.forEach(id => {
            if (id !== undefined) {
                GM_unregisterMenuCommand(id);
            }
        });
        registeredMenuCommandIds = [];
    };

    const registerMenuCommands = () => {
        unregisterMenuCommands();
        const menuCommands = [{
            label: t.readmeMenuTitle,
            action: () => readme().then(),
        }, {
            label: t.resetIconPositionMenuText,
            action: () => resetIconPosition(),
        }, {
            label: lang === "CN" ? i18n.EN.switchToLanguageMenuText : i18n.CN.switchToLanguageMenuText,
            action: () => {
                lang = lang === "CN" ? "EN" : "CN";
                GM_setValue("language", lang);
                t = i18n[lang];
                if (isMenuVisible) {
                    updateMenuContent();
                    positionMenu();
                }
                setTimeout(registerMenuCommands, 0);
            },
        }];
        registeredMenuCommandIds = menuCommands.map(item => GM_registerMenuCommand(item.label, item.action));
    };

    registerMenuCommands();

    const updatePackageDownloadFiles = (value) => {
        config.packageDownloadFiles = value;
        GM_setValue("packageDownloadFiles", config.packageDownloadFiles);
    };

    const updateAutoScrollSwitch = (value) => {
        config.autoScrollSwitch = value;
        GM_setValue("autoScrollSwitch", config.autoScrollSwitch);
    };

    const updateMaxScrollCount = (value) => {
        config.maxScrollCount = parseInt(value) || 50;
        GM_setValue("maxScrollCount", config.maxScrollCount);
    };

    const updateKeepMenuVisible = (value) => {
        config.keepMenuVisible = value;
        GM_setValue("keepMenuVisible", config.keepMenuVisible);
        if (config.keepMenuVisible) {
            showMenu();
        } else {
            hideMenu();
        }
    };

    const updateLinkCheckboxSwitch = (value) => {
        config.linkCheckboxSwitch = value;
        GM_setValue("linkCheckboxSwitch", config.linkCheckboxSwitch);
    }

    const updateImageCheckboxSwitch = (value) => {
        config.imageCheckboxSwitch = value;
        GM_setValue("imageCheckboxSwitch", config.imageCheckboxSwitch);
    }

    const updateScriptServerURL = (value) => {
        config.scriptServerURL = value;
        GM_setValue("scriptServerURL", config.scriptServerURL);
    }

    const updateScriptServerSwitch = (value) => {
        webSocket.disconnect();
        if (value) {
            webSocket.url = config.scriptServerURL;
            webSocket.connect();
        }
        config.scriptServerSwitch = value;
        GM_setValue("scriptServerSwitch", config.scriptServerSwitch);
    }

    const updateImageDownloadFormat = (value) => {
        config.imageDownloadFormat = value.toLowerCase();
        GM_setValue("imageDownloadFormat", config.imageDownloadFormat);
    }

    const updateVideoPreference = (value) => {
        config.videoPreference = value;
        GM_setValue("videoPreference", value);
    };

    // 更新文件名格式配置。
    const updateFileNameFormat = (value) => {
        config.fileNameFormatKeys = parseFileNameFormat(value);
        GM_setValue("fileNameFormat", config.fileNameFormatKeys);
    };

    const about = () => {
        showTextModal({
                          title: t.aboutTitle, text: t.aboutText, mode: 'info', closeText: t.closeButton
                      }).then();
    }

    const abnormal = (text) => {
        showTextModal({
                          title: t.errorTitle, text: t.errorText(text), mode: 'info', closeText: t.closeButton
                      }).then();
    };

    const runTips = (text) => {
        showTextModal({
                          title: t.tipsTitle, text: text, mode: 'info', closeText: t.closeButton
                      }).then();
    }

    const detailUrlPattern = {
        "xiaohongshu": {
            "normal": /http:\/\/sns-webpic-qc\.xhscdn\.com\/\d+\/[0-9a-z]+\/(\S+)!/, "video": undefined,
        }, "rednote": {
            "normal": /http:\/\/sns-web-i10\.rednotecdn\.com\/\d+\/[0-9a-z]+\/(\S+)!/, "video": undefined,
        }
    }

    const preferenceKey = {
        resolution: "height",
        bitrate: "videoBitrate",
        size: "size",
    };

    const generateVideoUrl = note => {
        try {
            const key = note.video?.consumer?.originVideoKey;
            if (key) return [`https://sns-video-bd.xhscdn.com/${key}`];
            const allStreams = Object.values(note.video.media.stream).flat();
            if (allStreams.length === 0) return [];
            sortArray(allStreams, preferenceKey[config.videoPreference]);
            const stream = allStreams[0];
            return [stream.backupUrls[0] || stream.masterUrl];
        } catch (error) {
            console.error("Error deal video URL:", error);
            return [];
        }
    };

    /**
     * @param {Array} arr - 原数组
     * @param {String} key - 排序字段
     */
    function sortArray(arr, key) {
        arr.sort((a, b) => {
            const vA = a[key];
            const vB = b[key];
            return vB - vA;
        });
    }

    // 收集所有可选视频流（原画 + 转码流），供"手动选择视频清晰度"使用
    const generateVideoStreams = note => {
        const video = note.video;
        if (!video) return [];
        // 仅保护可能抛错的数据收集阶段，排序与原画拼不会抛错
        let renditions;
        try {
            renditions = Object.values(video.media?.stream || {})
                .flat()
                .filter(Boolean)
                .map(s => ({
                    url: s.backupUrls?.[0] || s.masterUrl,
                    width: s.width,
                    height: s.height,
                    bitrate: s.videoBitrate,
                    fps: s.fps,
                    size: s.size,
                    qualityType: s.qualityType,
                }))
                .filter(s => s.url);
        } catch (error) {
            console.error("Error generate video streams:", error);
            return [];
        }
        // 按分辨率降序，默认列出最高画质在前（原画已置于首位）
        renditions.sort((a, b) => (b.height ?? 0) - (a.height ?? 0));
        const streams = [];
        const originKey = video?.consumer?.originVideoKey;
        if (originKey) {
            streams.push({
                url: `https://sns-video-bd.xhscdn.com/${originKey}`,
                isOriginal: true,
            });
        }
        streams.push(...renditions);
        return streams;
    };

    const generateImageUrl = note => {
        let images = note.imageList;
        const regex = detailUrlPattern[currentSite]["normal"];
        let urls = [];
        try {
            images.forEach((item) => {
                const url = item.urlDefault || item.url;
                let match = url.match(regex);
                if (match && match[1]) {
                    urls.push(
                        `https://ci.xiaohongshu.com/${match[1]}?imageView2/format/${GM_getValue(
                            "imageDownloadFormat",
                            "jpeg"
                        )}`);
                }
            })
            return urls
        } catch (error) {
            console.error("Error generating image URLs:", error);
            return [];
        }
    };

    const extractImageWebpUrls = (note, urls,) => {
        try {
            let items = []
            let {imageList} = note;
            if (urls.length !== imageList.length) {
                console.error("图片数量不一致！")
                return []
            }
            for (const [index, item] of imageList.entries()) {
                const url = item.urlDefault || item.url;
                if (url) {
                    items.push({
                                   webp: url, index: index + 1, url: urls[index],
                               })
                } else {
                    console.error("提取图片预览链接失败", item)
                    break
                }
            }
            return items;
        } catch (error) {
            console.error("Error occurred in generating image object:", error);
            return []
        }
    };

    const download = async (urls, note, server = false,) => {
        const name = extractName(note);
        if (server) {
            let data = {data: note, index: null,};
            if (note.type === "normal") {
                let items = extractImageWebpUrls(note, urls);
                if (items.length === 0) {
                    console.error("解析图文作品数据失败", note)
                    abnormal(t.imageExtractError)
                } else if (urls.length > 1 && config.imageCheckboxSwitch) {
                    data.index = await showImageSelectionModal(items, name, server,);
                }
            }
            webSocket.send(JSON.stringify(data));
        } else {
            console.debug(`文件名称 ${name}`);
            if (note.type === "video") {
                showToast(t.downloadTips);
                await downloadVideo(urls[0], name);
            } else {
                let items = extractImageWebpUrls(note, urls);
                if (items.length === 0) {
                    console.error("解析图文作品数据失败", note)
                    abnormal(t.imageExtractError)
                } else if (urls.length > 1 && config.imageCheckboxSwitch) {
                    await showImageSelectionModal(items, name,);
                } else {
                    showToast(t.downloadTips);
                    await downloadImage(items, name);
                }
            }
        }
    };

    // 选择最终视频下载链接：手动模式下弹出选择窗口，其余沿用 generateVideoUrl 的自动选择
    // 返回 null 表示用户取消（不下载也不报错），[] 表示无可用流，[url] 表示确定下载
    const selectVideoStream = async (note, server) => {
        if (config.videoPreference !== "manual") {
            return generateVideoUrl(note);
        }
        const streams = generateVideoStreams(note);
        if (streams.length === 0) return [];
        let selectedUrl = streams[0].url; // 默认最高画质（原画或最高转码流）
        if (!server && streams.length > 1) {
            const selected = await showVideoStreamSelectionModal(streams);
            if (!selected) return null; // 用户取消
            selectedUrl = selected.url;
        }
        return [selectedUrl];
    };

    const exploreDeal = async (note, server = false,) => {
        try {
            let links;
            if (note.type === "normal") {
                links = generateImageUrl(note);
            } else {
                links = await selectVideoStream(note, server);
                if (links === null) return; // 用户取消
            }
            if (links.length > 0) {
                // console.debug("下载链接", links);
                await download(links, note, server,);
            } else {
                abnormal(t.downloadLinkError)
            }
        } catch (error) {
            console.error("Error in exploreDeal function:", error);
            abnormal(t.downloadError);
        }
    };

    // 提取作品详情数据。
    const extractNoteInfo = () => {
        const initialState = unsafeWindow.__INITIAL_STATE__;
        const data = initialState?.noteData?.data?.noteData;
        if (data) return data;
        const noteId = extractCurrentNoteId();
        const noteDetailMap = initialState?.note?.noteDetailMap;
        const noteDetailItems = Object.values(noteDetailMap || {});
        const note = (noteId && noteDetailMap?.[noteId]?.note) || noteDetailItems[noteDetailItems.length - 1]?.note;
        if (note) {
            return note;
        }
        console.error("从页面提取作品数据失败", currentUrl,);
    };

    const extractDownloadLinks = async (server = false) => {
        if (currentUrl.includes(`https://www.${currentSite}.com/explore/`) || currentUrl.includes(
            `https://www.${currentSite}.com/discovery/item/`)) {
            let note = extractNoteInfo();
            if (note) {
                await exploreDeal(note, server,);
            } else {
                abnormal(t.extractError);
            }
        }
    };

    const triggerDownload = (name, blob) => {
        // 创建 Blob 对象的 URL
        const blobUrl = URL.createObjectURL(blob);

        // 创建一个临时链接元素
        const tempLink = document.createElement("a");
        tempLink.href = blobUrl;
        tempLink.download = name;

        // 将链接添加到 DOM 并模拟点击
        document.body.appendChild(tempLink); // 避免某些浏览器安全限制
        tempLink.click();

        // 清理临时链接元素
        document.body.removeChild(tempLink); // 从 DOM 中移除临时链接
        URL.revokeObjectURL(blobUrl); // 释放 URL

        // console.debug(`文件已成功下载: ${name}`);
    }

    const downloadFile = async (link, name, trigger = true, retries = 5) => {
        for (let attempt = 1; attempt <= retries; attempt++) {
            try {
                // 使用 fetch 获取文件数据
                const response = await fetch(link, {
                    "headers": {
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "accept-language": "zh-SG,zh;q=0.9",
                    }, "method": "GET", "referrerPolicy": "no-referrer",
                });

                // 检查响应状态码
                if (!response.ok) {
                    console.error(`下载失败，状态码: ${response.status}，URL: ${link}，尝试次数: ${attempt}`);
                    continue; // 继续下一次尝试
                }

                const blob = await response.blob();

                if (trigger) {
                    triggerDownload(name, blob);
                    return true;
                } else {
                    return blob;
                }
            } catch (error) {
                console.error(`下载失败 (${name})，错误信息:`, error, `尝试次数: ${attempt}`);
                if (attempt === retries) {
                    return false; // 如果达到最大重试次数，返回失败
                }
            }
        }
        return false; // 如果所有尝试都失败，返回失败
    };

    const downloadFiles = async (items, name,) => {
        const downloadResults = []; // 用于存储下载结果

        const downloadPromises = items.map(async (item) => {
            let fileName;
            if (item.index) {
                fileName = `${name}_${item.index}.${GM_getValue("imageDownloadFormat", "jpeg")}`; // 根据索引生成文件名
            } else {
                fileName = `${name}.${GM_getValue("imageDownloadFormat", "jpeg")}`;
            }
            const result = await downloadFile(item.url, fileName, false); // 调用单个文件下载方法
            if (result) {
                downloadResults.push({name: fileName, file: result});
                return true; // 成功
            } else {
                return false; // 失败
            }
        });

        // 等待所有下载操作完成
        const results = await Promise.all(downloadPromises);

        if (results.every(result => result === true)) {
            try {
                const zip = new JSZip();
                downloadResults.forEach((item) => {
                    zip.file(item.name, item.file);
                });

                const content = await zip.generateAsync({type: "blob", compression: "STORE"});
                triggerDownload(`${name}.zip`, content,)
                return true;
            } catch (error) {
                console.error('生成 ZIP 文件或保存失败，错误信息:', error);
                return false;
            }
        } else {
            return false;
        }
    };

    // 截断过长字符串。
    const truncateString = (str, maxLength) => {
        const characters = Array.from(`${str ?? ""}`);
        if (characters.length > maxLength) {
            const availableLength = maxLength - 3;
            const startLength = Math.floor(availableLength / 2);
            const endLength = availableLength - startLength;
            return characters.slice(0, startLength).join("") + '...' + characters.slice(-endLength).join("");
        }
        return characters.join("");
    };

    // 清理文件名文本。
    const filterFileName = (value) => {
        const name = `${value ?? ""}`
            .replace(fileNameInvalidCharPattern, " ")
            .replace(fileNameBlankPattern, " ")
            .trim()
            .replace(fileNameTrailingDotBlankPattern, "");
        if (name === "." || name === "..") {
            return "";
        }
        return reservedFileNamePattern.test(name) ? "" : name;
    };

    // 按路径读取对象值。
    const safeExtract = (data, path, defaultValue = "") => {
        if (!data) {
            return defaultValue;
        }
        const value = path.split(".").reduce((current, key) => current?.[key], data);
        return value ?? defaultValue;
    };

    // 提取当前作品 ID。
    const extractCurrentNoteId = () => {
        const match = currentUrl?.match(/\/(?:explore|discovery\/item)\/([^/?#]+)/);
        return match ? match[1] : "";
    };

    // 提取作品数据内的作品 ID。
    const getNoteId = (note) => {
        return safeExtract(note, "noteId") || safeExtract(note, "id") || extractCurrentNoteId();
    };

    // 格式化命名时间。
    const formatNameTime = (value) => {
        const timestamp = Number(value);
        if (!Number.isFinite(timestamp) || timestamp <= 0) {
            return "未知";
        }
        const date = new Date(timestamp > 1000000000000 ? timestamp : timestamp * 1000);
        if (Number.isNaN(date.getTime())) {
            return "未知";
        }
        const pad = number => `${number}`.padStart(2, "0");
        return [
            `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`,
            `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
        ].join("_");
    };

    // 判断作品类型名称。
    const classifyNoteType = (note) => {
        const type = safeExtract(note, "type");
        const imageList = safeExtract(note, "imageList", []);
        if (!["video", "normal"].includes(type) || !Array.isArray(imageList) || imageList.length === 0) {
            return "未知";
        }
        if (type === "video") {
            return imageList.length === 1 ? "视频" : "图集";
        }
        return "图文";
    };

    // 文件名字段值提取器。
    const fileNameValueExtractors = {
        "收藏数量": note => safeExtract(note, "interactInfo.collectedCount", "0"),
        "评论数量": note => safeExtract(note, "interactInfo.commentCount", "0"),
        "分享数量": note => safeExtract(note, "interactInfo.shareCount", "0"),
        "点赞数量": note => safeExtract(note, "interactInfo.likedCount", "0"),
        "作品标签": note => {
            const tags = safeExtract(note, "tagList", []);
            return Array.isArray(tags) ? tags.map(item => safeExtract(item, "name")).filter(Boolean).join(" ") : tags;
        },
        "作品ID": note => getNoteId(note),
        "作品标题": note => safeExtract(note, "title") || safeExtract(note, "displayTitle") || getNoteId(note),
        "作品描述": note => safeExtract(note, "desc"),
        "作品类型": note => classifyNoteType(note),
        "发布时间": note => formatNameTime(safeExtract(note, "time")),
        "更新时间": note => formatNameTime(safeExtract(note, "lastUpdateTime")),
        "作者昵称": note => safeExtract(note, "user.nickname") || safeExtract(note, "user.nickName"),
        "作者ID": note => safeExtract(note, "user.userId"),
    };

    // 提取单个文件名字段值。
    const getFileNameKeyValue = (note, key) => {
        const extractor = fileNameValueExtractors[key];
        return extractor ? extractor(note) : "";
    };

    // 获取文件名字段回退值。
    const getFallbackFileNameValue = (values, note, key) => {
        return filterFileName(values[key]) || filterFileName(getFileNameKeyValue(note, key));
    };

    // 作品字段值设置入口
    const setFileNameKeyValues = (values, note, keys = NAME_KEYS) => {
        if (!note) {
            return;
        }
        keys.forEach(key => {
            values[key] = getFileNameKeyValue(note, key);
        });
    };

    // 创建文件名字段值集合。
    const getFileNameKeyValues = (note, keys = NAME_KEYS) => {
        const values = {};
        keys.forEach(key => {
            values[key] = "";
        });
        setFileNameKeyValues(values, note, keys);
        return values;
    };

    // 格式化单个文件名字段。
    const formatFileNameValue = (key, value, values, note) => {
        if (Array.isArray(value)) {
            value = value.join(" ");
        }
        value = `${value ?? ""}`.trim();
        if (key === "发布时间" || key === "更新时间") {
            value = value.replace(/:/g, ".");
        } else if (key === "作者昵称") {
            return filterFileName(value) || getFallbackFileNameValue(values, note, "作者ID");
        } else if (key === "作品标题") {
            return filterFileName(value) || getFallbackFileNameValue(values, note, "作品ID");
        } else if (key === "作品描述") {
            const filteredValue = filterFileName(value.replace(fileNameTopicMarkerPattern, ""));
            return filteredValue ? truncateString(filteredValue, fileNameDescriptionMaxLength) :
                   getFallbackFileNameValue(values, note, "作品ID");
        }
        if (!value) {
            return "";
        }
        return filterFileName(value);
    };

    // 生成自定义下载文件名。
    const extractCustomName = (note) => {
        const values = getFileNameKeyValues(note, config.fileNameFormatKeys);
        const name = config.fileNameFormatKeys
                           .map(key => formatFileNameValue(key, values[key], values, note))
                           .filter(Boolean)
                           .join("_");
        if (name) {
            return truncateString(name, fileNameMaxLength);
        }
        const fallback = getFallbackFileNameValue(values, note, "作品ID");
        return truncateString(fallback, fileNameMaxLength);
    };

    // 从页面标题提取文件名。
    const extractDocumentName = () => {
        let name = filterFileName(document.title.replace(/ - 小红书$/, "").replace(/ - rednote$/, ""));
        name = truncateString(name, 64,);
        let id = extractCurrentNoteId() || null;
        return name === "" ? id : name
    };

    // 获取下载文件名。
    const extractName = (note) => {
        return extractCustomName(note) || extractDocumentName();
    };

    const downloadVideo = async (url, name) => {
        if (!await downloadFile(url, `${name}.mp4`)) {
            abnormal(t.videoDownloadError);
        }
    };

    const downloadImage = async (items, name) => {
        let success;
        if (!config.packageDownloadFiles && items.length > 1) {
            let result = [];
            for (let item of items) {
                result.push(await downloadFile(
                    item.url,
                    `${name}_${item.index}.${GM_getValue("imageDownloadFormat", "jpeg")}`
                ));
            }
            success = result.every(item => item === true);
        } else if (items.length === 1) {
            success = await downloadFile(items[0].url, `${name}.${GM_getValue("imageDownloadFormat", "jpeg")}`);
        } else {
            success = await downloadFiles(items, name,);
        }
        if (!success) {
            abnormal(t.imageDownloadError);
        }
    };

    const window_scrollBy = (x, y,) => {
        window.scrollBy(x, y,);
    }

    // 随机整数生成函数
    const getRandomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

    // 判断是否需要暂停，模拟用户的停顿行为
    const shouldPause = () => Math.random() < 0.2;  // 20%几率停顿

    // 执行一次增量滚动
    const scrollOnce = () => {
        const scrollDistanceMin = 100;  // 最小滚动距离
        const scrollDistanceMax = 300; // 最大滚动距离
        const scrollDistance = getRandomInt(scrollDistanceMin, scrollDistanceMax);
        window_scrollBy(0, scrollDistance);  // 增量滚动
    };

    // 检查是否已经滚动到底部
    const isAtBottom = () => {
        const docHeight = document.documentElement.scrollHeight;
        const winHeight = window.innerHeight;
        const scrollPos = window.scrollY;

        return (docHeight - winHeight - scrollPos <= 10);  // 如果距离底部小于10px，认为滚动到底部
    };

    // 自动滚动主函数
    const scrollScreen = (callback, endless = false, scrollCount = 0,) => {
        const timeoutMin = 250;  // 最小滚动间隔
        const timeoutMax = 500;  // 最大滚动间隔

        const scrollInterval = setInterval(() => {
            if (shouldPause()) {
                // 停顿，模拟用户的休息
                clearInterval(scrollInterval);
                setTimeout(() => {
                    scrollScreen(callback, endless, scrollCount,);  // 重新启动滚动
                }, getRandomInt(timeoutMin, timeoutMax,));  // 随机停顿时间
            } else if (endless) {
                // 无限滚动至底部模式
                if (!isAtBottom()) {
                    scrollOnce();  // 执行一次滚动
                } else {
                    // 到达底部，停止滚动
                    clearInterval(scrollInterval);
                    callback();  // 调用回调函数
                }
            } else if (scrollCount < config.maxScrollCount && !isAtBottom()) {
                scrollOnce();  // 执行一次滚动
                scrollCount++;
            } else {
                // 如果到达底部或滚动次数已满，停止滚动
                clearInterval(scrollInterval);
                callback();  // 调用回调函数
            }
        }, getRandomInt(timeoutMin, timeoutMax));  // 随机滚动间隔
    };

    const scrollScreenEvent = (callback, endless = false) => {
        if (config.autoScrollSwitch) {
            scrollScreen(callback, endless,);
        } else {
            callback();
        }
    };

    const extractNotesInfo = order => {
        const notesRawValue = unsafeWindow.__INITIAL_STATE__.user.notes._rawValue[order];
        return notesRawValue.filter(item => item?.noteCard).map(
            item => [item.id, item.xsecToken, item.noteCard.cover.urlDefault, item.noteCard.user.nickName,
                     item.noteCard.displayTitle,]);
    };

    const extractBoardInfo = () => {
        // 定义正则表达式来匹配 URL 中的 ID
        const regex = /\/board\/([a-z0-9]+)\?/;

        // 使用 exec 方法执行正则表达式
        const match = regex.exec(currentUrl);

        // 检查是否有匹配
        if (match) {
            // 提取 ID
            const id = match[1]; // match[0] 是整个匹配的字符串，match[1] 是第一个括号内的匹配

            const notesRawValue = unsafeWindow.__INITIAL_STATE__.board.boardFeedsMap._rawValue[id].notes;
            return notesRawValue.map(
                item => [item.noteId, item.xsecToken, item.cover.urlDefault, item.user.nickName, item.displayTitle,]);
        } else {
            console.error("从链接提取专辑 ID 失败", currentUrl,);
            return [];
        }
    };

    const extractFeedInfo = () => {
        const notesRawValue = unsafeWindow.__INITIAL_STATE__.feed.feeds._rawValue;
        return notesRawValue.filter(item => item?.noteCard).map(
            item => [item.id, item.xsecToken, item.noteCard.cover.urlDefault, item.noteCard.user.nickName,
                     item.noteCard.displayTitle,]);
    };

    const extractSearchNotes = () => {
        const notesRawValue = unsafeWindow.__INITIAL_STATE__.search.feeds._rawValue;
        return notesRawValue.filter(item => item?.noteCard).map(
            item => [item.id, item.xsecToken, item.noteCard.cover.urlDefault, item.noteCard.user.nickName,
                     item.noteCard.displayTitle,]);
    }

    const extractSearchUsers = () => {
        const notesRawValue = unsafeWindow.__INITIAL_STATE__.search.userLists._rawValue;
        return notesRawValue.map(item => item.id);
    }

    const generateNoteUrls = data => data.map(
        ([id, token,]) => `https://www.xiaohongshu.com/discovery/item/${id}?source=webshare&xhsshare=pc_web&xsec_token=${token}&xsec_source=pc_share`)
                                         .join(" ");

    const generateUserUrls = data => data.map(id => `https://www.${currentSite}.com/user/profile/${id}`).join(" ");

    const invalidDetection = data => data.every(([first]) => Boolean(first));

    const extractAllLinks = (callback, order) => {
        scrollScreenEvent(() => {
            let data;
            if (order >= 0 && order <= 2) {
                data = extractNotesInfo(order);
                if (!invalidDetection(data)) {
                    runTips(t.signInPrompt);
                    return;
                }
            } else if (order === 3) {
                data = extractSearchNotes();
            } else if (order === 4) {
                data = extractSearchUsers();
            } else if (order === -1) {
                data = extractFeedInfo()
            } else if (order === 5) {
                data = extractBoardInfo()
            } else {
                data = []
            }
            if (data.length === 0) {
                callback("");
                return;
            }
            let urlsString;
            if (order === 4) {
                urlsString = generateUserUrls(data);
                callback(urlsString);
            } else if (config.linkCheckboxSwitch) {
                showListSelectionModal(data.map(([id, token, cover, author, title,]) => ({
                    id: id, token: token, image: cover, author: author, title: title,
                })),).then((selected) => {
                    if (selected.length > 0) {
                        urlsString = generateNoteUrls(selected.map(item => [item.id, item.token]));
                        callback(urlsString);
                    }
                });
            } else {
                urlsString = generateNoteUrls(data.map(item => item.slice(0, 2)))
                callback(urlsString);
            }
        }, [0, 1, 2, 5].includes(order))
    };

    const extractAllLinksEvent = (order = 0) => {
        extractAllLinks(urlsString => {
            if (urlsString) {
                GM_setClipboard(urlsString, "text", () => {
                    showToast(t.linkExtractSuccess);
                });
            } else {
                showToast(t.linkExtractError)
            }
        }, order);
    };

    if (typeof JSZip === 'undefined') {
        runTips(t.jsZipError);
    }

    let style = document.createElement('style');
    style.textContent = `
    /* 通用 Overlay（三个弹窗共用） */
    #SettingsOverlay,
    #imageSelectionOverlay,
    #textGenericOverlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.32);
        backdrop-filter: blur(4px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        animation: fadeIn 0.3s;
    }

    /* Settings 容器，仅本块特有尺寸 */
    .optimized-scroll-modal {
        background: white;
        border-radius: 16px;
        width: 860px;
        max-width: 95vw;
        max-height: 95vh;
        box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
        overflow: hidden;
        animation: scaleUp 0.3s;
        display: flex;
        flex-direction: column;
    }

    /* 通用头部/内容/底部/按钮（三个弹窗共用） */
    .modal-header {
        padding: 1rem;
        border-bottom: 1px solid #eee;
        text-align: center;
    }
    .modal-header span {
        font-size: 1.25rem;
        font-weight: 500;
        color: #212121;
    }
    .modal-body {
        flex: 1;
        padding: 1rem;
        overflow-y: auto;
    }
    .scrollable-modal-body {
        overflow-y: scroll;
        scrollbar-gutter: stable;
        scrollbar-width: thin;
        scrollbar-color: #bdbdbd #f5f5f5;
    }
    .scrollable-modal-body::-webkit-scrollbar {
        width: 10px;
    }
    .scrollable-modal-body::-webkit-scrollbar-track {
        background: #f5f5f5;
        border-radius: 8px;
    }
    .scrollable-modal-body::-webkit-scrollbar-thumb {
        background: #bdbdbd;
        border: 2px solid #f5f5f5;
        border-radius: 8px;
    }
    .scrollable-modal-body::-webkit-scrollbar-thumb:hover {
        background: #9e9e9e;
    }
    .settings-body {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 18px 20px;
        align-items: start;
    }
    .modal-footer {
        padding: 1rem;
        border-top: 1px solid #eee;
        display: flex;
        justify-content: flex-end;
        gap: 12px;
    }
    .primary-btn {
        background: #2196F3;
        color: white;
        padding: 8px 24px;
        border-radius: 24px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .secondary-btn {
        background: #f0f0f0;
        color: #666;
        padding: 8px 24px;
        border-radius: 24px;
        cursor: pointer;
        transition: all 0.2s;
    }

    /* Settings 专用的设置项样式（保持不变） */
    .setting-item {
        margin: 0.5rem 0;
        padding: 10px;
        border-radius: 8px;
        transition: background 0.2s;
    }
    .setting-item:hover { background: #f0f0f0; }
    .settings-body .setting-item {
        margin: 0;
        min-width: 0;
    }
    .settings-group {
        display: flex;
        flex-direction: column;
        gap: 10px;
        min-width: 0;
    }
    .settings-group.wide {
        grid-column: 1 / -1;
    }
    .settings-group-title {
        color: #212121;
        font-size: 0.95rem;
        font-weight: 600;
        line-height: 1.4;
        padding-bottom: 6px;
        border-bottom: 1px solid #eee;
    }
    .settings-group-content {
        display: flex;
        flex-direction: column;
        gap: 10px;
        min-width: 0;
    }
    .settings-group.wide .settings-group-content {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px 12px;
    }
    .setting-item label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    .setting-item label span {
        font-size: 1rem;
        font-weight: 500;
        color: #333;
    }

    .toggle-switch {
        position: relative;
        width: 40px;
        height: 20px;
    }
    .toggle-switch input { opacity: 0; width: 0; height: 0; }
    .slider {
        position: absolute;
        cursor: pointer;
        top: 0; left: 0; right: 0; bottom: 0;
        background: #ccc;
        transition: 0.4s;
        border-radius: 34px;
    }
    .slider:before {
        content: "";
        position: absolute;
        height: 16px; width: 16px;
        left: 2px; bottom: 2px;
        background: white;
        border-radius: 50%;
        transition: 0.4s;
    }
    input:checked + .slider { background: #2196F3; }
    input:checked + .slider:before { transform: translateX(20px); }

    .number-input {
        display: flex;
        align-items: center;
        border: 1px solid #ddd;
        border-radius: 8px;
        overflow: hidden;
        margin: 6px 0;
    }
    .number-input input {
        width: 60px;
        text-align: center;
        border: none;
    }
    .number-button {
        padding: 4px 8px;
        background: #f0f0f0;
        border: none;
        cursor: pointer;
        transition: all 0.2s;
    }
    .text-input {
        width: 100%;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 0.9rem;
        margin-top: 8px;
        transition: border-color 0.2s;
    }
    .text-input:focus {
        outline: none;
        border-color: #2196F3;
        box-shadow: 0 0 4px rgba(33, 150, 243, 0.3);
    }
    .select-input {
        min-width: 130px;
        width: auto;
        padding: 8px 12px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 0.9rem;
        margin-top: 8px;
        background: #fff;
        transition: border-color 0.2s, box-shadow 0.2s;
        appearance: none;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M3 4.5L6 7.5L9 4.5H3Z'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 12px center;
        padding-right: 32px;
    }
    .select-input:focus {
        outline: none;
        border-color: #2196F3;
        box-shadow: 0 0 4px rgba(33, 150, 243, 0.3);
    }
    .select-input:disabled {
        background-color: #f5f5f5;
        color: #999;
        cursor: not-allowed;
    }
    .setting-description {
        font-size: 0.875rem;
        color: #757575;
        margin-top: 4px;
        line-height: 1.4;
        text-align: left;
    }
    .file-name-format-item {
        grid-column: 1 / -1;
    }
    .file-name-format-editor {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 10px;
    }
    .file-name-format-group-title {
        font-size: 0.85rem;
        font-weight: 500;
        color: #555;
        margin-bottom: 6px;
    }
    .file-name-card-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        min-height: 42px;
        padding: 8px;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        background: #fff;
    }
    .file-name-card {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        min-height: 30px;
        padding: 5px 8px;
        border: 1px solid #d0d0d0;
        border-radius: 4px;
        background: #fafafa;
        color: #333;
        font-size: 0.85rem;
        line-height: 1.2;
        cursor: pointer;
        user-select: none;
        transition: background 0.15s, border-color 0.15s, opacity 0.15s;
    }
    .file-name-card.available:not(.disabled):hover {
        background: #f0f7ff;
        border-color: #90caf9;
    }
    .file-name-card.selected {
        background: #eaf4ff;
        border-color: #90caf9;
        cursor: grab;
    }
    .file-name-card.selected:active {
        cursor: grabbing;
    }
    .file-name-card.dragging {
        opacity: 0.5;
    }
    .file-name-card.disabled {
        opacity: 0.45;
        cursor: not-allowed;
    }
    .file-name-card-remove {
        width: 16px;
        height: 16px;
        padding: 0;
        border: none;
        background: transparent;
        color: #666;
        font-size: 16px;
        line-height: 14px;
        cursor: pointer;
    }
    .file-name-card-remove:hover {
        color: #d32f2f;
    }
    @media (max-width: 760px) {
        .optimized-scroll-modal {
            width: 95vw;
        }
        .settings-body {
            grid-template-columns: 1fr;
        }
        .settings-group.wide .settings-group-content {
            grid-template-columns: 1fr;
        }
    }

    /* 通用动画：统一定义一次 */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes scaleUp { from { transform: scale(0.98); } to { transform: scale(1); } }
    @keyframes fadeOut { from { opacity: 1; } to { opacity: 0; } }
    `;
    document.head.appendChild(style);

    // 覆盖修改：文本弹窗样式
    (() => {
        if (!document.getElementById('textModalStyle')) {
            const style = document.createElement('style');
            style.id = 'textModalStyle';
            style.textContent = `
            /* 仅文本弹窗容器特有的尺寸与外观 */
            .text-generic-modal {
                background: #fff;
                border-radius: 16px;
                width: 80%;
                max-width: 700px;
                max-height: 80vh;
                box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
                overflow: hidden;
                animation: scaleUp 0.3s;
                display: flex;
                flex-direction: column;
            }
            /* 仅该弹窗使用的文本内容样式 */
            .text-content {
                white-space: pre-wrap;
                word-break: break-word;
                color: #1e272e;
                line-height: 1.6;
                font-size: 0.95rem;
                user-select: text;
            }
            `;
            document.head.appendChild(style);
        }
    })();

    /**
     * 显示文本弹窗（手动调用）
     * @param {Object} opts
     * @param {string} opts.title    标题
     * @param {string} opts.text     文本内容
     * @param {'confirm'|'info'} opts.mode 模式：confirm=确认+关闭；info=仅关闭
     * @param {string} [opts.confirmText='确认'] 确认按钮文案（仅 confirm 模式生效）
     * @param {string} [opts.closeText='关闭']   关闭按钮文案
     * @returns {Promise<boolean>} confirm 返回 true；关闭/点遮罩返回 false
     */
    function showTextModal(opts) {
        const {
            title = t.tipsTitle, text = '', mode = 'info', confirmText = t.confirmButton, closeText = t.closeButton,
        } = opts || {};

        if (document.getElementById('textGenericOverlay')) {
            return Promise.resolve(false);
        }

        return new Promise((resolve) => {
            const overlay = document.createElement('div');
            overlay.id = 'textGenericOverlay';

            const modal = document.createElement('div');
            modal.className = 'text-generic-modal';

            const header = document.createElement('div');
            header.className = 'modal-header';
            header.innerHTML = `<span>${title}</span>`;

            const body = document.createElement('div');
            body.className = 'modal-body';
            const content = document.createElement('div');
            content.className = 'text-content';
            content.textContent = text ?? '';
            body.appendChild(content);

            const footer = document.createElement('div');
            footer.className = 'modal-footer';

            if (mode === 'confirm') {
                const okBtn = document.createElement('button');
                okBtn.className = 'primary-btn';
                okBtn.textContent = confirmText;
                okBtn.addEventListener('click', () => close(true));
                footer.appendChild(okBtn);
            }

            const closeBtn = document.createElement('button');
            closeBtn.className = 'secondary-btn';
            closeBtn.textContent = closeText;
            closeBtn.addEventListener('click', () => close(false));
            footer.appendChild(closeBtn);

            modal.appendChild(header);
            modal.appendChild(body);
            modal.appendChild(footer);
            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            function close(result) {
                overlay.style.animation = 'fadeOut 0.2s';
                setTimeout(() => {
                    overlay.remove();
                    resolve(result);
                }, 200);
            }

            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) close(false);
            });
        });
    }

    (() => {
        if (!document.getElementById('videoStreamStyle')) {
            const style = document.createElement('style');
            style.id = 'videoStreamStyle';
            style.textContent = `
            .video-quality-body {
                max-height: 60vh;
                overflow-y: auto;
            }
            .video-quality-item {
                display: flex;
                align-items: center;
                padding: 12px;
                margin: 8px 0;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                cursor: pointer;
                transition: background 0.15s, border-color 0.15s, box-shadow 0.15s;
            }
            .video-quality-item:hover {
                background: #fafafa;
                border-color: #e6e6e6;
            }
            .video-quality-item.selected {
                border-color: #2196F3;
                box-shadow: 0 0 0 4px rgba(33,150,243,0.12) inset;
            }
            .video-quality-radio {
                margin-right: 12px;
                width: 18px;
                height: 18px;
                cursor: pointer;
            }
            .video-quality-info {
                flex: 1;
            }
            .video-quality-title {
                font-weight: 600;
                font-size: 15px;
                margin-bottom: 4px;
            }
            .video-quality-sub {
                font-size: 13px;
                color: #666;
            }
            `;
            document.head.appendChild(style);
        }
    })();

    /**
     * 创建单个视频流选项（供 showVideoStreamSelectionModal 使用）
     * @param {Object} stream - 视频流描述符
     * @param {number} index - 序号
     * @param {(item: HTMLLabelElement) => void} onSelect - 选中回调
     * @returns {HTMLLabelElement}
     */
    const createStreamOption = (stream, index, onSelect) => {
        const item = document.createElement('label');
        item.className = 'video-quality-item';

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'xhsVideoStream';
        radio.value = index;
        radio.checked = index === 0;
        radio.className = 'video-quality-radio';
        radio.onchange = () => onSelect(item);

        const titleParts = [];
        if (stream.width && stream.height) {
            titleParts.push(`${stream.width}×${stream.height}`);
        }
        if (stream.isOriginal) {
            titleParts.push(t.videoQualityOriginal);
        } else if (stream.qualityType) {
            titleParts.push(stream.qualityType);
        }

        const subParts = [];
        if (stream.bitrate) subParts.push(`${t.videoQualityBitrate}: ${(stream.bitrate / 1000).toFixed(0)}kbps`);
        if (stream.fps) subParts.push(`${t.videoQualityFps}: ${stream.fps}fps`);
        if (stream.size) subParts.push(`${t.videoQualitySize}: ${(stream.size / 1024 / 1024).toFixed(2)}MB`);

        const info = document.createElement('div');
        info.className = 'video-quality-info';
        const titleDiv = document.createElement('div');
        titleDiv.className = 'video-quality-title';
        titleDiv.textContent = titleParts.join(' ');
        info.appendChild(titleDiv);
        const subDiv = document.createElement('div');
        subDiv.className = 'video-quality-sub';
        if (subParts.length) {
            subDiv.textContent = subParts.join(' | ');
            info.appendChild(subDiv);
        }

        item.appendChild(radio);
        item.appendChild(info);

        return item;
    };

    /**
     * 显示视频清晰度选择弹窗
     * @param {Array<{url:string, width?:number, height?:number, codec?:string, bitrate?:number, size?:number, qualityType?:string, isOriginal?:boolean}>} streams
     * @returns {Promise<Object|null>} 确认返回选中的流对象；取消或点击遮罩返回 null
     */
    function showVideoStreamSelectionModal(streams) {
        if (document.getElementById('videoStreamOverlay')) return Promise.resolve(null);

        return new Promise((resolve) => {
            const overlay = document.createElement('div');
            overlay.id = 'videoStreamOverlay';
            overlay.style.cssText = `position: fixed; inset: 0; background: rgba(0,0,0,0.32); backdrop-filter: blur(4px); display: flex; justify-content: center; align-items: center; z-index: 10000; animation: fadeIn 0.3s;`;

            const modal = document.createElement('div');
            modal.className = 'text-generic-modal';
            modal.style.maxWidth = '500px';

            const header = document.createElement('div');
            header.className = 'modal-header';
            const headerTitle = document.createElement('span');
            headerTitle.textContent = t.videoQualityTitle;
            header.appendChild(headerTitle);

            const body = document.createElement('div');
            body.className = 'modal-body video-quality-body';

            let selectedItem = null;
            const selectItem = (item) => {
                if (selectedItem) selectedItem.classList.remove('selected');
                selectedItem = item;
                item.classList.add('selected');
            };
            streams.forEach((stream, index) => {
                const item = createStreamOption(stream, index, selectItem);
                if (index === 0) selectItem(item);
                body.appendChild(item);
            });

            const footer = document.createElement('div');
            footer.className = 'modal-footer';

            const confirmBtn = document.createElement('button');
            confirmBtn.className = 'primary-btn';
            confirmBtn.textContent = t.startDownloadButton;
            confirmBtn.onclick = () => {
                const selected = modal.querySelector('input[name="xhsVideoStream"]:checked');
                close(selected ? streams[selected.value] : null);
            };

            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'secondary-btn';
            cancelBtn.textContent = t.closeDownloadButton;
            cancelBtn.onclick = () => close(null);

            footer.appendChild(confirmBtn);
            footer.appendChild(cancelBtn);

            modal.appendChild(header);
            modal.appendChild(body);
            modal.appendChild(footer);
            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            function close(result) {
                overlay.style.animation = 'fadeOut 0.2s';
                setTimeout(() => {
                    overlay.remove();
                    resolve(result);
                }, 200);
            }

            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) close(null);
            });
        });
    }

    // 创建开关项
    const createSwitchItem = ({label, description, checked, disabled = false}) => {
        const item = document.createElement('div');
        item.className = 'setting-item';
        item.style.opacity = disabled ? 0.6 : 1;

        item.innerHTML = `
            <label>
                <span>${label}</span>
                <div class="toggle-switch">
                    <input type="checkbox" ${checked ? 'checked' : ''} ${disabled ? 'disabled' : ''}>
                    <span class="slider"></span>
                </div>
            </label>
            <div class="setting-description">${description}</div>
        `;

        return item;
    };

    // 创建数值输入项
    const createNumberInput = ({label, description, value, min, max, disabled}) => {
        const item = document.createElement('div');
        item.className = 'setting-item';

        const numberInput = document.createElement('div');
        numberInput.className = 'number-input';
        numberInput.style.opacity = disabled ? 0.6 : 1;
        numberInput.innerHTML = `
            <button class="number-button" data-action="decrement">−</button>
            <input type="number" value="${value}" min="${min}" max="${max}" ${disabled ? 'disabled' : ''}>
            <button class="number-button" data-action="increment">+</button>
        `;

        item.innerHTML = `
            <label>
                <span>${label}</span>
                ${numberInput.outerHTML}
            </label>
            <div class="setting-description">${description}</div>
        `;

        // 绑定数值按钮事件
        const container = item.querySelector('.number-input');
        container.querySelectorAll('.number-button').forEach(btn => {
            btn.addEventListener('click', () => {
                const input = container.querySelector('input');
                if (input.disabled) {
                    return;
                }

                let val = parseInt(input.value);
                if (btn.dataset.action === 'increment') {
                    val = Math.min(val + 1, max);
                } else {
                    val = Math.max(val - 1, min);
                }
                input.value = val;
            });
        });

        return item;
    };

    // 创建文本输入项
    const createTextInput = ({label, description, placeholder, value, disabled = false}) => {
        const item = document.createElement('div');
        item.className = 'setting-item';
        item.style.opacity = disabled ? 0.6 : 1;

        const title = document.createElement('div');
        const titleText = document.createElement('span');
        titleText.style.cssText = 'font-size: 1rem; font-weight: 500; color: #333;';
        titleText.textContent = label;
        title.appendChild(titleText);

        const desc = document.createElement('div');
        desc.className = 'setting-description';
        desc.textContent = description;

        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'text-input';
        input.placeholder = placeholder ?? "";
        input.value = value ?? "";
        input.disabled = disabled;

        item.append(title, desc, input);

        return item;
    };

    // 创建文件名称格式编辑器
    const createFileNameFormatEditor = ({label, description, value}) => {
        const item = document.createElement('div');
        item.className = 'setting-item file-name-format-item';

        item.innerHTML = `
            <div>
                <span style="font-size: 1rem; font-weight: 500; color: #333;">${label}</span>
            </div>
            <div class="setting-description">${description}</div>
            <div class="file-name-format-editor">
                <div>
                    <div class="file-name-format-group-title">${t.fileNameSelectedLabel}</div>
                    <div class="file-name-card-list file-name-selected-fields"></div>
                </div>
                <div>
                    <div class="file-name-format-group-title">${t.fileNameAvailableLabel}</div>
                    <div class="file-name-card-list file-name-available-fields"></div>
                </div>
            </div>
        `;

        const selectedContainer = item.querySelector('.file-name-selected-fields');
        const availableContainer = item.querySelector('.file-name-available-fields');
        let selectedKeys = parseFileNameFormat(value);
        let draggedKey = null;

        item.getFileNameFormatKeys = () => [...selectedKeys];

        const removeKey = (key) => {
            if (selectedKeys.length <= 1) {
                return;
            }
            selectedKeys = selectedKeys.filter(item => item !== key);
            renderCards();
        };

        const addKey = (key) => {
            if (!selectedKeys.includes(key)) {
                selectedKeys.push(key);
                renderCards();
            }
        };

        const moveKey = (targetKey) => {
            if (!draggedKey || draggedKey === targetKey) {
                return;
            }
            const from = selectedKeys.indexOf(draggedKey);
            const to = selectedKeys.indexOf(targetKey);
            if (from === -1 || to === -1) {
                return;
            }
            const [key] = selectedKeys.splice(from, 1);
            selectedKeys.splice(to, 0, key);
            renderCards();
        };

        const createFieldCard = (key, selected) => {
            const card = document.createElement('div');
            card.className = `file-name-card ${selected ? 'selected' : 'available'}`;
            card.dataset.key = key;

            const text = document.createElement('span');
            text.textContent = getFileNameKeyLabel(key);
            card.appendChild(text);

            if (selected) {
                card.draggable = true;
                card.addEventListener('dragstart', (e) => {
                    draggedKey = key;
                    card.classList.add('dragging');
                    e.dataTransfer.effectAllowed = 'move';
                    e.dataTransfer.setData('text/plain', key);
                });
                card.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    e.dataTransfer.dropEffect = 'move';
                });
                card.addEventListener('drop', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    moveKey(key);
                    draggedKey = null;
                });
                card.addEventListener('dragend', () => {
                    draggedKey = null;
                    card.classList.remove('dragging');
                });

                const removeButton = document.createElement('button');
                removeButton.type = 'button';
                removeButton.className = 'file-name-card-remove';
                removeButton.title = t.fileNameRemoveTip;
                removeButton.textContent = '×';
                removeButton.addEventListener('click', (e) => {
                    e.stopPropagation();
                    removeKey(key);
                });
                card.appendChild(removeButton);
            } else if (selectedKeys.includes(key)) {
                card.classList.add('disabled');
            } else {
                card.addEventListener('click', () => addKey(key));
            }

            return card;
        };

        const renderSelectedCards = () => {
            selectedContainer.innerHTML = '';
            selectedKeys.forEach(key => {
                selectedContainer.appendChild(createFieldCard(key, true));
            });
        };

        const renderAvailableCards = () => {
            availableContainer.innerHTML = '';
            NAME_KEYS.forEach(key => {
                availableContainer.appendChild(createFieldCard(key, false));
            });
        };

        function renderCards() {
            renderSelectedCards();
            renderAvailableCards();
        }

        selectedContainer.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });
        selectedContainer.addEventListener('drop', (e) => {
            e.preventDefault();
            const target = e.target instanceof Element ? e.target : e.target.parentElement;
            if (draggedKey && target && !target.closest('.file-name-card')) {
                selectedKeys = selectedKeys.filter(key => key !== draggedKey);
                selectedKeys.push(draggedKey);
                renderCards();
                draggedKey = null;
            }
        });

        renderCards();
        return item;
    };

    // 创建下拉框项
    const createSelectItem = ({label, description, options, value, disabled = false}) => {
        const item = document.createElement('div');
        item.className = 'setting-item';
        item.style.opacity = disabled ? 0.6 : 1;

        // 生成选项HTML
        const optionsHtml = options.map(option => {
            const optionValue = typeof option === 'object' ? option.value : option;
            const optionLabel = typeof option === 'object' ? option.label : option;
            return `<option value="${optionValue}" ${optionValue === value ? 'selected' : ''}>${optionLabel}</option>`;
        }).join('');

        item.innerHTML = `
            <label>
                <span>${label}</span>
                <select class="select-input" ${disabled ? 'disabled' : ''}>
                    ${optionsHtml}
                </select>
            </label>
            <div class="setting-description">${description}</div>
        `;

        return item;
    };

    // 关闭弹窗函数
    const closeSettingsModal = () => {
        const overlay = document.getElementById('SettingsOverlay');
        if (overlay) {
            overlay.style.animation = 'fadeOut 0.2s';
            setTimeout(() => overlay.remove(), 200);
        }
    };

    /* ==================== 弹窗逻辑 ==================== */
    const showSettings = () => {
        if (document.getElementById('SettingsOverlay')) {
            return;
        }

        // 创建覆盖层
        const overlay = document.createElement('div');
        overlay.id = 'SettingsOverlay';

        // 创建弹窗
        const modal = document.createElement('div');
        modal.className = 'optimized-scroll-modal';

        // 创建头部
        const header = document.createElement('div');
        header.className = 'modal-header';
        header.innerHTML = `
            <span>${t.settingsTitle}</span>
        `;

        // 创建内容区域
        const body = document.createElement('div');
        body.className = 'modal-body settings-body scrollable-modal-body';

        // 自动滚动开关
        const autoScroll = createSwitchItem({
                                                label: t.autoScrollLabel,
                                                description: t.autoScrollDesc,
                                                checked: GM_getValue("autoScrollSwitch", false),
                                            });

        // 文件打包开关
        const filePack = createSwitchItem({
                                              label: t.filePackLabel,
                                              description: t.filePackDesc,
                                              checked: GM_getValue("packageDownloadFiles", true),
                                          });

        // 滚动次数设置
        const scrollCount = createNumberInput({
                                                  label: t.scrollCountLabel,
                                                  description: t.scrollCountDesc,
                                                  value: GM_getValue("maxScrollCount", 50),
                                                  min: 10,
                                                  max: 9999,
                                                  disabled: !GM_getValue("autoScrollSwitch", false),
                                              });

        const linkCheckboxSwitch = createSwitchItem({
                                                        label: t.linkCheckboxSwitchLabel,
                                                        description: t.linkCheckboxSwitchDesc,
                                                        checked: GM_getValue("linkCheckboxSwitch", true),
                                                    });

        const imageCheckboxSwitch = createSwitchItem({
                                                         label: t.imageCheckboxSwitchLabel,
                                                         description: t.imageCheckboxSwitchDesc,
                                                         checked: GM_getValue("imageCheckboxSwitch", true),
                                                     });

        const keepMenuVisible = createSwitchItem({
                                                     label: t.keepMenuVisibleLabel,
                                                     description: t.keepMenuVisibleDesc,
                                                     checked: GM_getValue("keepMenuVisible", false),
                                                 });

        const scriptServerURL = createTextInput({
                                                    label: t.scriptServerURLLabel,
                                                    description: t.scriptServerURLDesc,
                                                    placeholder: defaultsWebSocketURL,
                                                    value: GM_getValue("scriptServerURL", defaultsWebSocketURL),
                                                    disabled: !GM_getValue("scriptServerSwitch", false),
                                                });

        const scriptServerSwitch = createSwitchItem({
                                                        label: t.scriptServerSwitchLabel,
                                                        description: t.scriptServerSwitchDesc,
                                                        checked: GM_getValue("scriptServerSwitch", false),
                                                    });

        const imageDownloadFormat = createSelectItem({
                                                         label: t.imageDownloadFormatLabel,
                                                         description: t.imageDownloadFormatDesc,
                                                         options: ["PNG", "WEBP", "JPEG", "HEIC"],
                                                         value: GM_getValue("imageDownloadFormat", "jpeg")
                                                             .toUpperCase(),
                                                     });

        const videoPreference = createSelectItem({
                                                     label: t.videoPreferenceLabel,
                                                     description: t.videoPreferenceDesc,
                                                     options: Object.entries(t.videoPreferenceOptions)
                                                                    .map(([value, label]) => ({
                                                                        value,
                                                                        label,
                                                                    })),
                                                     value: config.videoPreference,
                                                 });

        const nameFormat = createFileNameFormatEditor({
                                                          label: t.fileNameFormatLabel,
                                                          description: t.fileNameFormatDesc,
                                                          value: config.fileNameFormatKeys,
                                                      });

        // 绑定自动滚动开关控制次数输入
        autoScroll.querySelector('input').addEventListener('change', (e) => {
            scrollCount.querySelector('input').disabled = !e.target.checked;
            scrollCount.querySelector('.number-input').style.opacity = e.target.checked ? 1 : 0.6;
        });
        scriptServerSwitch.querySelector('input').addEventListener('change', (e) => {
            scriptServerURL.querySelector('input').disabled = !e.target.checked;
            scriptServerURL.querySelector('.text-input').style.opacity = e.target.checked ? 1 : 0.6;
        });

        const createSettingsGroup = (title, items, wide = false) => {
            const group = document.createElement('div');
            group.className = `settings-group${wide ? ' wide' : ''}`;

            const groupTitle = document.createElement('div');
            groupTitle.className = 'settings-group-title';
            groupTitle.textContent = title;
            group.appendChild(groupTitle);

            const groupContent = document.createElement('div');
            groupContent.className = 'settings-group-content';
            items.forEach(item => groupContent.appendChild(item));
            group.appendChild(groupContent);
            return group;
        };

        // 组合内容
        body.appendChild(createSettingsGroup(
            t.downloadSettingsGroup,
            [filePack, imageCheckboxSwitch, imageDownloadFormat, videoPreference, nameFormat],
            true
        ));
        body.appendChild(createSettingsGroup(t.extractSettingsGroup, [autoScroll, scrollCount, linkCheckboxSwitch]));
        body.appendChild(createSettingsGroup(t.displaySettingsGroup, [keepMenuVisible]));
        body.appendChild(createSettingsGroup(t.serverSettingsGroup, [scriptServerSwitch, scriptServerURL]));

        // 创建底部按钮
        const footer = document.createElement('div');
        footer.className = 'modal-footer';
        const saveBtn = document.createElement('button');
        saveBtn.className = 'primary-btn';
        saveBtn.textContent = t.saveSettingsButton;
        const cancelBtn = document.createElement('button');
        cancelBtn.className = 'secondary-btn';
        cancelBtn.textContent = t.cancelSettingsButton;
        footer.appendChild(saveBtn);
        footer.appendChild(cancelBtn);

        // 组装弹窗
        modal.appendChild(header);
        modal.appendChild(body);
        modal.appendChild(footer);
        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        // 保存事件
        saveBtn.addEventListener('click', () => {
            updateAutoScrollSwitch(autoScroll.querySelector('input').checked);
            updatePackageDownloadFiles(filePack.querySelector('input').checked);
            updateKeepMenuVisible(keepMenuVisible.querySelector('input').checked);
            updateLinkCheckboxSwitch(linkCheckboxSwitch.querySelector('input').checked);
            updateImageCheckboxSwitch(imageCheckboxSwitch.querySelector('input').checked);
            updateMaxScrollCount(parseInt(scrollCount.querySelector('input').value) || 50)
            updateScriptServerURL(scriptServerURL.querySelector('.text-input').value.trim() || defaultsWebSocketURL);
            updateScriptServerSwitch(scriptServerSwitch.querySelector('input').checked);
            updateImageDownloadFormat(imageDownloadFormat.querySelector('select').value.trim() || "jpeg");
            updateVideoPreference(videoPreference.querySelector('select').value);
            updateFileNameFormat(nameFormat.getFileNameFormatKeys());
            closeSettingsModal();
        });

        // 关闭事件
        cancelBtn.addEventListener('click', closeSettingsModal);
        overlay.addEventListener('click', (e) => e.target === overlay && closeSettingsModal());
    };

    /* ==================== 样式定义 ==================== */
    style = document.createElement('style');
    style.textContent = `
    /* 图片选择弹窗：仅容器尺寸与自身网格等特有样式 */
    .image-selection-modal {
        background: white;
        border-radius: 16px;
        width: 80%;
        max-width: 900px;
        max-height: 90vh;
        box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
        overflow: hidden;
        animation: scaleUp 0.3s;
        display: flex;
        flex-direction: column;
    }

    /* 图片网格等仅此弹窗拥有的样式 */
    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 12px;
    }
    .image-item {
        position: relative;
        border-radius: 8px;
        overflow: hidden;
        cursor: pointer;
        transition: all 0.2s;
        border: 2px solid transparent;
        aspect-ratio: 3 / 4;
        background:
            conic-gradient(#eee 25%, transparent 0 50%, #eee 0 75%, transparent 0)
            0 0/16px 16px #fafafa;
    }
    .image-item img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        object-position: center;
        border-radius: 6px;
        display: block;
    }
    .image-item.selected { border-color: #2196F3; }

    .image-checkbox {
        position: absolute;
        top: 8px;
        right: 8px;
        width: 20px;
        height: 20px;
        opacity: 0;
    }
    .image-checkbox + label {
        position: absolute;
        top: 8px;
        right: 8px;
        width: 20px;
        height: 20px;
        background: white;
        border: 1px solid #ccc;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: all 0.2s;
    }
    .image-checkbox:checked + label {
        background: #2196F3;
        border-color: #2196F3;
    }
    .image-checkbox:checked + label::after {
        content: "✓";
        color: white;
        font-size: 12px;
    }
    `;
    document.head.appendChild(style);

    // 关闭弹窗函数
    const closeImagesModal = () => {
        const overlay = document.getElementById('imageSelectionOverlay');
        if (overlay) {
            overlay.style.animation = 'fadeOut 0.2s';
            setTimeout(() => overlay.remove(), 200);
        }
    };

    /* ==================== 弹窗逻辑 ==================== */
    const showImageSelectionModal = (imageUrls, name, server = false,) => {
        return new Promise((resolve,) => {
            if (document.getElementById('imageSelectionOverlay')) {
                return;
            }

            // 创建覆盖层
            const overlay = document.createElement('div');
            overlay.id = 'imageSelectionOverlay';

            // 创建弹窗
            const modal = document.createElement('div');
            modal.className = 'image-selection-modal';

            // 创建头部
            const header = document.createElement('div');
            header.className = 'modal-header';
            header.innerHTML = `
            <span>${t.imageCheckboxTitle}</span>
        `;

            // 创建内容区域
            const body = document.createElement('div');
            body.className = 'modal-body scrollable-modal-body';

            // 创建图片网格
            const imageGrid = document.createElement('div');
            imageGrid.className = 'image-grid';

            // 动态生成图片项
            imageUrls.forEach((image) => {
                const item = document.createElement('div');
                item.className = 'image-item';

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'image-checkbox';
                checkbox.id = `image-checkbox-${image.index}`;
                checkbox.checked = true;

                const label = document.createElement('label');
                label.htmlFor = `image-checkbox-${image.index}`;

                const img = document.createElement('img');
                img.src = image.webp;
                img.index = image.index;
                img.url = image.url;
                img.alt = `图片_${image.index}`;

                item.appendChild(checkbox);
                item.appendChild(label);
                item.appendChild(img);

                // 绑定点击事件
                item.addEventListener('click', (e) => {
                    if (e.target.tagName !== 'INPUT') {
                        checkbox.checked = !checkbox.checked;
                        item.classList.toggle('selected', checkbox.checked);
                    }
                });

                imageGrid.appendChild(item);
            });

            body.appendChild(imageGrid);

            // 创建底部按钮
            const footer = document.createElement('div');
            footer.className = 'modal-footer';
            // 新增：全选 / 全不选
            const selectAllBtn = document.createElement('button');
            selectAllBtn.className = 'secondary-btn';
            selectAllBtn.textContent = t.selectAllButton;

            const selectNoneBtn = document.createElement('button');
            selectNoneBtn.className = 'secondary-btn';
            selectNoneBtn.textContent = t.deselectAllButton;

            const confirmBtn = document.createElement('button');
            confirmBtn.className = 'primary-btn';
            confirmBtn.textContent = t.startDownloadButton;

            const closeBtn = document.createElement('button');
            closeBtn.className = 'secondary-btn';
            closeBtn.textContent = t.closeDownloadButton;

            footer.appendChild(selectAllBtn);
            footer.appendChild(selectNoneBtn);
            footer.appendChild(confirmBtn);
            footer.appendChild(closeBtn);

            // 组装弹窗
            modal.appendChild(header);
            modal.appendChild(body);
            modal.appendChild(footer);
            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            // 确认事件
            confirmBtn.addEventListener('click', async () => {
                const selectedImages = Array.from(document.querySelectorAll('.image-checkbox:checked'))
                                            .map((checkbox) => {
                                                let item = checkbox.parentElement.querySelector('img');
                                                return {
                                                    index: item.index, url: item.url,
                                                }
                                            });
                if (selectedImages.length === 0) {
                    showToast(t.imageSelectionTip);
                    return;
                }
                closeImagesModal();
                if (server) {
                    resolve(selectedImages.map(item => item.index));
                } else {
                    showToast(t.downloadTips);
                    await downloadImage(selectedImages, name)
                }
            });

            // 关闭事件
            closeBtn.addEventListener('click', closeImagesModal);
            overlay.addEventListener('click', (e) => e.target === overlay && closeImagesModal());

            const setAllChecked = (checked) => {
                const items = imageGrid.querySelectorAll('.image-item');
                items.forEach((item) => {
                    const box = item.querySelector('.image-checkbox');
                    if (!box || box.disabled) return;
                    box.checked = checked;
                    item.classList.toggle('selected', checked);
                });
            };

            // 全选 / 全不选
            selectAllBtn.addEventListener('click', () => setAllChecked(true));
            selectNoneBtn.addEventListener('click', () => setAllChecked(false));
        })
    };

    (() => {
        if (!document.getElementById('listSelectionStyle')) {
            const style = document.createElement('style');
            style.id = 'listSelectionStyle';
            style.textContent = `
            /* 列表弹窗容器，仅定义差异尺寸，其他沿用通用 modal 样式 */
            .list-selection-modal {
                background: #fff;
                border-radius: 16px;
                width: 80%;
                max-width: 800px;
                max-height: 80vh;
                box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
                overflow: hidden;
                animation: scaleUp 0.3s;
                display: flex;
                flex-direction: column;
            }

            /* 列表容器 */
            .list-container {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }

            /* 列表项 */
            .list-item {
                display: grid;
                grid-template-columns: 32px 0px 64px 1fr; /* 序号、复选框、缩略图、文本区 */
                align-items: center;
                gap: 8px;
                padding: 8px;
                border: 1px solid #eee;
                border-radius: 10px;
                transition: background 0.15s, border-color 0.15s, box-shadow 0.15s;
                cursor: pointer;
            }
            .list-item:hover {
                background: #fafafa;
                border-color: #e6e6e6;
            }
            .list-item.selected {
                border-color: #2196F3;
                box-shadow: 0 0 0 4px rgba(33,150,243,0.12) inset;
            }

            /* 序号样式 */
            .list-number {
                text-align: center;
            }

            /* 复选框样式（使用原生复选框以保证可访问性与简单性） */
            .list-checkbox {
                width: 18px;
                height: 18px;
                margin: 0 0 0 2px;
                cursor: pointer;
            }

            /* 缩略图 */
            .list-thumb {
                width: 64px;
                height: 64px;
                object-fit: cover;
                border-radius: 8px;
                user-select: none;
                pointer-events: none; /* 点击行切换选择，避免图片拦截点击 */
                background: #f2f2f2;
            }

            /* 文本区 */
            .list-texts {
                display: flex;
                flex-direction: column;
                min-width: 0; /* 允许文本正确换行截断 */
            }
            .list-author {
                font-size: 0.95rem;
                color: #212121;
                font-weight: 500;
                line-height: 1.4;
                word-break: break-word;
            }
            .list-title {
                margin-top: 4px;
                font-size: 0.85rem;
                color: #757575;
                line-height: 1.4;
                word-break: break-word;
            }
        `;
            document.head.appendChild(style);
        }
    })();

    /**
     * 显示列表选择弹窗
     * @param {Array<{id:any, image:string, author:string, title:string}>} list
     * @param {Object} [options]
     * @param {string} [options.title='请选择'] 弹窗标题
     * @param {string} [options.confirmText='确认'] 确认按钮文本
     * @param {string} [options.cancelText='取消'] 取消按钮文本
     * @param {boolean} [options.prechecked=true] 是否默认勾选全部
     * @returns {Promise<Array|null>} 点击确认返回选中项数组；取消/关闭返回 null
     */
    function showListSelectionModal(list, options = {}) {
        const {
            title = t.itemsExtractTip,
            confirmText = t.itemsExtractConfirm,
            cancelText = t.itemsExtractCancel,
            prechecked = true,
        } = options;

        if (document.getElementById('listSelectionOverlay')) return Promise.resolve(null);

        return new Promise((resolve) => {
            // 覆盖层
            const overlay = document.createElement('div');
            overlay.id = 'listSelectionOverlay';
            overlay.style.cssText = `
            position: fixed; inset: 0; background: rgba(0,0,0,0.32);
            backdrop-filter: blur(4px); display: flex; justify-content: center; align-items: center;
            z-index: 10000; animation: fadeIn 0.3s;
        `;

            // 弹窗
            const modal = document.createElement('div');
            modal.className = 'list-selection-modal';

            // 头部
            const header = document.createElement('div');
            header.className = 'modal-header';
            header.innerHTML = `<span>${title}</span>`;

            // 内容
            const body = document.createElement('div');
            body.className = 'modal-body scrollable-modal-body';

            const container = document.createElement('div');
            container.className = 'list-container';

            // id -> item 映射
            const map = new Map();
            list.forEach((item, index) => {
                const row = document.createElement('div');
                row.className = 'list-item';
                row.dataset.key = item.id;

                // 添加序号
                const number = document.createElement('div');
                number.className = 'list-number';
                number.textContent = (index + 1).toString();

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'list-checkbox';
                checkbox.checked = prechecked;

                const img = document.createElement('img');
                img.className = 'list-thumb';
                img.src = item.image || '';
                img.alt = 'thumb';

                const texts = document.createElement('div');
                texts.className = 'list-texts';
                const author = document.createElement('div');
                author.className = 'list-author';
                author.textContent = item.author ?? '';
                const title = document.createElement('div');
                title.className = 'list-title';
                title.textContent = item.title ?? '';
                texts.appendChild(author);
                texts.appendChild(title);

                row.appendChild(number);
                row.appendChild(checkbox);
                row.appendChild(img);
                row.appendChild(texts);

                if (checkbox.checked) row.classList.add('selected');

                row.addEventListener('click', (e) => {
                    if ((e.target instanceof HTMLElement) && e.target.classList.contains('list-checkbox')) return;
                    checkbox.checked = !checkbox.checked;
                    row.classList.toggle('selected', checkbox.checked);
                });

                checkbox.addEventListener('change', () => {
                    row.classList.toggle('selected', checkbox.checked);
                });

                map.set(row.dataset.key, item);
                container.appendChild(row);
            });

            body.appendChild(container);

            // 底部按钮
            const footer = document.createElement('div');
            footer.className = 'modal-footer';

            // 新增：全选 / 全不选
            const selectAllBtn = document.createElement('button');
            selectAllBtn.className = 'secondary-btn';
            selectAllBtn.textContent = t.selectAllButton;

            const selectNoneBtn = document.createElement('button');
            selectNoneBtn.className = 'secondary-btn';
            selectNoneBtn.textContent = t.deselectAllButton;

            // 右侧操作：确认 / 取消
            const confirmBtn = document.createElement('button');
            confirmBtn.className = 'primary-btn';
            confirmBtn.textContent = confirmText;

            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'secondary-btn';
            cancelBtn.textContent = cancelText;

            // 将按钮加入 footer（顺序：全选、全不选、确认、取消）
            footer.appendChild(selectAllBtn);
            footer.appendChild(selectNoneBtn);
            footer.appendChild(confirmBtn);
            footer.appendChild(cancelBtn);

            // 组装
            modal.appendChild(header);
            modal.appendChild(body);
            modal.appendChild(footer);
            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            // 辅助：批量设置选择状态
            const setAllChecked = (checked) => {
                container.querySelectorAll('.list-item').forEach((row) => {
                    const box = row.querySelector('.list-checkbox');
                    if (box) {
                        box.checked = checked;
                        row.classList.toggle('selected', checked);
                    }
                });
            };

            // 关闭
            const close = (result) => {
                overlay.style.animation = 'fadeOut 0.2s';
                setTimeout(() => {
                    overlay.remove();
                    resolve(result);
                }, 200);
            };

            // 事件绑定
            selectAllBtn.addEventListener('click', () => setAllChecked(true));
            selectNoneBtn.addEventListener('click', () => setAllChecked(false));
            cancelBtn.addEventListener('click', () => close(null));
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) close(null);
            });
            confirmBtn.addEventListener('click', () => {
                const selected = [];
                container.querySelectorAll('.list-item').forEach((row) => {
                    const checkbox = row.querySelector('.list-checkbox');
                    if (checkbox && checkbox.checked) {
                        const {key} = row.dataset;
                        if (map.has(key)) selected.push(map.get(key));
                    }
                });
                close(selected);
            });
        });
    }

    // 悬浮图标位置常量
    const iconPositionStorageKey = "floatingIconPosition";
    const iconViewportMargin = 8;
    const menuViewportMargin = 8;
    const menuGap = 12;
    const iconDragThreshold = 4;

    // 悬浮图标位置工具
    const clamp = (value, min, max) => {
        const safeMax = Math.max(min, max);
        return Math.min(Math.max(value, min), safeMax);
    };

    const getIconSize = () => config.icon[config.icon.type].size;

    const clampIconPosition = (left, top) => {
        const size = getIconSize();
        return {
            left: clamp(left, iconViewportMargin, window.innerWidth - size - iconViewportMargin),
            top: clamp(top, iconViewportMargin, window.innerHeight - size - iconViewportMargin),
        };
    };

    const applyIconPosition = (target, position) => {
        target.style.left = `${position.left}px`;
        target.style.top = `${position.top}px`;
        target.style.right = 'auto';
        target.style.bottom = 'auto';
    };

    const applyDefaultIconPosition = (target) => {
        target.style.left = 'auto';
        target.style.top = config.position.top;
        target.style.right = config.position.right;
        target.style.bottom = 'auto';
    };

    const getCurrentIconPosition = (target) => {
        const rect = target.getBoundingClientRect();
        return clampIconPosition(rect.left, rect.top);
    };

    const readStoredIconPosition = () => {
        const position = GM_getValue(iconPositionStorageKey, null);
        if (!position || typeof position.left !== 'number' || typeof position.top !== 'number') {
            return null;
        }
        return clampIconPosition(position.left, position.top);
    };

    // 创建主图标
    const createIcon = () => {
        const icon = document.createElement('div');
        icon.style = `
            position: fixed;
            top: ${config.position.top};
            right: ${config.position.right};
            width: ${config.icon[config.icon.type].size}px;
            height: ${config.icon[config.icon.type].size}px;
            background: white;
            border-radius: ${config.icon.image.borderRadius || '8px'};
            cursor: grab;
            z-index: 9999;
            box-shadow: 0 3px 5px rgba(0,0,0,0.12), 0 3px 5px rgba(0,0,0,0.24);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform ${config.animation.duration}s ${config.animation.easing}, box-shadow ${config.animation.duration}s ${config.animation.easing};
            touch-action: none;
            user-select: none;
            -webkit-user-drag: none;
        `;

        icon.style.backgroundImage = `url(${config.icon.image.url})`;
        icon.style.backgroundSize = 'cover';

        return icon;
    };

    // 创建菜单容器
    const menu = document.createElement('div');
    menu.style = `
        position: fixed;
        top: 0;
        left: 0;
        width: 255px;
        max-width: calc(100vw - 1rem);
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
        overflow: hidden;
        display: none;
        z-index: 9998;
        transform-origin: top center;
        transition: all ${config.animation.duration}s ${config.animation.easing};
        opacity: 0;
        transform: translateY(var(--menu-hidden-translate, 10px)) scaleY(0.95);
        will-change: transform, opacity;
    `;

    // 创建菜单内容容器
    const menuContent = document.createElement('div');
    menuContent.style = `
        max-height: 400px;
        overflow-y: auto;
        overscroll-behavior: contain;
    `;
    menu.appendChild(menuContent);

    let icon;
    let hideTimeout;
    let hideAnimationTimeout;
    let isMenuVisible = false;
    let isDraggingIcon = false;
    let menuHiddenTranslate = '10px';

    const getMenuMaxHeight = (availableSpace) => {
        const viewportMaxHeight = Math.max(0, window.innerHeight - menuViewportMargin * 2);
        const minimumVisibleHeight = Math.min(120, viewportMaxHeight);
        return Math.min(400, viewportMaxHeight, Math.max(availableSpace, minimumVisibleHeight));
    };

    const positionMenu = () => {
        if (!icon) {
            return;
        }
        const iconRect = icon.getBoundingClientRect();
        const iconCenterX = iconRect.left + iconRect.width / 2;
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        menuContent.style.maxHeight = '400px';
        const naturalHeight = menu.offsetHeight;
        const availableBelow = viewportHeight - iconRect.bottom - menuGap - menuViewportMargin;
        const availableAbove = iconRect.top - menuGap - menuViewportMargin;
        const openAbove = availableBelow < naturalHeight && availableAbove > availableBelow;
        const availableHeight = openAbove ? availableAbove : availableBelow;
        menuContent.style.maxHeight = `${getMenuMaxHeight(availableHeight)}px`;

        const menuWidth = menu.offsetWidth;
        const menuHeight = menu.offsetHeight;
        const left = clamp(
            iconCenterX - menuWidth / 2,
            menuViewportMargin,
            viewportWidth - menuWidth - menuViewportMargin
        );
        const top = clamp(
            openAbove ? iconRect.top - menuGap - menuHeight : iconRect.bottom + menuGap,
            menuViewportMargin,
            viewportHeight - menuHeight - menuViewportMargin
        );
        const originX = clamp(iconCenterX - left, 16, menuWidth - 16);

        menuHiddenTranslate = openAbove ? '-10px' : '10px';
        menu.style.setProperty('--menu-hidden-translate', menuHiddenTranslate);
        menu.style.left = `${left}px`;
        menu.style.top = `${top}px`;
        menu.style.right = 'auto';
        menu.style.bottom = 'auto';
        menu.style.transformOrigin = `${originX}px ${openAbove ? '100%' : '0'}`;
    };

    const saveIconPosition = () => {
        const position = getCurrentIconPosition(icon);
        applyIconPosition(icon, position);
        GM_setValue(iconPositionStorageKey, position);
    };

    const syncFloatingControlsToViewport = () => {
        const position = getCurrentIconPosition(icon);
        applyIconPosition(icon, position);
        if (isMenuVisible) {
            positionMenu();
        }
    };

    const initializeIconPosition = () => {
        applyDefaultIconPosition(icon);
        const defaultPosition = getCurrentIconPosition(icon);
        const position = readStoredIconPosition() || defaultPosition;
        applyIconPosition(icon, position);
        GM_setValue(iconPositionStorageKey, position);
    };

    function resetIconPosition() {
        if (!icon) {
            return;
        }
        applyDefaultIconPosition(icon);
        const position = getCurrentIconPosition(icon);
        applyIconPosition(icon, position);
        GM_setValue(iconPositionStorageKey, position);
        if (isMenuVisible) {
            positionMenu();
        }
        showToast(t.resetIconPositionTip, 2000);
    }

    // 初始化样式
    style = document.createElement('style');
    style.textContent = `
        :root {
            --primary: #2196F3;
            --surface: #ffffff;
            --on-surface: #212121;
            --ripple-color: rgba(33, 150, 243, 0.15);
            --border-radius: 12px;
        }

        .menu-item {
            display: flex;
            padding: 1rem 1.5rem;
            cursor: pointer;
            position: relative;
            transition: all 0.2s ease;
            align-items: center;
        }

        .menu-item:hover {
            background: var(--ripple-color);
        }

        .menu-item:not(:last-child) {
            border-bottom: 1px solid #eee;
        }

        .icon-container {
            margin-right: 1rem;
            display: flex;
            align-items: center;
        }

        .material-icons {
            font-size: 24px;
            color: var(--primary);
        }

        .content {
            flex: 1;
        }

        .menuTitle {
            font-size: 0.95rem;
            color: var(--on-surface);
            font-weight: 500;
            margin-bottom: 2px;
        }

        .subtitle {
            font-size: 0.75rem;
            color: #757575;
            line-height: 1.4;
        }

        .menu-enter {
            animation: slideIn ${config.animation.duration}s ${config.animation.easing};
        }

        .menu-exit {
            animation: slideOut ${config.animation.duration}s ${config.animation.easing};
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(var(--menu-hidden-translate, 10px)) scaleY(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scaleY(1);
            }
        }

        @keyframes slideOut {
            from {
                opacity: 1;
                transform: translateY(0) scaleY(1);
            }
            to {
                opacity: 0;
                transform: translateY(var(--menu-hidden-translate, 10px)) scaleY(0.95);
            }
        }

        .ripple {
            position: absolute;
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            background: var(--ripple-color);
            pointer-events: none;
        }

        @keyframes ripple {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }

        /* 滚动条样式 */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
        }
    `;
    document.head.appendChild(style);

    // 创建并显示一个自动消失的消息弹窗（Toast）
    function showToast(message, duration = 5000) {
        const toast = document.createElement('div');
        toast.textContent = message;

        // 基础样式（可按需调整）
        Object.assign(toast.style, {
            position: 'fixed',
            left: '50%',
            bottom: '10rem',
            transform: 'translateX(-50%)',
            maxWidth: '80vw',
            padding: '10px 16px',
            background: 'rgba(128, 128, 128, 0.6)',
            color: '#fff',
            fontSize: '16px',
            lineHeight: '1.4',
            borderRadius: '8px',
            boxShadow: '0 6px 16px rgba(0,0,0,0.25)',
            zIndex: '99999',
            opacity: '0',
            transition: 'opacity 200ms ease',
            pointerEvents: 'none',
            whiteSpace: 'pre-wrap',
            textAlign: 'center',
        });

        document.body.appendChild(toast);

        // 触发淡入
        requestAnimationFrame(() => {
            toast.style.opacity = '1';
        });

        // 指定时间后淡出并移除
        const hide = () => {
            toast.style.opacity = '0';
            const remove = () => {
                toast.removeEventListener('transitionend', remove);
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            };
            toast.addEventListener('transitionend', remove);
        };

        setTimeout(hide, duration);
    }

    // 涟漪效果
    const createRipple = e => {
        const target = e.currentTarget;
        const rect = target.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;

        target.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    };

    // 隐藏菜单
    const hideMenu = (force = false) => {
        clearTimeout(hideTimeout);
        clearTimeout(hideAnimationTimeout);
        if (config.keepMenuVisible && !force) {
            return;
        }
        const runHide = () => {
            menu.classList.remove('menu-enter');
            if (force) {
                menu.classList.remove('menu-exit');
                menu.style.display = 'none';
                menu.style.opacity = 0;
                menu.style.transform = `translateY(${menuHiddenTranslate}) scaleY(0.95)`;
                isMenuVisible = false;
                return;
            }
            menu.classList.add('menu-exit');
            menu.style.opacity = 0;
            menu.style.transform = `translateY(${menuHiddenTranslate}) scaleY(0.95)`;

            hideAnimationTimeout = setTimeout(() => {
                menu.style.display = 'none';
                menu.classList.remove('menu-exit');
                isMenuVisible = false;
            }, config.animation.duration * 1000);
        };
        if (force) {
            runHide();
        } else {
            hideTimeout = setTimeout(runHide, 100);
        }
    };

    const keepMenuOpen = () => {
        clearTimeout(hideTimeout);
        clearTimeout(hideAnimationTimeout);
        if (!isMenuVisible) {
            return;
        }
        menu.classList.remove('menu-exit');
        menu.style.display = 'block';
        menu.style.opacity = 1;
        menu.style.transform = 'translateY(0) scaleY(1)';
    };

    let currentUrl, currentSite = null;
    const currentSitePattern = /www\.(xiaohongshu|rednote)\.com/;

    // 动态生成菜单内容
    const updateMenuContent = () => {
        menuContent.innerHTML = '';

        // 根据URL生成不同菜单项
        currentUrl = window.location.href;
        const menuItems = [];

        if (!config.disclaimer) {
            menuItems.push({
                               text: 'README', icon: ' 📄 ', action: readme, description: t.readmeMenuTitle
                           },);
        } else if (currentUrl === `https://www.${currentSite}.com/explore` || currentUrl.includes(
            `https://www.${currentSite}.com/explore?`)) {
            menuItems.push({
                               text: t.extractRecommendLinksText,
                               icon: ' ⛓ ',
                               action: () => extractAllLinksEvent(-1),
                               description: t.extractRecommendLinksDescription
                           },);
        } else if (currentUrl.includes(`https://www.${currentSite}.com/explore/`) || currentUrl.includes(
            `https://www.${currentSite}.com/discovery/item/`)) {
            menuItems.push({
                               text: t.downloadNoteFilesText,
                               icon: ' 📦 ',
                               action: () => extractDownloadLinks(false),
                               description: t.downloadNoteFilesDescription
                           },);
            if (config.scriptServerSwitch) {
                menuItems.push({
                                   text: t.pushDownloadTaskText,
                                   icon: ' 🌏 ',
                                   action: () => extractDownloadLinks(true),
                                   description: t.pushDownloadTaskDescription
                               });
            }
        } else if (currentUrl.includes(`https://www.${currentSite}.com/user/profile/`)) {
            menuItems.push({
                               text: t.extractPublishedLinksText,
                               icon: ' ⛓ ',
                               action: () => extractAllLinksEvent(0),
                               description: t.extractPublishedLinksDescription
                           }, {
                               text: t.extractLikedLinksText,
                               icon: ' ⛓ ',
                               action: () => extractAllLinksEvent(2),
                               description: t.extractLikedLinksDescription
                           }, {
                               text: t.extractSavedLinksText,
                               icon: ' ⛓ ',
                               action: () => extractAllLinksEvent(1),
                               description: t.extractSavedLinksDescription
                           },);
        } else if (currentUrl.includes(`https://www.${currentSite}.com/search_result`)) {
            menuItems.push({
                               text: t.extractSearchNoteLinksText,
                               icon: ' ⛓ ',
                               action: () => extractAllLinksEvent(3),
                               description: t.extractSearchNoteLinksDescription
                           }, {
                               text: t.extractSearchUsersLinksText,
                               icon: ' ⛓ ',
                               action: () => extractAllLinksEvent(4),
                               description: t.extractSearchUsersLinksDescription
                           },);
        } else if (currentUrl.includes(`https://www.${currentSite}.com/board/`)) {
            menuItems.push({
                               text: t.extractAlbumNotesLinksText,
                               icon: ' ⛓ ',
                               action: () => extractAllLinksEvent(5),
                               description: t.extractAlbumNotesLinksDescription
                           },);
        }

        // 常用功能
        menuItems.push({
                           separator: true
                       }, {
            text: t.modifyScriptSettingsText,
            icon: ' ⚙️ ',
            action: showSettings,
            description: t.modifyScriptSettingsDescription
                       }, {
                           text: t.aboutXHSText, icon: ' 📒 ', action: about, description: t.aboutXHSDescription
                       });

        // 创建菜单项
        menuItems.forEach(item => {
            if (item.separator) {
                const divider = document.createElement('div');
                divider.style = `
                    height: 8px;
                    background: #f5f5f5;
                `;
                menuContent.appendChild(divider);
                return;
            }

            const btn = document.createElement('div');
            btn.className = 'menu-item';
            btn.innerHTML = `
                <div class="icon-container">
                    <span class="material-icons">${item.icon}</span>
                </div>
                <div class="content">
                    <div class="menuTitle">${item.text}</div>
                    <div class="subtitle">${item.description}</div>
                </div>
            `;

            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                item.action();
                hideMenu();
            });

            btn.addEventListener('mousedown', createRipple);

            menuContent.appendChild(btn);
        });
    };

    // URL监测相关
    let lastUrl = window.location.href;
    let currentSiteMatch = lastUrl.match(currentSitePattern);
    if (currentSiteMatch) {
        currentSite = currentSiteMatch[1];
    } else {
        abnormal(t.scriptInternalError);
    }

    // 显示菜单
    const showMenu = () => {
        if (isDraggingIcon) {
            return;
        }
        clearTimeout(hideTimeout);
        clearTimeout(hideAnimationTimeout);
        updateMenuContent();
        menu.style.display = 'block';
        menu.style.visibility = 'hidden';
        menu.classList.remove('menu-enter', 'menu-exit');
        menu.style.opacity = 0;
        positionMenu();
        menu.style.transform = `translateY(${menuHiddenTranslate}) scaleY(0.95)`;
        void menu.offsetHeight; // 触发重绘
        menu.style.visibility = 'visible';
        menu.classList.add('menu-enter');
        menu.style.opacity = 1;
        menu.style.transform = 'translateY(0) scaleY(1)';
        isMenuVisible = true;
    };

    const setupIconDragging = () => {
        let dragState = null;

        const stopDrag = (event) => {
            if (!dragState || event.pointerId !== dragState.pointerId) {
                return;
            }
            const wasDragging = dragState.dragging;
            dragState = null;
            window.removeEventListener('pointermove', moveDrag);
            window.removeEventListener('pointerup', stopDrag);
            window.removeEventListener('pointercancel', stopDrag);
            try {
                icon.releasePointerCapture(event.pointerId);
            } catch (_) {
            }
            icon.style.transition = '';
            icon.style.cursor = 'grab';
            isDraggingIcon = false;
            if (wasDragging) {
                saveIconPosition();
                requestAnimationFrame(() => {
                    if (config.keepMenuVisible || icon.matches(':hover')) {
                        showMenu();
                    }
                });
            }
        };

        const moveDrag = (event) => {
            if (!dragState || event.pointerId !== dragState.pointerId) {
                return;
            }
            const deltaX = event.clientX - dragState.startClientX;
            const deltaY = event.clientY - dragState.startClientY;

            if (!dragState.dragging) {
                if (Math.hypot(deltaX, deltaY) < iconDragThreshold) {
                    return;
                }
                dragState.dragging = true;
                isDraggingIcon = true;
                hideMenu(true);
                icon.style.transition = 'none';
                icon.style.cursor = 'grabbing';
            }

            event.preventDefault();
            applyIconPosition(icon, clampIconPosition(
                dragState.startLeft + deltaX,
                dragState.startTop + deltaY
            ));
        };

        icon.addEventListener('pointerdown', (event) => {
            if (event.button !== 0) {
                return;
            }
            const rect = icon.getBoundingClientRect();
            dragState = {
                pointerId: event.pointerId,
                startClientX: event.clientX,
                startClientY: event.clientY,
                startLeft: rect.left,
                startTop: rect.top,
                dragging: false,
            };
            try {
                icon.setPointerCapture(event.pointerId);
            } catch (_) {
            }
            window.addEventListener('pointermove', moveDrag, {passive: false});
            window.addEventListener('pointerup', stopDrag);
            window.addEventListener('pointercancel', stopDrag);
        });
    };

    // 事件监听
    icon = createIcon();
    setupIconDragging();
    icon.addEventListener('mouseenter', showMenu);
    icon.addEventListener('mouseleave', () => hideMenu());
    menu.addEventListener('mouseenter', keepMenuOpen);
    menu.addEventListener('mouseleave', () => hideMenu());
    window.addEventListener('resize', syncFloatingControlsToViewport);

    // URL变化监听
    const setupUrlListener = () => {
        const observeUrl = () => {
            if (window.location.href !== lastUrl) {
                lastUrl = window.location.href;
                currentSiteMatch = lastUrl.match(currentSitePattern);
                if (currentSiteMatch) {
                    currentSite = currentSiteMatch[1];
                    if (isMenuVisible) {
                        updateMenuContent();
                        positionMenu();
                    }
                } else {
                    currentSite = null;
                    abnormal(t.scriptInternalError);
                }
            }
            requestAnimationFrame(observeUrl);
        };
        observeUrl();
    };

    // 添加到页面
    document.body.appendChild(icon);
    document.body.appendChild(menu);
    document.head.appendChild(style);
    initializeIconPosition();
    syncFloatingControlsToViewport();
    setupUrlListener();

    if (config.keepMenuVisible) {
        showMenu();
    }

    class WebSocketManager {
        constructor(url) {
            this.url = url;
            this.ws = null;
        }

        onOpen() {
        }

        onMessage(message) {

        }

        onClose(event) {

        }

        onError(error) {
            console.error('Script Server WebSocket error:', error);
            showToast(t.scriptServerError,);
        }

        get isConnected() {
            return this.ws && this.ws.readyState === WebSocket.OPEN;
        }

        connect() {
            if (this.ws && this.ws.readyState !== WebSocket.CLOSED) {
                return;
            }
            try {
                this.ws = new WebSocket(this.url);
                this.ws.onopen = (event) => this.onOpen(event);
                this.ws.onmessage = (event) => this.onMessage(event);
                this.ws.onclose = (event) => {
                    this.ws = null;
                    this.onClose(event);
                };
                this.ws.onerror = (event) => {
                    this.ws = null;
                    this.onError(event);
                };
            } catch (error) {
                this.onError(error);
            }
        }

        disconnect() {
            if (this.isConnected) {
                this.ws.close();
            }
        }

        send(data) {
            if (this.isConnected) {
                this.ws.send(data);
                showToast(t.pushTaskSuccess);
            } else {
                showToast(t.pushTaskError,);
            }
        }
    }

    const webSocket = new WebSocketManager(config.scriptServerURL,);

    if (config.scriptServerSwitch) {
        webSocket.connect();
    }
})();

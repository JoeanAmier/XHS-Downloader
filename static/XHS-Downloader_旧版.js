// ==UserScript==
// @name         XHS-Downloader
// @namespace    https://github.com/JoeanAmier/XHS-Downloader
// @version      1.8.8
// @description  提取小红书作品/用户链接，下载小红书无水印图文/视频作品文件
// @author       JoeanAmier
// @match        http*://xhslink.com/*
// @match        http*://www.xiaohongshu.com/explore*
// @match        http*://www.xiaohongshu.com/user/profile/*
// @match        http*://www.xiaohongshu.com/search_result*
// @match        http*://www.xiaohongshu.com/board/*
// @icon         data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMjAwMTA5MDQvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvVFIvMjAwMS9SRUMtU1ZHLTIwMDEwOTA0L0RURC9zdmcxMC5kdGQiPjxzdmcgdmVyc2lvbj0iMS4wIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNTYuMDAwMDAwcHQiIGhlaWdodD0iMjU2LjAwMDAwMHB0IiB2aWV3Qm94PSIwIDAgMjU2LjAwMDAwMCAyNTYuMDAwMDAwIiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCBtZWV0Ij48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLjAwMDAwMCwyNTYuMDAwMDAwKSBzY2FsZSgwLjEwMDAwMCwtMC4xMDAwMDApIiBmaWxsPSIjZTgzYjM1IiBzdHJva2U9Im5vbmUiPjxwYXRoIGQ9Ik0xMTI1IDI1NDMgYy02MyAtNyAtMjIxIC00NiAtMjgyIC02OSAtMTc3IC02NyAtMzIxIC0xNjAgLTQ1OSAtMjk4IC0xOTQgLTE5NCAtMzEzIC00MjIgLTM1OSAtNjgzIC0xOSAtMTExIC0xOSAtMzI2IDAgLTQzOSA3NCAtNDIzIDM3OCAtNzk4IDc3NiAtOTU4IDQ4OSAtMTk3IDEwMzUgLTgwIDEzOTkgMzAwIDEzOCAxNDUgMjM2IDMwNyAyOTQgNDg3IDg1IDI2MCA4MSA1NjYgLTEwIDgxOSAtMTU2IDQzNCAtNTM4IDc1NCAtOTkzIDgzMiAtODYgMTQgLTI4MiAyMCAtMzY2IDl6IG01MCAtODEwIGw4MCAtMzAgMyAtMzg5IDIgLTM5MCAtODcgMjkgYy0xMzIgNDQgLTMwMiA0OCAtNDQwIDExIGwtMjMgLTYgMCAzOTEgYzAgMjE1IDMgMzkxIDggMzkxIDQgMSAzMCA3IDU3IDE1IDM2IDExIDg5IDE0IDE4NSAxMSAxMjEgLTIgMTQzIC02IDIxNSAtMzN6IG02MzggMTggbDM3IC0xMiAwIC0zODkgYzAgLTIxNSAtMiAtMzkwIC00IC0zOTAgLTMgMCAtMzUgNyAtNzMgMTYgLTEwOCAyNSAtMjc0IDE1IC0zODUgLTIzIGwtODggLTMxIDAgMzg4IDAgMzg3IDM5IDE4IGMxMDAgNDQgMTYwIDU1IDMwMSA1MSA3NCAtMiAxNTIgLTkgMTczIC0xNXogbS0xMTQzIC00NTggYzAgLTE5NyA0IC0zNjQgOCAtMzcxIDcgLTkgMjUgLTggODcgOCAxNDUgMzcgMzE1IDI0IDQ1NiAtMzUgbDYxIC0yNiA3MSAzMCBjNDAgMTYgMTAwIDM1IDEzNSA0MSA4MSAxNiAyNzEgOCAzMzIgLTE0IDI0IC05IDUwIC0xNCA1NyAtMTIgMTAgNCAxMyA4MSAxMyAzNzEgbDAgMzY1IDQ1IDAgNDUgMCAwIC00MjkgYzAgLTIzNyAtMyAtNDMyIC04IC00MzUgLTQgLTIgLTU5IDExIC0xMjEgMzAgLTYzIDE5IC0xNDYgMzcgLTE4NSA0MCAtODcgOCAtMjE0IC0xNCAtMjkzIC01MSAtNzEgLTMyIC0xMDUgLTMyIC0xOTYgNSAtMTUzIDYxIC0yODEgNjMgLTQ3MCA1IC02MCAtMTkgLTExNCAtMzIgLTExOSAtMjkgLTQgMyAtOCAxOTggLTggNDM1IGwwIDQyOSA0NSAwIDQ1IDAgMCAtMzU3eiIvPjxwYXRoIGQ9Ik04NTcgMTYwMyBjLTI0IC0yMyAtMSAtMzEgMTA2IC0zNiA2MSAtNCAxMjMgLTggMTM3IC05IDQ1IC01IDI5IDI2IC0yMCAzOSAtNDkgMTIgLTIxMiAxNyAtMjIzIDZ6Ii8+PHBhdGggZD0iTTg1NyAxNDYzIGMtMjQgLTIzIC0yIC0zMSAxMDEgLTM3IDU5IC0zIDEyMSAtNyAxMzcgLTggMjEgLTIgMzAgMSAzMCAxMiAwIDEwIC0xOCAxOSAtNTAgMjYgLTU1IDEzIC0yMDggMTggLTIxOCA3eiIvPjxwYXRoIGQ9Ik04NjMgMTMyNCBjLTcgLTMgLTEzIC0xMSAtMTMgLTE5IDAgLTkgMzAgLTE0IDEwOCAtMTkgNTkgLTMgMTE4IC03IDEzMiAtOSAzNiAtMyAzOSAxNiA2IDMxIC0yOCAxNCAtMjExIDI2IC0yMzMgMTZ6Ii8+PHBhdGggZD0iTTg2OCAxMTgzIGMtMTAgLTIgLTE4IC0xMSAtMTggLTE5IDAgLTExIDE3IC0xNCA4MSAtMTQgNDQgMCAxMDAgLTUgMTI0IC0xMSA1MiAtMTMgODMgLTYgNjYgMTUgLTIyIDI2IC0xOTEgNDYgLTI1MyAyOXoiLz48cGF0aCBkPSJNMTQ4OCAxNTk4IGMtMzggLTggLTQ4IC0xNCAtNDggLTMwIDAgLTE3IDQgLTE5IDI4IC0xMyAxNSAzIDc2IDkgMTM1IDEyIDkzIDUgMTA4IDggMTA1IDIyIC0zIDEzIC0xOCAxNiAtODggMTcgLTQ3IDEgLTEwNiAtMyAtMTMyIC04eiIvPjxwYXRoIGQ9Ik0xNDkwIDE0NTcgYy0zMCAtOCAtNDYgLTE4IC00OCAtMzEgLTMgLTE2IDAgLTE4IDI1IC0xMiAxNSA0IDc3IDEwIDEzNiAxMyA5MyA1IDEwOCA4IDEwNSAyMiAtMyAxMyAtMTggMTYgLTg4IDE4IC00NyAxIC0xMDUgLTQgLTEzMCAtMTB6Ii8+PHBhdGggZD0iTTE0OTUgMTMxNiBjLTM1IC04IC01MSAtMTcgLTUzIC0zMCAtMyAtMTYgMCAtMTggMjUgLTEyIDE1IDQgNzYgMTAgMTM2IDEzIDc2IDQgMTA3IDkgMTA3IDE4IDAgNyAtNyAxNiAtMTYgMTkgLTI1IDEwIC0xNDQgNSAtMTk5IC04eiIvPjxwYXRoIGQ9Ik0xNTAwIDExNzcgYy00MCAtOSAtNTYgLTE3IC01OCAtMzEgLTMgLTE2IDAgLTE4IDMwIC0xMiAxOCAzIDc2IDkgMTI4IDEyIDExOSA3IDEzMiAxMCAxMDYgMzAgLTI0IDE3IC0xMjYgMTcgLTIwNiAxeiIvPjwvZz48L3N2Zz4=
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        unsafeWindow
// @grant        GM_setClipboard
// @grant        GM_registerMenuCommand
// @grant        GM_unregisterMenuCommand
// @license      GNU General Public License v3.0
// @run-at       document-end
// @updateURL    https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js
// @downloadURL  https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js
// @require      https://cdnjs.cloudflare.com/ajax/libs/jszip/3.9.1/jszip.min.js
// ==/UserScript==

(function () {
    let config = {
        disclaimer: GM_getValue("disclaimer", false),
        packageDownloadFiles: GM_getValue("packageDownloadFiles", true),
        autoScrollSwitch: GM_getValue("autoScrollSwitch", false), // scrollCheckTime: GM_getValue("scrollCheckTime", 2500),
        maxScrollCount: GM_getValue("maxScrollCount", 10),
    };

    let menu = {
        disclaimer: undefined, packageDownloadFiles: undefined, autoScrollSwitch: undefined, // scrollCheckTime: undefined,
        maxScrollCount: undefined,
    };

    const readme = () => {
        const instructions = `
XHS-Downloader 用户脚本 功能清单：
1. 下载小红书无水印作品文件
2. 提取推荐页面作品链接
3. 提取账号发布作品链接
4. 提取账号收藏作品链接
5. 提取账号专辑作品链接
6. 提取账号点赞作品链接
7. 提取搜索结果作品链接
8. 提取搜索结果用户链接

XHS-Downloader 用户脚本 详细说明：
1. 下载小红书无水印作品文件时，脚本需要花费时间处理文件，请等待片刻，请勿多次点击下载按钮
2. 无水印作品文件较大，可能需要较长的时间处理，页面跳转可能会导致下载失败
3. 提取账号发布、收藏、点赞、专辑作品链接时，脚本可以自动滚动页面直至加载全部作品
4. 提取推荐作品链接、搜索作品、用户链接时，脚本可以自动滚动指定次数加载更多内容，默认滚动次数：10 次
5. 自动滚动页面功能默认关闭；用户可以自由开启，并修改滚动页面次数，修改后立即生效
6. 如果未开启自动滚动页面功能，用户需要手动滚动页面以便加载更多内容后再进行其他操作
7. 支持作品文件打包下载；该功能默认开启，多个文件的作品将会以压缩包格式下载

项目开源地址：https://github.com/JoeanAmier/XHS-Downloader
`
        const disclaimer_content = `
关于 XHS-Downloader 的 免责声明：

1. 使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项目所产生的任何损失、责任、或风险概不负责。
2. 本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者尽力确保代码的正确性和安全性，但不保证代码完全没有错误或缺陷。
3. 使用者在使用本项目时必须严格遵守 GNU General Public License v3.0 的要求，并在适当的地方注明使用了 GNU General Public License v3.0 的代码。
4. 使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。
5. 使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。
6. 本项目的作者不会提供 XHS-Downloader 项目的付费版本，也不会提供与 XHS-Downloader 项目相关的任何商业服务。
7. 基于本项目进行的任何二次开发、修改或编译的程序与原创作者无关，原创作者不承担与二次开发行为或其结果相关的任何责任，使用者应自行对因二次开发可能带来的各种情况负全部责任。

在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声明有任何疑问或不同意，请不要使用本项目的代码和功能。如果您使用了本项目的代码和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险和后果。

是否已阅读 XHS-Downloader 功能说明与免责声明(YES/NO)
`
        alert(instructions);
        alert(`自动滚动页面功能代码已重构，该功能默认关闭！
启用该功能可能会被小红书检测为自动化操作，从而导致账号受到风控或封禁！
该功能在使用过程中遇到任何问题请及时向开发者反馈！
`);
        if (!config.disclaimer) {
            const answer = prompt(disclaimer_content, "");
            if (answer === null) {
                GM_setValue("disclaimer", false);
                config.disclaimer = false;
            } else {
                GM_setValue("disclaimer", answer.toUpperCase() === "YES" || answer.toUpperCase() === "Y");
                config.disclaimer = GM_getValue("disclaimer");
                location.reload();
            }
        }
    };

    if (!config.disclaimer) {
        readme();
    }

    menu.disclaimer = GM_registerMenuCommand("关于 XHS-Downloader", function () {
        readme();
    });

    const packageDownloadFilesMenu = () => {
        menu.packageDownloadFiles = GM_registerMenuCommand(`文件打包下载功能 ${config.packageDownloadFiles ? '✔️' : '❌'}`, function () {
            config.packageDownloadFiles = !config.packageDownloadFiles;
            GM_setValue("packageDownloadFiles", config.packageDownloadFiles);
            GM_unregisterMenuCommand(menu.packageDownloadFiles);
            packageDownloadFilesMenu();
        }, {title: "单击切换功能状态",});
    };

    packageDownloadFilesMenu();

    const autoScrollSwitchMenu = () => {
        menu.autoScrollSwitch = GM_registerMenuCommand(`自动滚动页面功能 ${config.autoScrollSwitch ? '✔️' : '❌'}`, function () {
            config.autoScrollSwitch = !config.autoScrollSwitch;
            GM_setValue("autoScrollSwitch", config.autoScrollSwitch);
            GM_unregisterMenuCommand(menu.autoScrollSwitch);
            autoScrollSwitchMenu();
        }, {title: "单击切换功能状态",});
    };

    autoScrollSwitchMenu();

    // menu.scrollCheckTime = GM_registerMenuCommand("修改滚动检测间隔", function () {
    //     let data;
    //     data = prompt("请输入自动滚动页面检测间隔：\n如果网络环境不佳导致脚本未能加载全部作品，可以设置较大的检测间隔！", config.scrollCheckTime / 1000);
    //     if (data === null) {
    //         return
    //     }
    //     data = parseFloat(data) || 2.5
    //     config.scrollCheckTime = data * 1000;
    //     GM_setValue("scrollCheckTime", config.scrollCheckTime);
    //     alert(`修改自动滚动页面检测间隔成功，当前值：${data} 秒`);
    // });

    menu.maxScrollCount = GM_registerMenuCommand("修改滚动页面次数", function () {
        let data;
        data = prompt("请输入自动滚动页面次数：\n仅对提取推荐作品、搜索作品、搜索用户链接功能生效！", config.maxScrollCount);
        if (data === null) {
            return
        }
        config.maxScrollCount = parseInt(data) || 10;
        GM_setValue("maxScrollCount", config.maxScrollCount);
        alert(`修改自动滚动页面次数成功，当前值：${config.maxScrollCount} 次`);
    });

    const icon = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMjAwMTA5MDQvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvVFIvMjAwMS9SRUMtU1ZHLTIwMDEwOTA0L0RURC9zdmcxMC5kdGQiPjxzdmcgdmVyc2lvbj0iMS4wIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNTYuMDAwMDAwcHQiIGhlaWdodD0iMjU2LjAwMDAwMHB0IiB2aWV3Qm94PSIwIDAgMjU2LjAwMDAwMCAyNTYuMDAwMDAwIiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCBtZWV0Ij48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLjAwMDAwMCwyNTYuMDAwMDAwKSBzY2FsZSgwLjEwMDAwMCwtMC4xMDAwMDApIiBmaWxsPSIjZTgzYjM1IiBzdHJva2U9Im5vbmUiPjxwYXRoIGQ9Ik0xMTI1IDI1NDMgYy02MyAtNyAtMjIxIC00NiAtMjgyIC02OSAtMTc3IC02NyAtMzIxIC0xNjAgLTQ1OSAtMjk4IC0xOTQgLTE5NCAtMzEzIC00MjIgLTM1OSAtNjgzIC0xOSAtMTExIC0xOSAtMzI2IDAgLTQzOSA3NCAtNDIzIDM3OCAtNzk4IDc3NiAtOTU4IDQ4OSAtMTk3IDEwMzUgLTgwIDEzOTkgMzAwIDEzOCAxNDUgMjM2IDMwNyAyOTQgNDg3IDg1IDI2MCA4MSA1NjYgLTEwIDgxOSAtMTU2IDQzNCAtNTM4IDc1NCAtOTkzIDgzMiAtODYgMTQgLTI4MiAyMCAtMzY2IDl6IG01MCAtODEwIGw4MCAtMzAgMyAtMzg5IDIgLTM5MCAtODcgMjkgYy0xMzIgNDQgLTMwMiA0OCAtNDQwIDExIGwtMjMgLTYgMCAzOTEgYzAgMjE1IDMgMzkxIDggMzkxIDQgMSAzMCA3IDU3IDE1IDM2IDExIDg5IDE0IDE4NSAxMSAxMjEgLTIgMTQzIC02IDIxNSAtMzN6IG02MzggMTggbDM3IC0xMiAwIC0zODkgYzAgLTIxNSAtMiAtMzkwIC00IC0zOTAgLTMgMCAtMzUgNyAtNzMgMTYgLTEwOCAyNSAtMjc0IDE1IC0zODUgLTIzIGwtODggLTMxIDAgMzg4IDAgMzg3IDM5IDE4IGMxMDAgNDQgMTYwIDU1IDMwMSA1MSA3NCAtMiAxNTIgLTkgMTczIC0xNXogbS0xMTQzIC00NTggYzAgLTE5NyA0IC0zNjQgOCAtMzcxIDcgLTkgMjUgLTggODcgOCAxNDUgMzcgMzE1IDI0IDQ1NiAtMzUgbDYxIC0yNiA3MSAzMCBjNDAgMTYgMTAwIDM1IDEzNSA0MSA4MSAxNiAyNzEgOCAzMzIgLTE0IDI0IC05IDUwIC0xNCA1NyAtMTIgMTAgNCAxMyA4MSAxMyAzNzEgbDAgMzY1IDQ1IDAgNDUgMCAwIC00MjkgYzAgLTIzNyAtMyAtNDMyIC04IC00MzUgLTQgLTIgLTU5IDExIC0xMjEgMzAgLTYzIDE5IC0xNDYgMzcgLTE4NSA0MCAtODcgOCAtMjE0IC0xNCAtMjkzIC01MSAtNzEgLTMyIC0xMDUgLTMyIC0xOTYgNSAtMTUzIDYxIC0yODEgNjMgLTQ3MCA1IC02MCAtMTkgLTExNCAtMzIgLTExOSAtMjkgLTQgMyAtOCAxOTggLTggNDM1IGwwIDQyOSA0NSAwIDQ1IDAgMCAtMzU3eiIvPjxwYXRoIGQ9Ik04NTcgMTYwMyBjLTI0IC0yMyAtMSAtMzEgMTA2IC0zNiA2MSAtNCAxMjMgLTggMTM3IC05IDQ1IC01IDI5IDI2IC0yMCAzOSAtNDkgMTIgLTIxMiAxNyAtMjIzIDZ6Ii8+PHBhdGggZD0iTTg1NyAxNDYzIGMtMjQgLTIzIC0yIC0zMSAxMDEgLTM3IDU5IC0zIDEyMSAtNyAxMzcgLTggMjEgLTIgMzAgMSAzMCAxMiAwIDEwIC0xOCAxOSAtNTAgMjYgLTU1IDEzIC0yMDggMTggLTIxOCA3eiIvPjxwYXRoIGQ9Ik04NjMgMTMyNCBjLTcgLTMgLTEzIC0xMSAtMTMgLTE5IDAgLTkgMzAgLTE0IDEwOCAtMTkgNTkgLTMgMTE4IC03IDEzMiAtOSAzNiAtMyAzOSAxNiA2IDMxIC0yOCAxNCAtMjExIDI2IC0yMzMgMTZ6Ii8+PHBhdGggZD0iTTg2OCAxMTgzIGMtMTAgLTIgLTE4IC0xMSAtMTggLTE5IDAgLTExIDE3IC0xNCA4MSAtMTQgNDQgMCAxMDAgLTUgMTI0IC0xMSA1MiAtMTMgODMgLTYgNjYgMTUgLTIyIDI2IC0xOTEgNDYgLTI1MyAyOXoiLz48cGF0aCBkPSJNMTQ4OCAxNTk4IGMtMzggLTggLTQ4IC0xNCAtNDggLTMwIDAgLTE3IDQgLTE5IDI4IC0xMyAxNSAzIDc2IDkgMTM1IDEyIDkzIDUgMTA4IDggMTA1IDIyIC0zIDEzIC0xOCAxNiAtODggMTcgLTQ3IDEgLTEwNiAtMyAtMTMyIC04eiIvPjxwYXRoIGQ9Ik0xNDkwIDE0NTcgYy0zMCAtOCAtNDYgLTE4IC00OCAtMzEgLTMgLTE2IDAgLTE4IDI1IC0xMiAxNSA0IDc3IDEwIDEzNiAxMyA5MyA1IDEwOCA4IDEwNSAyMiAtMyAxMyAtMTggMTYgLTg4IDE4IC00NyAxIC0xMDUgLTQgLTEzMCAtMTB6Ii8+PHBhdGggZD0iTTE0OTUgMTMxNiBjLTM1IC04IC01MSAtMTcgLTUzIC0zMCAtMyAtMTYgMCAtMTggMjUgLTEyIDE1IDQgNzYgMTAgMTM2IDEzIDc2IDQgMTA3IDkgMTA3IDE4IDAgNyAtNyAxNiAtMTYgMTkgLTI1IDEwIC0xNDQgNSAtMTk5IC04eiIvPjxwYXRoIGQ9Ik0xNTAwIDExNzcgYy00MCAtOSAtNTYgLTE3IC01OCAtMzEgLTMgLTE2IDAgLTE4IDMwIC0xMiAxOCAzIDc2IDkgMTI4IDEyIDExOSA3IDEzMiAxMCAxMDYgMzAgLTI0IDE3IC0xMjYgMTcgLTIwNiAxeiIvPjwvZz48L3N2Zz4=";

    const about = () => {
        window.open('https://github.com/JoeanAmier/XHS-Downloader', '_blank');
    }

    const abnormal = () => {
        alert("下载无水印作品文件失败！请向作者反馈！\n项目地址：https://github.com/JoeanAmier/XHS-Downloader");
    };

    const generateVideoUrl = note => {
        try {
            return [`https://sns-video-bd.xhscdn.com/${note.video.consumer.originVideoKey}`];
        } catch (error) {
            console.error("Error generating video URL:", error);
            return [];
        }
    };

    const generateImageUrl = note => {
        let images = note.imageList;
        const regex = /http:\/\/sns-webpic-qc\.xhscdn.com\/\d+\/[0-9a-z]+\/(\S+)!/;
        let urls = [];
        try {
            images.forEach((item) => {
                let match = item.urlDefault.match(regex);
                if (match && match[1]) {
                    urls.push(`https://ci.xiaohongshu.com/${match[1]}?imageView2/format/png`);
                }
            })
            return urls
        } catch (error) {
            console.error("Error generating image URLs:", error);
            return [];
        }
    };

    const download = async (urls, type_) => {
        const name = extractName();
        console.info(`文件名称 ${name}`);
        if (type_ === "video") {
            await downloadVideo(urls[0], name);
        } else {
            await downloadImage(urls, name);
        }
    };

    const exploreDeal = async note => {
        try {
            let links;
            if (note.type === "normal") {
                links = generateImageUrl(note);
            } else {
                links = generateVideoUrl(note);
            }
            if (links.length > 0) {
                console.info("下载链接", links);
                await download(links, note.type);
            } else {
                abnormal()
            }
        } catch (error) {
            console.error("Error in exploreDeal function:", error);
            abnormal();
        }
    };

    const extractNoteInfo = () => {
        const regex = /\/explore\/([^?]+)/;
        const match = currentUrl.match(regex);
        if (match) {
            return unsafeWindow.__INITIAL_STATE__.note.noteDetailMap[match[1]]
        } else {
            console.error("从链接提取作品 ID 失败", currentUrl,);
        }
    };

    const extractDownloadLinks = async () => {
        if (currentUrl.includes("https://www.xiaohongshu.com/explore/")) {
            let note = extractNoteInfo();
            if (note.note) {
                await exploreDeal(note.note);
            } else {
                abnormal();
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

        console.info(`文件已成功下载: ${name}`);
    }

    const downloadFile = async (link, name, trigger = true, retries = 5) => {
        for (let attempt = 1; attempt <= retries; attempt++) {
            try {
                // 使用 fetch 获取文件数据
                const response = await fetch(link, {method: "GET"});

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

    const downloadFiles = async (urls, name,) => {
        const downloadResults = []; // 用于存储下载结果

        const downloadPromises = urls.map(async (url, index) => {
            const fileName = `${name}_${index + 1}.png`; // 根据索引生成文件名
            const result = await downloadFile(url, fileName, false); // 调用单个文件下载方法
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

    const truncateString = (str, maxLength) => {
        if (str.length > maxLength) {
            const halfLength = Math.floor(maxLength / 2) - 1; // 减去 1 留出省略号的空间
            return str.slice(0, halfLength) + '...' + str.slice(-halfLength);
        }
        return str;
    };

    const extractName = () => {
        let name = document.title.replace(/ - 小红书$/, "").replace(/[^\u4e00-\u9fa5a-zA-Z0-9 ~!@#$%&()_\-+=\[\];"',.！（）【】：“”，。《》？]/g, "");
        name = truncateString(name, 64,);
        let match = currentUrl.match(/\/([^\/]+)$/);
        let id = match ? match[1] : null;
        return name === "" ? id : name
    };

    const downloadVideo = async (url, name) => {
        if (!await downloadFile(url, `${name}.mp4`)) {
            abnormal();
        }
    };

    const downloadImage = async (urls, name) => {
        let success;
        if (!config.packageDownloadFiles) {
            let result = [];
            for (const [index, url] of urls.entries()) {
                result.push(await downloadFile(url, `${name}_${index + 1}.png`));
            }
            success = result.every(item => item === true);
        } else if (urls.length > 1) {
            success = await downloadFiles(urls, name,);
        } else {
            success = await downloadFile(urls[0], `${name}.png`);
        }
        if (!success) {
            abnormal();
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
        return notesRawValue.map(item => [item.id, item.xsecToken,]);
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
            return notesRawValue.map(item => [item.noteId, item.xsecToken,]);
        } else {
            console.error("从链接提取专辑 ID 失败", currentUrl,);
            return [];
        }
    };

    const extractFeedInfo = () => {
        const notesRawValue = unsafeWindow.__INITIAL_STATE__.feed.feeds._rawValue;
        return notesRawValue.map(item => [item.id, item.xsecToken,]);
    };

    const extractSearchNotes = () => {
        const notesRawValue = unsafeWindow.__INITIAL_STATE__.search.feeds._rawValue;
        return notesRawValue.map(item => [item.id, item.xsecToken,]);
    }

    const extractSearchUsers = () => {
        const notesRawValue = unsafeWindow.__INITIAL_STATE__.search.userLists._rawValue;
        return notesRawValue.map(item => item.id);
    }

    const generateNoteUrls = data => data.map(([id, token,]) => `https://www.xiaohongshu.com/discovery/item/${id}?source=webshare&xhsshare=pc_web&xsec_token=${token}&xsec_source=pc_share`).join(" ");

    const generateUserUrls = data => data.map(id => `https://www.xiaohongshu.com/user/profile/${id}`).join(" ");

    const extractAllLinks = (callback, order) => {
        scrollScreenEvent(() => {
            let data;
            if (order >= 0 && order <= 2) {
                data = extractNotesInfo(order);
            } else if (order === 3) {
                data = extractSearchNotes();
            } else if (order === 4) {
                data = extractSearchUsers();
            } else if (order === -1) {
                data = extractFeedInfo()
            } else if (order === 5) {
                data = extractBoardInfo()
            } else {
                data = [];
            }
            let urlsString = order !== 4 ? generateNoteUrls(data) : generateUserUrls(data);
            callback(urlsString);
        }, [0, 1, 2, 5].includes(order))
    };

    const extractAllLinksEvent = (order = 0) => {
        extractAllLinks(urlsString => {
            if (urlsString) {
                GM_setClipboard(urlsString, "text", () => {
                    alert('作品/用户链接已复制到剪贴板！');
                });
            } else {
                alert("未提取到任何作品/用户链接！")
            }
        }, order);
    };

    const createContainer = () => {
        let container = document.createElement('div');
        container.id = 'xhsFunctionContainer';

        let imgTextContainer = document.createElement('div');
        imgTextContainer.id = 'xhsImgTextContainer';

        let img = new Image(48, 48); // 确保 icon 变量已定义
        img.src = icon;
        img.style.borderRadius = '50%';
        img.style.objectFit = 'cover';

        let textDiv = document.createElement('div');
        textDiv.id = 'xhsImgTextContainer__text'
        textDiv.textContent = 'XHS-Downloader';

        imgTextContainer.appendChild(img);
        imgTextContainer.appendChild(textDiv);

        container.appendChild(imgTextContainer);

        document.body.appendChild(container);
        return container;
    };

    const createButton = (id, text, onClick, ...args) => {
        let button = document.createElement('button');
        button.id = id;
        button.textContent = text;
        button.addEventListener('click', () => onClick(...args));
        return button;
    };

    const exclusionButton = ["xhsImgTextContainer", "About"];

    const updateContainer = buttons => {
        let container = document.getElementById('xhsFunctionContainer');
        if (!container) {
            container = createContainer();
        }

        // 移除除了 imgTextContainer 以外的所有子元素
        Array.from(container.children).forEach(child => {
            if (!exclusionButton.includes(child.id)) {
                child.remove();
            }
        });

        // 添加有效按钮
        buttons.forEach(button => {
            container.appendChild(button);
        });
    };

    const buttons = [
        createButton("Download", "下载无水印作品文件", extractDownloadLinks),
        createButton("Post", "提取发布作品链接", extractAllLinksEvent, 0),
        createButton("Collection", "提取收藏作品链接", extractAllLinksEvent, 1),
        createButton("Favorite", "提取点赞作品链接", extractAllLinksEvent, 2),
        createButton("Feed", "提取推荐作品链接", extractAllLinksEvent, -1),
        createButton("Search", "提取搜索作品链接", extractAllLinksEvent, 3),
        createButton("User", "提取搜索用户链接", extractAllLinksEvent, 4),
        createButton("Board", "提取专辑作品链接", extractAllLinksEvent, 5),
        createButton("Disclaimer", "脚本说明及免责声明", readme,),
        createButton("About", "关于 XHS-Downloader", about,),];

    const run = url => {
        setTimeout(function () {
            if (!config.disclaimer) {
            } else if (url === "https://www.xiaohongshu.com/explore" || url.includes("https://www.xiaohongshu.com/explore?")) {
                updateContainer(buttons.slice(4, 5));
            } else if (url.includes("https://www.xiaohongshu.com/explore/")) {
                updateContainer(buttons.slice(0, 1));
            } else if (url.includes("https://www.xiaohongshu.com/user/profile/")) {
                updateContainer(buttons.slice(1, 4));
            } else if (url.includes("https://www.xiaohongshu.com/search_result")) {
                updateContainer(buttons.slice(5, 7));
            } else if (url.includes("https://www.xiaohongshu.com/board/")) {
                updateContainer(buttons.slice(7, 8));
            }
        }, 500)
    }

    let currentUrl = window.location.href;

    updateContainer(buttons.slice(8));

    // 初始化容器
    run(currentUrl)

    // 设置 MutationObserver 来监听 URL 变化
    let observer
    if (config.disclaimer) {
        observer = new MutationObserver(function () {
            if (currentUrl !== window.location.href) {
                currentUrl = window.location.href;
                run(currentUrl);
            }
        });
        const config = {childList: true, subtree: true};
        observer.observe(document.body, config);
    }

    const buttonStyle = `
    #xhsFunctionContainer {
        position: fixed;
        bottom: 15%;
        background-color: #fff;
        color: #2f3542;
        padding: 5px 10px;
        border-radius: 0 32px 32px 0;
        box-shadow: 0 3.2px 12px #00000014, 0 5px 24px #0000000a;
        transition: width 0.25s ease-in-out, border-radius 0.25s ease-in-out, height 0.25s ease-in-out;
        overflow: hidden;
        white-space: nowrap;
        width: 65px; /* 初始宽度 */
        height: 60px;
        text-align: center;
        font-size: 16px;
        display: flex;
        flex-direction: column-reverse;
        z-index: 99999;
    }
    
    #xhsFunctionContainer:hover {
        padding: 10px 10px 5px 10px;
        width: 210px; /* hover时的宽度 */
        height: auto;
    }

    #xhsFunctionContainer button {
        cursor: pointer;
        height: 48px;
        color: #ff4757;
        font-size: 14px;
        font-weight: 600;
        border-radius: 32px;
        margin-bottom: 14px;
        border: 3px #ff4757 solid;
    }
    
    #xhsFunctionContainer button:active {
        background-color: #ff4757; /* 点击时的背景颜色 */
    }
    
    #xhsImgTextContainer {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    #xhsImgTextContainer__text {
        font-size: 14px;
        font-weight: 600;
    }
    `;

    const head = document.head || document.getElementsByTagName('head')[0];
    const style = document.createElement('style');
    head.appendChild(style);

    style.type = 'text/css';
    style.appendChild(document.createTextNode(buttonStyle));
    console.info("用户接受 XHS-Downloader 免责声明", config.disclaimer)

    if (typeof JSZip === 'undefined') {
        alert("XHS-Downloader 用户脚本依赖库 JSZip 加载失败，作品文件打包下载功能无法使用，请尝试刷新网页或者向作者反馈！");
    }
})();

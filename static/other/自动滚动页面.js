// ==UserScript==
// @name         自动滚动页面
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  模拟自然滚动，测试页面滚动效果
// @author       ChatGPT, JoeanAmier
// @match        *://*/*  // 匹配所有页面，也可以指定具体网站
// @grant        none
// @run-at       document-end  // 在页面加载完毕后运行脚本
// ==/UserScript==

(function () {
    'use strict';

    // 配置滚动模式
    const scrollMode = 'limited'; // 'none'、'endless' 或 'limited'
    const maxScrollCount = 10; // 最大滚动次数（如果模式是 'limited'）

    // 随机整数生成函数
    const getRandomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

    // 判断是否需要暂停，模拟用户的停顿行为
    const shouldPause = () => Math.random() < 0.2;  // 20%几率停顿

    // 执行一次增量滚动
    const scrollOnce = () => {
        const scrollDistanceMin = 50;  // 最小滚动距离
        const scrollDistanceMax = 200; // 最大滚动距离
        const scrollDistance = getRandomInt(scrollDistanceMin, scrollDistanceMax);
        console.log(`滚动距离: ${scrollDistance}px`);  // 日志输出滚动距离
        window.scrollBy(0, scrollDistance);  // 增量滚动
    };

    // 检查是否已经滚动到底部
    const isAtBottom = () => {
        const docHeight = document.documentElement.scrollHeight;
        const winHeight = window.innerHeight;
        const scrollPos = window.scrollY;

        return (docHeight - winHeight - scrollPos <= 10);  // 如果距离底部小于10px，认为滚动到底部
    };

    // 自动滚动主函数
    const scrollScreen = (callback, scrollCount = 0,) => {
        const timeoutMin = 100;  // 最小滚动间隔
        const timeoutMax = 300;  // 最大滚动间隔

        console.log('开始滚动...');

        const scrollInterval = setInterval(() => {
            if (shouldPause()) {
                // 停顿，模拟用户的休息
                clearInterval(scrollInterval);
                setTimeout(() => {
                    scrollScreen(callback, scrollCount,);  // 重新启动滚动
                }, getRandomInt(500, 1500));  // 随机停顿时间
            } else if (scrollMode === 'endless') {
                // 无限滚动至底部模式
                if (!isAtBottom()) {
                    scrollOnce();  // 执行一次滚动
                } else {
                    // 到达底部，停止滚动
                    clearInterval(scrollInterval);
                    callback();  // 调用回调函数
                    console.log('已经到达页面底部，停止滚动');
                }
            } else if (scrollMode === 'limited') {
                // 滚动指定次数模式
                if (scrollCount < maxScrollCount && !isAtBottom()) {
                    scrollOnce();  // 执行一次滚动
                    scrollCount++;
                } else {
                    // 如果到达底部或滚动次数已满，停止滚动
                    clearInterval(scrollInterval);
                    callback();  // 调用回调函数
                    console.log(`已经滚动${scrollCount}次，停止滚动`);
                }
            } else if (scrollMode === 'none') {
                // 关闭滚动功能
                clearInterval(scrollInterval);
                console.log('自动滚动已关闭');
            }
        }, getRandomInt(timeoutMin, timeoutMax));  // 随机滚动间隔
    };

    // 等待页面完全加载后执行滚动
    window.addEventListener('load', () => {
        console.log('页面加载完成');

        // 检查页面是否足够长，以便滚动
        if (document.body.scrollHeight > window.innerHeight && scrollMode !== 'none') {
            // 执行自动滚动
            scrollScreen(() => {
                console.log('滚动完成');
            });
        } else {
            console.log('页面没有足够的内容进行滚动，或者自动滚动已关闭');
        }
    });

})();

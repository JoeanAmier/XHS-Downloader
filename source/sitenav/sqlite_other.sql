
-- Root Level Nodes
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2000, 0, '常用', '', NULL, 1, 1, 'other', 2000);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2001, 0, '学习', '', NULL, 0, 1, 'other', 2001);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2002, 0, '影视', '', NULL, 0, 1, 'other', 2002);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2003, 0, '杂类', '', NULL, 0, 1, 'other', 2003);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2004, 0, '系统', '', NULL, 0, 1, 'other', 2004);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2005, 0, '生活', '', NULL, 0, 1, 'other', 2005);

-- Children under id:2000 ('常用')
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2006, 2000, '电影推荐 · MVCAT', '', 'https://www.mvcat.com/', 0, 1, 'other', 2006);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2007, 2000, '', '', 'javascript:void(0);', 0, 1, 'other', 2007);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2008, 2000, '编程工具', '', 'https://masuit.com/cat/7', 0, 1, 'other', 2008);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2009, 2000, 'Software - 厘米天空', '', 'http://www.cmsky.com/', 0, 1, 'other', 2009);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2010, 2000, '吾爱破解', 'dfg727/aB...6', 'https://www.52pojie.cn/', 0, 1, 'other', 2010);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2011, 2000, '图怪兽作图神器', '是一个在线ps图片 海报 编辑器,', 'https://818ps.com/', 0, 1, 'other', 2011);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2012, 2000, '', '', 'javascript:void(0);', 0, 1, 'other', 2012);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2013, 2000, '书享家', '', 'http://shuxiangjia.cn/', 0, 1, 'other', 2013);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2014, 2000, '', '', 'javascript:void(0);', 0, 1, 'other', 2014);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2015, 2000, 'fuliba', '搞笑图', 'https://fuliba2023.net', 0, 1, 'other', 2015);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2016, 2000, '', '', 'javascript:void(0);', 0, 1, 'other', 2016);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2017, 2000, '远景', 'ifelse01/Aa123456', 'http://bbs.pcbeta.com/', 0, 1, 'other', 2017);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2018, 2000, '威锋', '1581.../aB...', 'https://bbs.feng.com/', 0, 1, 'other', 2018);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2019, 2000, '', '', 'javascript:void(0);', 0, 0, 'other', 2019);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2020, 2000, 'ClashNode', '', 'https://clashfree.eu.org/', 0, 1, 'other', 2020);

-- Children under id:2001 ('学习')
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2021, 2001, 'Net Framework', '', 'https://www.microsoft.com/net/download/visual-studio-sdks/', 0, 1, 'other', 2021);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2022, 2001, '代码仓库， 免费建站', '', NULL, 1, 1, 'other', 2022);

-- Sub-items under id:2022
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2032, 2022, '免费建站 - 基于github...', '', 'https://app.netlify.com/account/sites', 0, 1, 'other', 2032);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2033, 2022, 'CodeSandbox - 托管编码平台', '', 'https://codesandbox.io/', 0, 1, 'other', 2033);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2034, 2022, 'glitch - 托管编码平台', '', 'https://glitch.com/', 0, 1, 'other', 2034);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2035, 2022, 'replit - 托管编码平台', '', 'https://replit.com/', 0, 1, 'other', 2035);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2036, 2022, 'RiouxSVN', '', 'https://riouxsvn.com', 0, 1, 'other', 2036);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2037, 2022, 'SourceForge.net', '', 'https://sourceforge.net/account/login.php', 0, 1, 'other', 2037);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2038, 2022, 'codeplex.com', '', 'https://workspaces.codeplex.com/SourceControl/latest', 0, 1, 'other', 2038);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2039, 2022, 'ifelse01  GitHub', '', 'https://github.com/ifelse01', 0, 1, 'other', 2039);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2040, 2022, '代码托管 - 开源中国社区', '', 'https://git.oschina.net/ifelse01', 0, 1, 'other', 2040);

-- Additional children under id:2001 ('学习')
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2023, 2001, 'sendgrid', 'ifelse01/abc..@123..', 'https://app.sendgrid.com/login', 0, 1, 'other', 2023);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2024, 2001, 'CSDN论坛', 'abc..@123..', 'http://forum.csdn.net/BList/DotNET/EssentialList', 0, 1, 'other', 2024);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2025, 2001, 'dfg727 博客园', '', 'http://www.cnblogs.com/dfg727/', 0, 1, 'other', 2025);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2026, 2001, 'Database', '', NULL, 1, 1, 'other', 2026);

-- Sub-items under id:2026
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2041, 2026, 'JackDB - 在线各种数据库', 'QQ Login', 'https://app.jackdb.com/', 0, 1, 'other', 2041);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2042, 2026, 'db4free.net  MySQL', '', 'http://db4free.net/d4f_apply.php', 0, 1, 'other', 2042);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2043, 2026, '云数据库 - Bmob', '', 'http://www.bmob.cn/', 0, 1, 'other', 2043);

-- Mock API section
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2027, 2001, 'Mock Api', '', NULL, 1, 1, 'other', 2027);

-- Sub-items under id:2027
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2044, 2027, 'DOClever', 'dfg727', 'http://doclever.cn/controller/index/index.html', 0, 1, 'other', 2044);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2045, 2027, 'rap2-taobao', '2167162@qq.com', 'rap2.taobao.org', 0, 1, 'other', 2045);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2046, 2027, 'easy-mock', '', 'https://www.easy-mock.com', 0, 1, 'other', 2046);

-- Other learning resources
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2028, 2001, 'ProcessOn - 在线作图', 'QQ Login', 'https://www.processon.com/', 0, 1, 'other', 2028);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2029, 2001, 'BootCDN - 在CDN 加速服务', '前端开源项目 CDN 加速服务 ', 'https://www.bootcdn.cn/', 0, 1, 'other', 2029);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2030, 2001, '音图资源', '', NULL, 1, 1, 'other', 2030);

-- Sub-items under id:2030
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2047, 2030, '好图网 - 提供最优秀的图标下载', '', 'http://www.haotu.net/icon/179594/todo', 0, 1, 'other', 2047);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2048, 2030, '素材_懒人图库', '', 'http://www.lanrentuku.com/psd/anniu/5992.html', 0, 1, 'other', 2048);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2049, 2030, '站长素材 - 音效', '', 'http://sc.chinaz.com/yinxiao/', 0, 1, 'other', 2049);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2050, 2030, '网页模版', '', 'http://www.templatesy.com/', 0, 1, 'other', 2050);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2051, 2030, 'Iconfont-阿里巴巴矢量图标库', '', 'http://www.iconfont.cn/', 0, 1, 'other', 2051);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2052, 2030, 'undraw-矢量图标库', '图标可自选色', 'https://undraw.co/illustrations', 0, 1, 'other', 2052);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2053, 2030, 'Fontello-图标库', '', 'http://fontello.com', 0, 1, 'other', 2053);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2054, 2030, 'Flatlcon-免费的SVG、PNG、WebFont 格式图标素材', '', 'http://flaticons.net', 0, 1, 'other', 2054);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2055, 2030, 'EasyIcon-免费搜索图标的搜索引擎站点', '', 'http://www.easyicon.net', 0, 1, 'other', 2055);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2056, 2030, 'Swifticons-高品质图标素材库', '', 'http://www.swifticons.com', 0, 1, 'other', 2056);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2057, 2030, 'Icons8-提供免费iOS、Windows、Android的平面化设计图案的搜索引擎', '', 'https://icons8.com/', 0, 1, 'other', 2057);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2058, 2030, 'vexels-免费素材涵盖的范围也非常的广', '', 'https://www.vexels.com/', 0, 1, 'other', 2058);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2059, 2030, 'Vector Me-免费矢量素材网站', '', 'http://vector.me/', 0, 1, 'other', 2059);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2060, 2030, 'Freeepik', '', 'http://t.cn/zjw6jrk', 0, 1, 'other', 2060);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2061, 2030, 'Subtle Pattern 是目前特别受欢迎的纹理网站', '', 'http://t.cn/RJhxpBo', 0, 1, 'other', 2061);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2062, 2030, '1001 Free Downloads 是一个综合性的网站', '', 'http://www.1001freedownloads.com/', 0, 1, 'other', 2062);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2063, 2030, 'Vecteezy 是一个免费的矢量图索引站点', '', 'https://www.vecteezy.com/', 0, 1, 'other', 2063);

-- Docker resource
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2031, 2001, 'Docker 从入门到实践 Search', '', 'https://vuepress.mirror.docker-practice.com/image/dockerfile/', 0, 1, 'other', 2031);

-- Children under id:2002 ('影视')
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2074, 2002, '周榜--音悦Tai', '', 'http://vchart.yinyuetai.com/vchart/v', 0, 1, 'other', 2074);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2075, 2002, '推荐音乐 -- SongTaste 用音乐倾听彼此', '', 'http://www.songtaste.com/music/', 0, 1, 'other', 2075);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2076, 2002, '6V电影', '', 'https://www.66s.cc/', 0, 1, 'other', 2076);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2077, 2002, '电影票房排行榜', '', 'http://58921.com/alltime', 0, 1, 'other', 2077);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2078, 2002, '电影先生', '', 'http://DianYing.im', 0, 1, 'other', 2078);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2079, 2002, '饭团影院', '', 'https://fantuan.tv/vodtype/1.html', 0, 1, 'other', 2079);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2080, 2002, '飘花电影下载', '', 'https://www.piaohua.com/', 0, 1, 'other', 2080);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2081, 2002, '福利吧', '', 'http://lao4g.com', 0, 1, 'other', 2081);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2082, 2002, '无损音乐下载', '', 'https://www.sq688.com/', 0, 1, 'other', 2082);

-- Children under id:2003 ('杂类')
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2083, 2003, 'PC6 Mac软件', '', 'http://www.pc6.com/mac/', 0, 1, 'other', 2083);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2084, 2003, '史蒂芬周的博客 - Mac软件', '', 'http://www.sdifen.com/', 0, 1, 'other', 2084);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2085, 2003, '软件学堂', '', 'http://www.xue51.com/apple/index.html', 0, 1, 'other', 2085);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2086, 2003, '精品Mac应用分享推荐 - Awesome Mac', '', 'http://wangchujiang.com/awesome-mac/index.zh.html', 0, 1, 'other', 2086);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2087, 2003, '知您网(zhinin.com) - Mac软件下载', '', 'http://www.zhinin.com/', 0, 0, 'other', 2087);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2088, 2003, 'macwk - 无需积分', '', 'https://www.macwk.com/', 0, 0, 'other', 2088);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2089, 2003, 'MacEnjoy - Mac软件下载', '', 'https://www.macenjoy.co/', 0, 1, 'other', 2089);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2090, 2003, '我爱Mac - Mac软件下载', '', 'https://www.52mac.com/', 0, 1, 'other', 2090);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2091, 2003, '软件sOS - 软件下载', '', 'https://www.rjsos.com/', 0, 1, 'other', 2091);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2092, 2003, 'MAC萌新 - Mac软件下载', '', 'https://www.macxin.com/archives/3372.html', 0, 1, 'other', 2092);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2093, 2003, 'Digit77', '', 'https://www.digit77.com/', 0, 1, 'other', 2093);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2094, 2003, '马可波罗 - Mac软件下载', '', 'https://www.macbl.com/', 0, 1, 'other', 2094);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2095, 2003, 'xclient.info - Mac软件下载', '', 'https://xclient.info/', 0, 1, 'other', 2095);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2096, 2003, '潘多拉盒子 - Mac软件下载', '', 'https://www.inpandora.com/', 0, 1, 'other', 2096);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2097, 2003, 'MacYY - Mac软件下载', '', 'https://www.macyy.cn/', 0, 1, 'other', 2097);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2098, 2003, '俄罗斯的，可切换中文 - Mac软件下载', '', 'https://appstorrent.ru/', 0, 1, 'other', 2098);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2099, 2003, 'Cmarked - Mac软件下载', '', 'https://apps.cmacked.com/', 0, 1, 'other', 2099);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2100, 2003, 'Mac App - Mac软件下载', '', 'https://macapp.org.cn/', 0, 1, 'other', 2100);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2101, 2003, 'TorrentMac - Mac软件下载', '', 'https://www.torrentmac.net/', 0, 1, 'other', 2101);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2102, 2003, '优美图', '', 'http://www.topit.me/', 0, 1, 'other', 2102);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2103, 2003, '极简插件 - Chrome插件下载', '', 'https://chrome.zzzmh.cn/', 0, 1, 'other', 2103);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2104, 2003, 'Remove Video Background', '', 'https://www.unscreen.com/', 0, 1, 'other', 2104);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2105, 2003, 'Photoshop online', '', 'https://www.photopea.com/', 0, 1, 'other', 2105);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2106, 2003, '搜索导航', '', 'http://bt-mao.com/', 0, 1, 'other', 2106);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2107, 2003, '阿雷导航', '', 'https://aleikeji.com/mac', 0, 1, 'other', 2107);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2108, 2003, '', '', 'javascript:void(0);', 0, 1, 'other', 2108);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2109, 2003, 'zd423 - 软件分享平台', '', 'http://www.zdfans.com', 0, 1, 'other', 2109);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2110, 2003, '绿软分享吧', '', 'http://www.lrshare.com', 0, 1, 'other', 2110);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2111, 2003, '软件缘 - 精品绿软', '', 'https://www.appcgn.com', 0, 1, 'other', 2111);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2112, 2003, '风刑软件站', '', 'http://www.wsf1234.com', 0, 1, 'other', 2112);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2113, 2003, '『BhVip』android破解软件更新合集', '', 'http://pan.lanzou.com/u/%E5%BD%AA%E7%85%8Cqq1846055318', 0, 1, 'other', 2113);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2114, 2003, 'win&android破解软件', '', 'https://hrtsea.com/category/android', 0, 1, 'other', 2114);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2115, 2003, '搞机师兄', '', 'https://www.lanzous.com/b904045', 0, 1, 'other', 2115);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2116, 2003, '网站导航', '', 'https://imyshare.com/navigation/', 0, 1, 'other', 2116);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2117, 2003, '软件学堂 - visual studio下载', 'visual studio下载', 'http://www.xue51.com/soft/18137.html', 0, 1, 'other', 2117);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2118, 2003, '极光下载 - visual studio（带注册码）', 'visual studio下载', 'http://www.xz7.com/downinfo/398522.html', 0, 1, 'other', 2118);

-- Children under id:2004 ('系统')
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2119, 2004, 'U盘启动盘制作工具,U盘启动系统,大白菜.装机专家！', '', 'http://www.winbaicai.com/u.html', 0, 1, 'other', 2119);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2120, 2004, '系统之家', '', 'http://www.xitongzhijia.net/', 0, 1, 'other', 2120);

-- Children under id:2005 ('生活')
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2121, 2005, '登录-学信网', '', 'https://account.chsi.com.cn/passport/login', 0, 1, 'other', 2121);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2122, 2005, '深圳市公安局出入境便民网', '', 'http://www.szga.gov.cn/MSJW/', 0, 1, 'other', 2122);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2123, 2005, '美食杰 - 美食_菜谱大全_食谱_美食网', '', 'http://www.meishij.net/', 0, 1, 'other', 2123);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (2124, 2005, '麦库记事', '', 'https://note.sdo.com/my', 0, 1, 'other', 2124);
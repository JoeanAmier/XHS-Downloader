-- Common Sites (id:1000)
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1000, 0, 'Common Sites', '', NULL, 1, 1, 'index', 1000);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1010, 1000, 'Jenkins', '', 'http://121.196.104.20:8888/', 0, 1, 'index', 1010);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1020, 1000, '禅道', '', 'http://192.168.2.180:82/zentao/my.html', 0, 1, 'index', 1020);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1030, 1000, '墨刀', '', 'https://modao.cc/team/splbgnpgz7muqiei/folder/tel2zzhemdlh8vgayk', 0, 1, 'index', 1030);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1040, 1000, '邮箱', '', 'http://mail.lanyang.com/', 0, 1, 'index', 1040);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1050, 1000, 'Gitblit', '', 'http://192.168.2.180:8808/', 0, 1, 'index', 1050);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1060, 1000, '开发任务汇总', '', 'https://www.kdocs.cn/wo/sl/v344KoRZ?app_id=2wd4E4bxTOHihwkwkvaNGN', 0, 1, 'index', 1060);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1070, 1000, '物联网秤项目任务', '', 'https://kdocs.cn/l/cogElwjqE2yZ', 0, 1, 'index', 1070);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1080, 1000, '发布申请表', '', 'https://kdocs.cn/l/crwpEMnJI6Lt', 0, 1, 'index', 1080);

-- Local Sites (id:1100)
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1100, 0, 'Local Sites', '', NULL, 1, 1, 'index', 1100);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1110, 1100, 'IotLpg.Web', '', 'http://localhost:8012/IotLpg.Web/index.aspx', 0, 1, 'index', 1110);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1120, 1100, 'IotLpg.Sale.App.Api', '', 'http://localhost:8012/iot.sale.app.api/swagger/index.html', 0, 1, 'index', 1120);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1130, 1100, 'IotLpg.Sale.App.Api(Sejil Log)', '', 'http://localhost:8012/iot.sale.app.api/Sejil', 0, 1, 'index', 1130);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1140, 1100, 'trunklpg', '', 'http://localhost:8012/dev.trunklpg/home/default.aspx', 0, 1, 'index', 1140);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1150, 1100, 'trunklpg - 呼叫配送管理系统', '', 'http://localhost:8012/dev.trunklpg/SysManage/index.aspx', 0, 1, 'index', 1150);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1160, 1100, '09WebAPI.WebApi', '', 'http://localhost:8012/dev.webapi/swagger', 0, 1, 'index', 1160);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1170, 1100, 'SaaSAPPlpg', '', 'http://localhost:8012/dev.saasapplpg', 0, 1, 'index', 1170);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1180, 1100, 'OperationLogs', '', 'http://localhost:8012/dev.trunklpg/SaasHTML5/System/OperationLogs.html', 0, 1, 'index', 1180);

-- Dev20 Sites (id:1200)
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1200, 0, 'Dev20 Sites', '', NULL, 0, 1, 'index', 1200);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1210, 1200, 'develop', '', NULL, 1, 1, 'index', 1210);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1211, 1210, 'dev.trunklpg', '', 'https://test.117915.com/dev.trunklpg/home/default.aspx', 0, 1, 'index', 1211);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1212, 1210, 'dev.webapi', '', 'https://test.117915.com/dev.webapi/swagger', 0, 1, 'index', 1212);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1213, 1210, 'dev.saasapplpg', '', 'https://test.117915.com/dev.saasapplpg/', 0, 1, 'index', 1213);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1220, 1200, 'QA', '', NULL, 0, 1, 'index', 1220);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1221, 1220, 'dev.trunklpg', '', 'http://121.196.104.20:8013/dev.trunklpg/home/default.aspx', 0, 1, 'index', 1221);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1222, 1220, 'dev.webapi', '', 'http://121.196.104.20:8013/dev.webapi/swagger', 0, 1, 'index', 1222);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1223, 1220, 'dev.saasapplpg', '', 'http://121.196.104.20:8013/dev.saasapplpg/', 0, 1, 'index', 1223);

-- Test Sites (id:1300)
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1300, 0, 'Test Sites', '', NULL, 1, 1, 'index', 1300);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1310, 1300, 'iotlpg', '', 'http://iotlpg.117915.com/testclient/Login.aspx', 0, 1, 'index', 1310);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1320, 1300, 'iotlpg.saleapp.api', '', 'https://iotlpg.117915.com/iot.weigh.webapi.testsaleapp/swagger/index.html', 0, 1, 'index', 1320);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1330, 1300, '气瓶安全信息化管理系统', '', 'http://www.117915.cn:99/', 0, 1, 'index', 1330);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1340, 1300, 'trunklpg', '', 'https://lpg.117915.com/testlpg/home/default.aspx', 0, 1, 'index', 1340);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1350, 1300, 'trunklpg.SysManage', '', 'https://lpg.117915.com/testlpg/sysmanage/index.aspx', 0, 1, 'index', 1350);

-- Prod Sites (id:1400)
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1400, 0, 'Prod Sites', '', NULL, 0, 1, 'index', 1400);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1410, 1400, 'iotlpg', '', 'http://iotlpg.117915.com/client/Login.aspx', 0, 1, 'index', 1410);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1420, 1400, 'iotlpg.saleapp.api', '', 'https://iotlpg.117915.com/iot.weigh.webapi.saleapp/swagger/index.html', 0, 1, 'index', 1420);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1430, 1400, 'iotlpg.saleapp.api logs', '', 'https://iotlpg.117915.com/iot.weigh.webapi.saleapp/sejil', 0, 1, 'index', 1430);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1440, 1400, 'dcc.PublishCompConnChanged', '', 'http://iotlpg.117915.com/iot.weigh.dcc/Ajax/DccClient/PublishCompConnChanged.ashx', 0, 1, 'index', 1440);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1450, 1400, 'trunklpg', '', 'https://lpg.117915.com/lpg/Login.aspx', 0, 1, 'index', 1450);
INSERT INTO site_item (id, pId, name, desc, uri, isExpand, status, category, orderNum) VALUES (1460, 1400, 'trunklpg.SysManage', '', 'https://lpg.117915.com/lpg/sysmanage/index.aspx', 0, 1, 'index', 1460);
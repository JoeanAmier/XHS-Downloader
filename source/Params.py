from re import compile

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Cookie": "abRequestId=fd245483-beed-57b0-abfc-440b6a6be2aa; webBuild=3.4.1; xsecappid=xhs-pc-web; a1=189fe37918ezx1jqcbe9fin95cnxqj2ewcbc250yp50000234538; webId=9fff21309cfd3e4f380a6c75ed463803; websectiga=f47eda31ec99545da40c2f731f0630efd2b0959e1dd10d5fedac3dce0bd1e04d; sec_poison_id=003395d3-6520-4a02-851a-17d093203251; web_session=030037a3efee2e602d5d16fca4234a8a44466c; gid=yYjidqWi2KE4yYjidqWjyS28YduCyVASDdjiDvU3Ij2SIS28CAVJdJ888Jq42qY88J44DyjS",
}
API = "https://sns-img-qc.xhscdn.com/"
ID = compile(r'"traceId":"(.*?)"')

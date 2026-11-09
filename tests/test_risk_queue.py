import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, call, patch

from source.application.app import XHS
from source.application.request import Html
from source.application.risk import RiskControlError, check_risk_response
from source.GUI.backend import GuiBackend, TaskState
from source.translation import switch_language


def response(status=200, url="https://www.xiaohongshu.com/explore/note", text=""):
    return SimpleNamespace(status_code=status, url=url, text=text)


class RiskResponseTests(unittest.TestCase):
    def test_recognizes_rate_limits_and_verification_redirects(self):
        cases = [
            response(status=429),
            response(status=461),
            response(status=471),
            response(url="https://www.xiaohongshu.com/website-login/error?error_code=300012"),
            response(url="https://www.xiaohongshu.com/website-login/captcha?verifyType=124"),
            response(text='{"code":-10000,"message":"blocked"}'),
            response(text='{"code":-1,"message":"请求过于频繁"}'),
            response(text="<title>安全验证</title>"),
        ]
        for case in cases:
            with self.subTest(status=case.status_code, url=case.url, body=case.text):
                with self.assertRaises(RiskControlError):
                    check_risk_response(case)

    def test_unrelated_http_errors_and_note_text_are_not_risk(self):
        cases = [
            response(status=403),
            response(text='<title>讨论风控 - 小红书</title><p>访问频繁</p>'),
            response(text='{"code":0,"success":true,"message":"风控讨论"}'),
            response(url="https://example.com/website-login/error?error_code=300012"),
        ]
        for case in cases:
            with self.subTest(status=case.status_code, url=case.url, body=case.text):
                check_risk_response(case)

    def test_extracts_short_links_without_network(self):
        content = "文案 https://xhslink.com/AbCdEF\nhttps://www.xiaohongshu.com/explore/123?xsec_token=abc"
        self.assertEqual(
            XHS.find_task_links(content),
            ["https://xhslink.com/AbCdEF", "https://www.xiaohongshu.com/explore/123?xsec_token=abc"],
        )


class QueueRiskTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        switch_language("zh_CN")
        self.backend = GuiBackend()

    async def test_delay_keeps_two_decimal_places_at_both_bounds(self):
        with patch("source.GUI.backend.randint", side_effect=[100, 200, 500]), patch(
            "source.GUI.backend.asyncio.sleep", new_callable=AsyncMock
        ) as sleep:
            for _ in range(3):
                await self.backend._wait_between_notes()
        self.assertEqual(sleep.await_args_list, [call(1.0), call(2.0), call(5.0)])
        self.assertEqual(
            [item["message"] for item in self.backend.logs],
            ["等待 1.00 秒后处理下一篇笔记", "等待 2.00 秒后处理下一篇笔记", "等待 5.00 秒后处理下一篇笔记"],
        )

    async def test_adding_short_links_does_not_resolve_them_before_queue(self):
        self.backend.task_queue = asyncio.Queue()
        resolve = AsyncMock(side_effect=AssertionError("unexpected network request"))
        self.backend.xhs = SimpleNamespace(find_task_links=XHS.find_task_links, extract_links=resolve)
        tasks = await self.backend.create_tasks("https://xhslink.com/AbCdEF")
        self.assertEqual(tasks[0]["url"], "https://xhslink.com/AbCdEF")
        resolve.assert_not_awaited()

    async def test_metadata_risk_is_raised_before_sleep_or_retry(self):
        blocked = response(url="https://www.xiaohongshu.com/website-login/error?error_code=300012")
        client = SimpleNamespace(get=AsyncMock(return_value=blocked))
        manager = SimpleNamespace(
            print=lambda: print,
            retry=5,
            request_client=client,
            timeout=10,
            proxy=None,
            impersonate="chrome",
            avg_delay=6,
            get_headers=lambda url: {},
        )
        html = Html(manager)
        with patch("source.application.request.sleep_time", new_callable=AsyncMock) as delay:
            with self.assertRaises(RiskControlError):
                await html.request_url("https://www.xiaohongshu.com/explore/note")
        self.assertEqual(client.get.await_count, 1)
        delay.assert_not_awaited()

    async def test_script_task_risk_stops_the_whole_queue(self):
        self.backend.xhs = SimpleNamespace(
            downloader=SimpleNamespace(pause=Mock()),
            manager=SimpleNamespace(download_record=False),
            deal_script_tasks=AsyncMock(side_effect=RiskControlError()),
        )
        task = TaskState("task", "", script_data={"noteId": "123"})
        await self.backend._process_task(task)
        self.assertEqual(task.state, "pending")
        self.assertFalse(self.backend.downloads_resumed.is_set())
        self.backend.xhs.downloader.pause.assert_called_once()
        self.assertIn("当前账号风控中。请休息一下", [item["message"] for item in self.backend.logs])


if __name__ == "__main__":
    unittest.main()

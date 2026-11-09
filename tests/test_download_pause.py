"""Use real HTTP streams to verify global pause without Xiaohongshu credentials."""

import asyncio
import shutil
import threading
import time
import unittest
from contextlib import suppress
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import AsyncMock

from curl_cffi.requests import AsyncSession

from source.application.download import Download
from source.application.risk import RiskControlError
from source.GUI.backend import GuiBackend
from source.translation import _, switch_language


CONTENT = bytes(range(256)) * 2048


class DownloadPauseTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        switch_language("zh_CN")
        self.requests = []
        requests = self.requests
        slow_started = threading.Event()

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(self.path)
                if self.path == "/fail-exhausted" and requests.count(self.path) <= 2:
                    self.send_response(503)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                if self.path in {"/risk-once", "/paired-risk"} and requests.count(self.path) == 1:
                    if self.path == "/paired-risk":
                        slow_started.wait(2)
                        time.sleep(0.12)
                    self.send_response(429)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                if self.path in {"/risk-json", "/risk-json-no-length", "/risk-html"}:
                    data = (
                        "<title>安全验证</title>".encode("utf-8")
                        if self.path == "/risk-html"
                        else b'{"code":300012,"message":"blocked"}'
                    )
                    self.send_response(200)
                    content_type = "text/html" if self.path == "/risk-html" else "application/json"
                    self.send_header("Content-Type", content_type)
                    if self.path != "/risk-json-no-length":
                        self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                    return
                if self.path == "/slow-headers":
                    time.sleep(0.15)
                offset = int(self.headers.get("Range", "bytes=0-")[6:-1])
                if self.path == "/ignore-range":
                    offset = 0
                data = CONTENT[offset:]
                self.send_response(206 if offset else 200)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                with suppress(BrokenPipeError, ConnectionResetError, OSError):
                    for start in range(0, len(data), 4096):
                        self.wfile.write(data[start : start + 4096])
                        self.wfile.flush()
                        if self.path == "/slow":
                            slow_started.set()
                        time.sleep(0.004)

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        self.directory = TemporaryDirectory()
        root = Path(self.directory.name)
        self.temp = root / "temp"
        self.output = root / "output"
        self.temp.mkdir()
        self.output.mkdir()
        self.client = AsyncSession(timeout=0.2)
        sink = SimpleNamespace(write=lambda *args, **kwargs: None)
        manager = SimpleNamespace(
            print=lambda: sink,
            folder=self.output,
            temp=self.temp,
            chunk=None,
            download_client=self.client,
            blank_headers={},
            retry=1,
            folder_mode=False,
            image_format="jpeg",
            image_download=True,
            video_download=True,
            video_cover_download=False,
            live_download=False,
            author_archive=False,
            write_mtime=False,
            move=lambda source, target, *args: shutil.move(source, target),
            delete=lambda path: path.unlink(missing_ok=True),
        )
        self.downloader = Download(manager)
        self.downloader.SEMAPHORE = asyncio.Semaphore(2)
        self.events = []
        self.jobs = []
        self.backend = GuiBackend()
        self.backend.settings = {"disclaimer_accepted": True}
        self.backend._settings_payload = lambda: {}

        async def extract_links(content):
            return content.split()

        async def extract(url, download, *, task_id, progress_callback, result_callback, **kwargs):
            result = await self.download(task_id, url, progress_callback)
            result_callback({"success": int(all(result))})

        self.backend.xhs = SimpleNamespace(
            downloader=self.downloader,
            manager=SimpleNamespace(download_record=False),
            extract_links=extract_links,
            find_task_links=lambda content: content.split(),
            extract=extract,
        )
        self.backend.task_queue = asyncio.Queue()
        self.backend._wait_between_notes = AsyncMock()

    async def asyncTearDown(self):
        for job in self.jobs:
            job.cancel()
        for job in self.jobs:
            with suppress(asyncio.CancelledError):
                await job
        await self.client.close()
        await asyncio.to_thread(self.server.shutdown)
        self.server.server_close()
        self.server_thread.join()
        self.directory.cleanup()

    async def until(self, predicate):
        async with asyncio.timeout(5):
            while not predicate():
                await asyncio.sleep(0.01)

    def start(self, coroutine):
        job = asyncio.create_task(coroutine)
        self.jobs.append(job)
        return job

    async def download(self, name, url=None, progress=None):
        return await self.downloader.run(
            [url or self.url + "/file"], [], None, self.output, name, _("视频"), 0,
            progress=progress or self.events.append, task_id=name,
        )

    async def test_pause_freezes_progress_and_resumes_queued_tasks(self):
        self.start(self.backend._worker_loop())
        first = (await self.backend.create_tasks(self.url + "/first"))[0]["task_id"]
        await self.until(lambda: any(f.get("completed_bytes", 0) > 16384 for f in self.backend.files.values()))
        self.assertTrue(await self.backend.pause_all())
        self.assertTrue(await self.backend.pause_all())
        second = (await self.backend.create_tasks(self.url + "/second"))[0]["task_id"]
        await asyncio.sleep(0.05)  # Let a disk write already in flight finish.
        before = [(f["completed_bytes"], f["total_bytes"]) for f in self.backend.files.values()]
        await asyncio.sleep(1.25)  # Longer than curl's one-second low-speed timeout.
        self.assertEqual(before, [(f["completed_bytes"], f["total_bytes"]) for f in self.backend.files.values()])
        self.assertEqual(self.requests, ["/first"])
        snapshot = await self.backend.snapshot()
        self.assertTrue(snapshot["downloads_paused"])
        self.assertEqual([t["state"] for t in snapshot["tasks"]], ["paused", "pending"])
        self.assertEqual(snapshot["files"][0]["state"], "paused")
        self.assertEqual(self.backend.tasks[first].state, "processing")
        self.assertEqual(self.backend.files[snapshot["files"][0]["file_id"]]["state"], "downloading")
        self.assertFalse((await self.backend.save_settings({}))["ok"])
        self.assertTrue(await self.backend.resume_all())
        self.assertTrue(await self.backend.resume_all())
        await asyncio.wait_for(self.backend.task_queue.join(), 5)
        self.assertEqual(self.requests, ["/first", "/second"])
        for task_id in (first, second):
            self.assertEqual(self.backend.tasks[task_id].state, "success")
            self.assertEqual((self.output / f"{task_id}.mp4").read_bytes(), CONTENT)
        self.assertFalse((await self.backend.snapshot())["downloads_paused"])

    async def test_idle_pause_blocks_new_tasks_and_allows_cancelling_pending(self):
        await self.backend.pause_all()
        self.start(self.backend._worker_loop())
        cancelled = (await self.backend.create_tasks(self.url + "/cancelled"))[0]["task_id"]
        await asyncio.sleep(0.05)
        self.assertTrue(await self.backend.cancel_task(cancelled))
        self.assertEqual(await self.backend.clear_finished(), 1)
        pending = (await self.backend.create_tasks(self.url + "/pending"))[0]["task_id"]
        await asyncio.sleep(0.05)
        self.assertEqual(self.requests, [])
        self.assertEqual(self.backend.tasks[pending].state, "pending")
        await self.backend.resume_all()
        await asyncio.wait_for(self.backend.task_queue.join(), 5)
        self.assertEqual(self.requests, ["/pending"])
        self.assertEqual(self.backend.tasks[pending].state, "success")

    async def test_parallel_files_resume_without_duplicate_or_missing_bytes(self):
        # Pre-existing partial data must survive pause/resume as well.
        (self.temp / "first.mp4").write_bytes(CONTENT[:8192])
        first = self.start(self.download("first", self.url + "/first"))
        second = self.start(self.download("second", self.url + "/second"))
        await self.until(lambda: len({e["task_id"] for e in self.events if e["completed_bytes"] > 16384}) == 2)
        self.downloader.pause()
        third = self.start(self.download("third", self.url + "/third"))
        await asyncio.sleep(0.05)
        count = len(self.events)
        await asyncio.sleep(0.1)
        self.assertEqual(len(self.events), count)
        self.assertNotIn("/third", self.requests)
        self.downloader.resume()
        self.assertEqual(await asyncio.wait_for(asyncio.gather(first, second, third), 5), [[True]] * 3)
        self.assertEqual(len(self.requests), 3)
        for name in ("first", "second", "third"):
            self.assertEqual((self.output / f"{name}.mp4").read_bytes(), CONTENT)

    async def test_pause_while_waiting_for_headers(self):
        job = self.start(self.download("headers", self.url + "/slow-headers"))
        await self.until(lambda: self.requests)
        self.downloader.pause()
        await asyncio.sleep(0.3)
        self.assertEqual(self.events, [])
        self.downloader.resume()
        self.assertEqual(await asyncio.wait_for(job, 5), [True])
        self.assertEqual((self.output / "headers.mp4").read_bytes(), CONTENT)

    async def test_retry_after_failure_and_cleanup_completes_same_note(self):
        self.start(self.backend._worker_loop())
        task_id = (await self.backend.create_tasks(self.url + "/fail-exhausted"))[0]["task_id"]
        await asyncio.wait_for(self.backend.task_queue.join(), 5)
        self.assertEqual(self.backend.tasks[task_id].state, "failed")
        self.assertEqual(len(self.requests), 2)
        self.assertEqual(await self.backend.clear_finished(), 0)
        self.assertIn(task_id, self.backend.tasks)
        self.assertTrue(await self.backend.retry_task(task_id))
        self.assertFalse(await self.backend.retry_task(task_id))
        await asyncio.wait_for(self.backend.task_queue.join(), 5)
        self.assertEqual(self.backend.tasks[task_id].state, "success")
        self.assertEqual(self.requests, ["/fail-exhausted"] * 3)
        self.assertEqual((self.output / f"{task_id}.mp4").read_bytes(), CONTENT)
        self.assertEqual(await self.backend.clear_finished(), 1)
        self.assertNotIn(task_id, self.backend.tasks)

    async def test_cancelling_a_paused_transfer_does_not_hang(self):
        job = self.start(self.download("cancel"))
        await self.until(lambda: any(e["completed_bytes"] > 16384 for e in self.events))
        self.downloader.pause()
        await asyncio.sleep(0.05)
        job.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await asyncio.wait_for(job, 1)
        self.assertFalse(self.downloader._responses)

    async def test_risk_pauses_queue_and_retries_same_note_before_next(self):
        self.start(self.backend._worker_loop())
        first = (await self.backend.create_tasks(self.url + "/risk-once"))[0]["task_id"]
        second = (await self.backend.create_tasks(self.url + "/next"))[0]["task_id"]
        await self.until(lambda: not self.backend.downloads_resumed.is_set())
        self.assertEqual(self.requests, ["/risk-once"])
        self.assertEqual(self.backend.tasks[first].state, "pending")
        self.assertEqual(self.backend.tasks[second].state, "pending")
        self.assertIn("当前账号风控中。请休息一下", [item["message"] for item in self.backend.logs])
        await asyncio.sleep(0.15)
        self.assertEqual(self.requests, ["/risk-once"])
        await self.backend.resume_all()
        await asyncio.wait_for(self.backend.task_queue.join(), 5)
        self.assertEqual(self.requests, ["/risk-once", "/risk-once", "/next"])
        self.assertEqual(self.backend.tasks[first].state, "success")
        self.assertEqual(self.backend.tasks[second].state, "success")
        self.assertEqual((self.output / f"{first}.mp4").read_bytes(), CONTENT)
        self.assertEqual(self.backend._wait_between_notes.await_count, 2)

    async def test_parallel_risk_saves_partial_data_and_cancels_siblings(self):
        async def image_download():
            return await self.downloader.run(
                [self.url + "/slow", self.url + "/paired-risk"],
                [None, None], None, self.output, "note", _("图文"), 0,
                progress=self.events.append, task_id="note",
            )

        with self.assertRaises(RiskControlError):
            await image_download()
        self.assertEqual(self.requests.count("/paired-risk"), 1)
        self.assertFalse(self.downloader._responses)
        self.assertGreater((self.temp / "note_1.jpeg").stat().st_size, 0)
        self.assertEqual(await asyncio.wait_for(image_download(), 5), [True, True])
        self.assertEqual((self.output / "note_1.jpeg").read_bytes(), CONTENT)
        self.assertEqual((self.output / "note_2.jpeg").read_bytes(), CONTENT)

    async def test_json_risk_response_does_not_retry(self):
        with self.assertRaises(RiskControlError):
            await self.download("json-risk", self.url + "/risk-json")
        self.assertEqual(self.requests, ["/risk-json"])
        self.assertFalse((self.output / "json-risk.mp4").exists())

    async def test_verification_page_and_json_without_length_stop_download(self):
        for path in ("/risk-json-no-length", "/risk-html"):
            with self.subTest(path=path), self.assertRaises(RiskControlError):
                await self.download(path[1:], self.url + path)
        self.assertEqual(self.requests, ["/risk-json-no-length", "/risk-html"])
        self.assertFalse((self.output / "risk-json-no-length.mp4").exists())
        self.assertFalse((self.output / "risk-html.mp4").exists())

    async def test_restart_is_safe_when_server_ignores_range(self):
        (self.temp / "range.mp4").write_bytes(CONTENT[:8192])
        self.assertEqual(await self.download("range", self.url + "/ignore-range"), [True])
        self.assertEqual((self.output / "range.mp4").read_bytes(), CONTENT)

    async def test_pausing_during_interval_prevents_next_note_start(self):
        waiting = asyncio.Event()
        finish_interval = asyncio.Event()

        async def interval():
            waiting.set()
            await finish_interval.wait()

        self.backend._wait_between_notes = interval
        self.start(self.backend._worker_loop())
        await self.backend.create_tasks(self.url + "/first")
        second = (await self.backend.create_tasks(self.url + "/next"))[0]["task_id"]
        await asyncio.wait_for(waiting.wait(), 5)
        await self.backend.pause_all()
        finish_interval.set()
        await asyncio.sleep(0.1)
        self.assertEqual(self.requests, ["/first"])
        self.assertEqual(self.backend.tasks[second].state, "pending")
        await self.backend.resume_all()
        await asyncio.wait_for(self.backend.task_queue.join(), 5)
        self.assertEqual(self.requests, ["/first", "/next"])


if __name__ == "__main__":
    unittest.main()

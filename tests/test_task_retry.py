import asyncio
import unittest
from contextlib import suppress
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from source.GUI.backend import GuiBackend, TaskState
from source.translation import switch_language


class TaskRetryTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        switch_language("zh_CN")
        self.backend = GuiBackend()
        self.backend.task_queue = asyncio.Queue()
        self.backend._wait_between_notes = AsyncMock()
        self.backend.xhs = SimpleNamespace(
            downloader=SimpleNamespace(pause=Mock(), resume=Mock()),
            manager=SimpleNamespace(download_record=False),
        )

    async def test_cleanup_retains_failed_tasks_and_their_file_progress(self):
        states = ("success", "failed", "skipped", "cancelled", "pending", "processing")
        self.backend.tasks = {state: TaskState(state, state, state=state) for state in states}
        self.backend.files = {
            state: {"task_id": state, "state": "failed" if state == "failed" else "completed"}
            for state in states
        }
        self.assertEqual(await self.backend.clear_finished(), 3)
        self.assertEqual(set(self.backend.tasks), {"failed", "pending", "processing"})
        self.assertEqual(set(self.backend.files), {"failed", "pending", "processing"})
        self.assertEqual(self.backend.files["failed"]["state"], "failed")
        self.assertEqual(await self.backend.clear_finished(), 0)

    async def test_retry_preserves_parameters_completed_files_and_rejects_duplicate_clicks(self):
        task = TaskState("failed", "https://xhslink.com/example", source="monitor", state="failed", index=[2, 4])
        self.backend.tasks[task.task_id] = task
        self.backend.files = {
            "done": {"task_id": task.task_id, "state": "completed", "completed_bytes": 50},
            "partial": {"task_id": task.task_id, "state": "failed", "completed_bytes": 20},
        }
        self.assertTrue(await self.backend.retry_task(task.task_id))
        self.assertFalse(await self.backend.retry_task(task.task_id))
        self.assertFalse(await self.backend.retry_task("missing"))
        self.assertEqual(self.backend.task_queue.qsize(), 1)
        self.assertIs(self.backend.tasks[task.task_id], task)
        self.assertEqual((task.url, task.source, task.index), ("https://xhslink.com/example", "monitor", [2, 4]))
        self.assertEqual(self.backend.files["done"]["state"], "completed")
        self.assertEqual(self.backend.files["partial"], {"task_id": task.task_id, "state": "pending", "completed_bytes": 20})
        self.assertTrue(await self.backend.cancel_task(task.task_id))
        self.assertEqual(self.backend.files["partial"]["state"], "cancelled")
        self.assertEqual(self.backend.files["done"]["state"], "completed")

    async def test_bulk_retry_only_queues_failed_tasks_and_respects_pause(self):
        script = {"noteId": "script-note"}
        self.backend.tasks = {
            "manual": TaskState("manual", "note-url", state="failed", index=[1]),
            "script": TaskState("script", "", state="failed", script_data=script, index=[2]),
            "success": TaskState("success", "done", state="success"),
            "pending": TaskState("pending", "pending"),
        }
        await self.backend.pause_all()
        self.assertEqual(await self.backend.retry_failed(), 2)
        self.assertEqual(await self.backend.retry_failed(), 0)

        async def extracted(*args, result_callback, **kwargs):
            result_callback({"success": 1})

        self.backend.xhs.extract = AsyncMock(side_effect=extracted)
        self.backend.xhs.deal_script_tasks = AsyncMock(side_effect=extracted)
        worker = asyncio.create_task(self.backend._worker_loop())
        try:
            await asyncio.sleep(0)
            self.backend.xhs.extract.assert_not_awaited()
            self.backend.xhs.deal_script_tasks.assert_not_awaited()
            self.assertFalse(self.backend.downloads_resumed.is_set())
            await self.backend.resume_all()
            await asyncio.wait_for(self.backend.task_queue.join(), 2)
            self.assertEqual(self.backend.tasks["manual"].state, "success")
            self.assertEqual(self.backend.tasks["script"].state, "success")
            self.assertEqual(self.backend.tasks["pending"].state, "pending")
            self.backend.xhs.extract.assert_awaited_once()
            self.assertEqual(self.backend.xhs.extract.await_args.args[0], "note-url")
            self.assertEqual(self.backend.xhs.extract.await_args.kwargs["index"], [1])
            self.backend.xhs.deal_script_tasks.assert_awaited_once()
            self.assertIs(self.backend.xhs.deal_script_tasks.await_args.args[0], script)
            self.assertEqual(self.backend.xhs.deal_script_tasks.await_args.args[1], [2])
            self.backend._wait_between_notes.assert_awaited_once()
        finally:
            worker.cancel()
            with suppress(asyncio.CancelledError):
                await worker

    async def test_retry_without_a_running_queue_keeps_failure(self):
        self.backend.tasks["failed"] = TaskState("failed", "note", state="failed")
        self.backend.task_queue = None
        self.assertFalse(await self.backend.retry_task("failed"))
        self.assertEqual(await self.backend.retry_failed(), 0)
        self.assertEqual(self.backend.tasks["failed"].state, "failed")


if __name__ == "__main__":
    unittest.main()

"""Exercise failed-task buttons and cleanup via the real Windows WebView bridge.

Uses temporary settings and an idle queue; no Xiaohongshu requests or cookies.
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import webview

from source.GUI import backend as backend_module
from source.GUI.backend import GuiApi, GuiBackend, TaskState
from source.module import ROOT, Settings


class TestBackend(GuiBackend):
    async def _initialize(self):
        self.settings = self.settings_manager.run()
        self.settings["disclaimer_accepted"] = True
        self.task_queue = asyncio.Queue()
        self.downloads_resumed.clear()
        self.tasks = {
            "single": TaskState("single", "https://xhslink.com/test", state="failed"),
            "bulk": TaskState("bulk", "", state="failed", script_data={"noteId": "test"}, display_text="test"),
            "done": TaskState("done", "done", state="success"),
        }


def main():
    outcomes = []
    with TemporaryDirectory() as directory:
        backend_module.VOLUME = Path(directory)
        backend = TestBackend()
        backend.settings_manager = Settings(Path(directory))
        api = GuiApi(backend)
        api._qr_login._diagnostic_path = None
        window = webview.create_window("Retry smoke", (ROOT / "static/GUI/index.html").as_uri(),
                                       js_api=api, hidden=True, width=1280, height=720)
        api._bind_window(window)
        backend.start()

        def until(script):
            end = time.monotonic() + 12
            while time.monotonic() < end:
                if window.evaluate_js(script):
                    return
                time.sleep(0.1)
            raise AssertionError("UI transition timed out: " + script)

        def run():
            try:
                window.events.loaded.wait(12)
                until("document.getElementById('startupScreen').hidden")
                window.evaluate_js("document.querySelector('[data-view=queue]').click()")
                until("document.querySelectorAll('#queueList [data-action=retry]').length===2")
                window.evaluate_js("document.getElementById('clearFinished').click()")
                until("document.querySelectorAll('#queueList .queue-item').length===2")
                assert set(backend.tasks) == {"single", "bulk"}
                outcomes.append("cleanup retains failures: PASS")

                window.evaluate_js("document.querySelector('#queueList [data-task-id=single] [data-action=retry]').click()")
                until("document.querySelector('#queueList [data-task-id=single]').dataset.state==='pending'")
                assert backend.task_queue.qsize() == 1
                outcomes.append("single retry: PASS")

                window.evaluate_js("document.getElementById('retryFailedTasks').click()")
                until("document.getElementById('retryFailedTasks').disabled && document.querySelectorAll('#queueList [data-state=pending]').length===2")
                assert backend.task_queue.qsize() == 2
                assert not backend.downloads_resumed.is_set()
                assert backend.tasks["bulk"].script_data == {"noteId": "test"}
                outcomes.append("bulk retry preserves pause and payload: PASS")

                layout = window.evaluate_js("""(() => {
                    const page = document.querySelector('[data-page=queue]');
                    return {width:innerWidth, fits:[...page.querySelectorAll('.heading-actions button')].every(b=>{
                        const r=b.getBoundingClientRect(); return r.left>=0 && r.right<=innerWidth;
                    }), overflow:page.scrollWidth>page.clientWidth};
                })()""")
                assert layout["fits"] and not layout["overflow"], layout
                outcomes.append("1280px toolbar fit: PASS")
            except Exception as error:
                outcomes.append("FAIL: " + str(error))
            finally:
                window.destroy()

        try:
            webview.start(run)
        finally:
            backend.stop()
    print(json.dumps(outcomes))
    return 0 if len(outcomes) == 4 and all(s.endswith("PASS") for s in outcomes) else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Screenshot the workflow diagram on the front page, once per step.

Each image shows the whole workflow (docs/index.md, the .rb-flow block) with
one box marked "You are here" and the others dimmed. The other pages lead
with the image for their step (docs/images/here/<step>.png).

Needs a built site:  cd docs && jupyter-book build --html --execute
Then:                python scripts/workflow_screenshots.py

Uses Playwright's Chromium; set CHROMIUM=/path/to/chromium to use a
system browser instead (no `playwright install` needed then).
Run by .github/workflows/workflow-screenshots.yml when docs/index.md changes.
"""
import functools
import http.server
import os
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs" / "_build" / "html"
OUT = ROOT / "docs" / "images" / "here"

# CSS class of each box in docs/index.md -> output file name.
STEPS = {
    "rb-s1": "step-1",
    "rb-s2": "step-2",
    "rb-s3": "step-3",
    "rb-s4": "step-4",
    "rb-s5": "step-5",
    "rb-s6": "step-6",
    "rb-journal": "journal",
}

# Marks one box; the styles (.rb-focus, .rb-here, .rb-here-tag) are in docs/assets/site.css.
MARK = """cls => {
  const flow = document.querySelector('.rb-flow');
  flow.classList.add('rb-focus');
  flow.querySelectorAll('.rb-here').forEach(e => e.classList.remove('rb-here'));
  flow.querySelectorAll('.rb-here-tag').forEach(e => e.remove());
  const box = flow.querySelector('.' + cls);
  box.classList.add('rb-here');
  const tag = document.createElement('span');
  tag.className = 'rb-here-tag';
  tag.textContent = 'You are here';
  box.prepend(tag);
}"""


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(directory):
    handler = functools.partial(QuietHandler, directory=str(directory))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main():
    if not (SITE / "index.html").exists():
        raise SystemExit(f"No built site at {SITE}. Build it first (see docstring).")
    OUT.mkdir(parents=True, exist_ok=True)
    server = serve(SITE)
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
        page = browser.new_page(viewport={"width": 1280, "height": 1600},
                                device_scale_factor=1, color_scheme="light")
        page.goto(url, wait_until="networkidle")
        flow = page.locator(".rb-flow")
        flow.scroll_into_view_if_needed()
        # Hover lift and transitions would make shots differ run to run.
        page.add_style_tag(content=".rb-step{transition:none!important;transform:none!important}")
        for cls, name in STEPS.items():
            page.evaluate(MARK, cls)
            path = OUT / f"{name}.png"
            # Viewport coordinates (the flow fits in the viewport). Padding keeps the
            # outline and shadow; little at the top, where the heading would show.
            box = flow.bounding_box()
            pad, top = 16, 6
            page.screenshot(path=str(path), clip={
                "x": box["x"] - pad, "y": box["y"] - top,
                "width": box["width"] + 2 * pad, "height": box["height"] + top + pad,
            })
            print(f"wrote {path.relative_to(ROOT)}")
        browser.close()
    server.shutdown()


if __name__ == "__main__":
    main()

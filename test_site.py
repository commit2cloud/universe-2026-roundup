"""Check the self-contained customer guide with Playwright and Chromium."""

import contextlib
import http.server
import pathlib
import threading

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def log_message(self, _format, *_args):
        pass


@contextlib.contextmanager
def serve():
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def main():
    with serve() as url, sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1360, "height": 1000})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(url)
        assert page.locator(".entry:visible").count() == 35
        links = page.locator(".announcement").evaluate_all(
            "(items) => items.map(item => item.href)"
        )
        assert len(set(links)) == 35
        assert all(link.startswith("https://github.blog/changelog/2026-10-") for link in links)
        ids = page.locator("[id]").evaluate_all("(items) => items.map(item => item.id)")
        assert len(ids) == len(set(ids))
        assert page.evaluate("""() => [...document.querySelectorAll('a[href^="#"]')]
            .every(a => document.getElementById(a.hash.slice(1)))""")

        page.select_option("#category", "security")
        assert page.locator(".entry:visible").count() == 6
        assert page.locator(".group:visible").count() == 1
        page.fill("#search", "  REACHABILITY  TypeScript ")
        assert page.locator(".entry:visible").count() == 1
        assert page.locator("#dependabot-reachability").is_visible()
        page.select_option("#category", "enterprise")
        assert page.locator("#empty").is_visible()
        assert page.locator(".group:visible").count() == 0
        page.click('button[type="reset"]')
        assert page.locator(".entry:visible").count() == 35
        assert page.locator("#search").input_value() == ""
        assert not page.locator("#empty").is_visible()
        page.fill("#search", "<script>no-match</script>")
        assert page.locator("#empty").is_visible()
        page.locator('.highlights a[href="#copilot-app"]').click()
        assert page.locator("#copilot-app").is_visible()
        assert page.locator(".entry:visible").count() == 35

        page.goto(url + "/?scoutTheme=dark#enterprise-copilot")
        assert page.locator("html").get_attribute("data-theme") == "dark"
        assert page.locator("#enterprise-copilot").is_visible()
        page.click("#theme-toggle")
        assert page.locator("html").get_attribute("data-theme") == "light"
        page.click("#theme-toggle")
        assert page.locator("html").get_attribute("data-theme") == "dark"

        for width in (320, 390, 768, 1360):
            page.set_viewport_size({"width": width, "height": 900})
            page.goto(url)
            assert page.evaluate(
                "document.documentElement.scrollWidth === document.documentElement.clientWidth"
            ), f"Horizontal overflow at {width}px"
            assert page.locator(".entry:visible").count() == 35

        no_js = browser.new_context(java_script_enabled=False)
        plain = no_js.new_page()
        plain.goto(url)
        assert plain.locator(".entry:visible").count() == 35
        assert plain.locator(".announcement").count() == 35
        assert not plain.locator("#filters").is_visible()
        assert not plain.locator("#theme-toggle").is_visible()
        no_js.close()
        assert not errors, errors
        browser.close()
    print("PASS: 35 announcements, search, categories, reset, anchors, themes, mobile, and no-JS.")


if __name__ == "__main__":
    main()

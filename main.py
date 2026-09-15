import os
from datetime import datetime
from playwright.sync_api import Page

_screenshots_folder = None


def create_screenshot_folder(base_name="screenshots"):
    """Создаёт папку с timestamp ОДИН РАЗ за запуск"""
    global _screenshots_folder
    if _screenshots_folder is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        _screenshots_folder = os.path.join("reports", f"{base_name}_{timestamp}")
        os.makedirs(_screenshots_folder, exist_ok=True)
    return _screenshots_folder


def login_to_site(
    page: Page,
    url: str,
    username: str,
    password: str,
):
    page.goto(url)
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()
    page.wait_for_load_state("load")

import os
from datetime import datetime
from playwright.sync_api import Page


def create_screenshot_folder(base_name="screenshots"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = os.path.join("reports", f"{base_name}_{timestamp}")
    os.makedirs(folder, exist_ok=True)
    return folder


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

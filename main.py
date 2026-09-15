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
    page.locator('input[autocomplete="username"]:visible').fill(username)
    page.locator('input[autocomplete="current-password"]:visible').fill(password)
    page.get_by_role("button", name="Sign in", exact=True).click()
    page.wait_for_load_state("networkidle")

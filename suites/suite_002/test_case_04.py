from playwright.sync_api import Page, expect
from main import create_screenshot_folder


def test_screenshot_java(page: Page):
    screenshots_dir = create_screenshot_folder("screenshots")
    page.goto("https://java.com")
    page.screenshot(path=f"{screenshots_dir}/04.png")
    expect(page).to_have_title("Java | Oracle")

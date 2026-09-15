from playwright.sync_api import Page, expect
from main import create_screenshot_folder


def test_screenshot_example(page: Page):
    screenshots_dir = create_screenshot_folder("screenshots")
    page.goto("https://example.com")
    page.screenshot(path=f"{screenshots_dir}/01.png")
    expect(page).to_have_title("Example Domain")

from playwright.sync_api import Page, expect
from main import create_screenshot_folder


def test_screenshot_google(page: Page):
    screenshots_dir = create_screenshot_folder("screenshots")
    page.goto("https://google.com")
    page.screenshot(path=f"{screenshots_dir}/02.png")
    expect(page).to_have_title("Google")

from playwright.sync_api import Page, expect
from main import create_screenshot_folder


def test_screenshot_wikipedia(page: Page):
    screenshots_dir = create_screenshot_folder()
    page.goto("https://wikipedia.org/")
    page.screenshot(path=f"{screenshots_dir}/02.png")
    expect(page).to_have_title("Wikipedia")

from playwright.sync_api import Page, expect
from main import create_screenshot_folder, login_to_site


def test_linkedin_login(page: Page):
    screenshots_dir = create_screenshot_folder("screenshots")

    login_to_site(
        page,
        url="https://linkedin.com/login",
        username="filippov.alexander.l@gmail.com",
        password="alf1020304050",
    )

    page.screenshot(path=f"{screenshots_dir}/linkedin_feed.png")

    # ✅ Проверка по URL
    expect(page).to_have_url("https://www.linkedin.com/feed/")

from playwright.sync_api import Page, expect
from main import create_screenshot_folder, login_to_site


def test_linkedin_login(page: Page):
    screenshots_dir = create_screenshot_folder("screenshots")

    login_to_site(
        page,
        url="https://www.saucedemo.com/",
        username="standard_user",
        password="secret_sauce",
    )

    page.screenshot(path=f"{screenshots_dir}/05.png")

    # ✅ Проверка по URL
    # expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

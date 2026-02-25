import os
from dotenv import load_dotenv
from playwright.sync_api import Page, expect, sync_playwright


load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def test_signup(page: Page):
    """Signup the user with email and password"""

    # Fill form
    page.goto(f"{BASE_URL}/signup")
    page.fill("input[name='name']", os.getenv("NAME"))
    page.fill("input[name='email']", os.getenv("EMAIL"))
    page.fill("input[name='phone_number']", os.getenv("PHONE_NUMBER"))
    page.fill("input[name='business_name']", os.getenv("BUSINESS_NAME"))
    page.fill("textarea[name='business_description']", os.getenv("BUSINESS_DESCRIPTION"))
    page.fill("input[name='password']", os.getenv("PASSWORD"))
    
    # Enable submit button and click
    submit_btn = page.locator("button[type='submit']")
    expect(submit_btn).to_be_enabled(timeout=40000)
    submit_btn.click()

    # Check for the confirmation page
    confirmation_header = page.locator("h6", has_text="Confirm your email address")
    confirmation_text = page.locator("p.sm", has_text="We’ve sent a validation email")

    # Assert the confirmation header and text has the email address
    expect(confirmation_header).to_be_visible()
    expect(confirmation_text).to_contain_text(os.getenv("EMAIL"))



if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        test_signup(page)
        browser.close()


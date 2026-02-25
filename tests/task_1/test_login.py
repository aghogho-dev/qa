import os, time, re, pytest
from dotenv import load_dotenv 
from playwright.sync_api import Page, expect
from get_otp import fetch_otp_with_retry
from scope_data import scopes_dict

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

@pytest.fixture
def loggedIn(page: Page):

    """LogIn to Email"""

    page.set_viewport_size({"width": 1366, "height": 768})  # Change to screen size

    # Navigate to login
    page.goto(f"{BASE_URL}/login")
    # Fill login form
    email_input = page.locator("input[name='email']")
    expect(email_input).to_be_visible()
    email_input.fill(os.getenv("EMAIL"))
    page.fill("input[name='password']", os.getenv("PASSWORD"))
    # Submit the form
    submit_btn = page.locator("button[type='submit']")
    expect(submit_btn).to_be_enabled()
    submit_btn.click()

    return page

@pytest.fixture
def authenticatedPage(loggedIn: Page):
    """Autheticate with OTP"""

    page = loggedIn 

    otp_header = page.locator(".modal-header .title", has_text="Two-Factor Authentication")

    try:
        # Wait until page is visible after login
        otp_header.wait_for(state="visible", timeout=3000)
        is_otp_required = True
    except:
        is_otp_required = False

    if is_otp_required:

        print("OTP requested. Fetching code...")

        otp = fetch_otp_with_retry()

        if otp:

            otp_container = page.locator(".pincode-input-text").first
            otp_container.wait_for(state="visible", timeout=5000)

            otp_inputs = page.locator(".pincode-input-text input")
            expect(otp_inputs.first).to_be_visible()

            otp_inputs.first.click()
            page.keyboard.type(otp, delay=50)

            otp_btn = page.locator("button:has-text('Confirm')")
            expect(otp_btn).not_to_have_attribute("disabled", "disabled", timeout=60000)
            # expect(otp_btn).to_be_enabled(timeout=60000)
            otp_btn.click()

    return page


def test_createApp(authenticatedPage: Page, requested_scopes: str):
    """After Login and Authentication, Create App, and get API key"""

    page = authenticatedPage

    # Create a task after login and authentication
    create_app_task = page.locator("div._get-started_todo_container__0-K1K", has_text="Create an app")
    create_app_btn = create_app_task.locator("button")
    
    expect(create_app_btn).to_be_visible(timeout=15000)
    create_app_btn.click()

    page.wait_for_url("**/app", timeout=10000)

    create_app_main_btn = page.locator("button", has=page.locator(".create-app-icon"))
    expect(create_app_main_btn).to_be_visible()
    create_app_main_btn.click()

    # Find the slideplane and fill the form: Name and Description fields
    slidepane = page.locator(".slidepane")

    pane = slidepane.filter(has_text="Create an app")
    pane.locator("input[name='name']").fill(f"Auto App {int(time.time())}")
    pane.locator("input[name='description']").fill("Automated testing of API Scopes.")

    # Get all the checkboxe in scope
    categories = slidepane.locator("div[class*='_multi-select-checkbox_selected_category__']")
    count = categories.count()

    for i in range(count):
        categories.nth(i).click()
        page.wait_for_timeout(200)

    # Check whether --scope is passed in the command and determine what to do
    # Select all scope if --scope is not passed
    if requested_scopes.lower() == "all":
        selected_scopes = list(scopes_dict.keys())
    else:
        selected_scopes = [s.strip() for s in requested_scopes.split(",")]
        selected_scopes = [k for k in selected_scopes if k in scopes_dict]

    # Tick the checkboxes of the scopes
    for scope in selected_scopes:
        scope_id = scopes_dict[scope]
        checkbox = slidepane.locator(f"input[name='{scope_id}']")

        checkbox.scroll_into_view_if_needed()

        if not checkbox.is_checked():
            checkbox.check()

    # Create app
    create_btn = slidepane.locator("button[type='submit']", has_text="Create app")
    expect(create_btn).to_be_enabled()
    page.pause()
    create_btn.click()

    page.wait_for_load_state("load")

    # Wait until the App created successfully shows up
    success_title = page.get_by_text("App created successfully")
    expect(success_title).to_be_visible(timeout=15000)

    # Grab the APP ID
    app_id = page.locator(".input-container", has_text="App ID").locator("input")
    expect(app_id).not_to_have_value("", timeout=10000)
    app_id = app_id.input_value()

    # Grab the API Key
    api_key = page.locator(".input-container", has_text="API Key").locator("input")
    expect(api_key).not_to_have_value("", timeout=10000)
    api_key = api_key.input_value()
    
    # Write APP ID and API Key values to .env_api
    with open(".env_api", "w") as f:
        f.write(f"APP_ID={app_id}\n")
        f.write(f"API_KEY={api_key}\n")

    page.pause()

    page.locator("button", has_text="Done").click()
    

if __name__ == "__main__":
    pytest.main([__file__, "-s"])







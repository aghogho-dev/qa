import os 
import re 
import time
import html
from imap_tools import MailBox, AND 
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone 
from playwright.sync_api import Page, expect, sync_playwright
from bs4 import BeautifulSoup
import pytz


load_dotenv()

def get_latest_validate_email():
    """Validate created account after SignUp"""

    wat_tz = pytz.timezone('Africa/Lagos')
    threshold = datetime.now(wat_tz) - timedelta(minutes=15)

    with MailBox(os.getenv("IMAP_SERVER")).login(
            os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD")) as mailbox:
    
        mailbox.folder.set("[Gmail]/All Mail")

        for msg in mailbox.fetch(AND(from_='support@lendsqr.com', subject="Validate your account"), limit=1, reverse=True):
            if msg.date.astimezone(wat_tz) < threshold:
                continue  

            soup = BeautifulSoup(msg.html, "html.parser")
            match = soup.find('a', string=lambda t: "Setup your account" in t)

            if match:
                setup_url = match["href"]
                print(f"Validation link found: {setup_url}")
                return setup_url
    return False


def test_validate_email(page:Page, retries:int=10):
    print("Waiting to Validate Email")

    for i in range(retries):
        
        setup_url = get_latest_validate_email()

        if setup_url:
            page.goto(setup_url)
            break
                    
        print(f"Email not found yet. Retrying...")
        time.sleep(10)

    expect(page).to_have_url(re.compile(r".*/login.*"), timeout=10000)
    print("Successfully validated account and redirected to Login page.")



if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        test_validate_email(page)
        browser.close()
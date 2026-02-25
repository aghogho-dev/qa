import os
import re
import time 
from imap_tools import MailBox, AND
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import pytz


load_dotenv()


def get_lastest_otp():
    """Get Latest OTP from Email"""
    # Set timezone and threshold to search the mail for otp
    wat_tz = pytz.timezone('Africa/Lagos')
    threshold = datetime.now(wat_tz) - timedelta(minutes=5)

    with MailBox(os.getenv("IMAP_SERVER")).login(
        os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD")) as mailbox:
        mailbox.folder.set("[Gmail]/All Mail")
        for msg in mailbox.fetch(AND(from_='support@lendsqr.com'), limit=1, reverse=True):
            if msg.date.astimezone(wat_tz) < threshold:
                continue

            match = re.search(r"provide.*?(\d{6}).*?as\s+your\s+OTP", msg.html, re.DOTALL | re.IGNORECASE)

            if match:
                return match.group(1)
    return False


def fetch_otp_with_retry(retries=30, delay=10):
    f"""Fetch OTP, delay for {delay} if it fails and retry"""
    
    print("Waiting for OTP email...")
    for i in range(retries):
        otp = get_lastest_otp()
        
        if otp:
            print(f"OTP Found: {otp}")
            return otp
        print(f"Attempt {i+1}: Email not found yet, retrying...")
        time.sleep(delay)
    return False
        

if __name__ == "__main__":
    fetch_otp_with_retry()
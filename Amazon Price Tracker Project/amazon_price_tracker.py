"""
Amazon Price Tracker (Educational / Portfolio Project)
-------------------------------------------------------
NOTE: This script is NOT runnable against live Amazon pages.
See README.md for a full explanation of why, and what this
project is meant to demonstrate instead.

Original goal: scrape a product's title and price from its
Amazon listing on a schedule, log each reading to a CSV, and
send an email alert when the price drops below a threshold.
"""

from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv
import smtplib

CSV_FILE = "AmazonWebScraperDataset.csv"
PRICE_THRESHOLD = 14  # send an alert if price drops below this

# Amazon requires a browser-like User-Agent or it rejects the request outright.
# Even with one, Amazon detects automated traffic patterns and serves a
# CAPTCHA / bot-check page instead of the real listing (see README).
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

URL = "https://www.amazon.com/dp/B07PB9XYH8"  # example product URL


def fetch_product_data(url: str, headers: dict) -> tuple[str, str]:
    """Fetch and parse a product's title and price from its Amazon page.

    Raises AttributeError if Amazon returns a bot-check / CAPTCHA page
    instead of the real listing, since expected elements won't exist.
    """
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").get_text().strip()
    price_text = soup.find(id="priceblock_ourprice").get_text().strip()
    price = price_text[1:]  # strip leading currency symbol, e.g. "$"

    return title, price


def log_to_csv(title: str, price: str, date: datetime.date, path: str = CSV_FILE) -> None:
    """Append a (title, price, date) row to the tracking CSV, creating it with
    a header row if it doesn't exist yet."""
    file_exists = False
    try:
        with open(path, "r", encoding="UTF8"):
            file_exists = True
    except FileNotFoundError:
        pass

    mode = "a" if file_exists else "w"
    with open(path, mode, newline="", encoding="UTF8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Title", "Price", "Date"])
        writer.writerow([title, price, date])


def send_price_alert(title: str, price: str) -> None:
    """Send an email notification when the price drops below the threshold.

    Credentials are read from environment variables — never hardcode
    email addresses or passwords in source code.
    """
    import os

    sender = os.environ.get("ALERT_EMAIL_SENDER")
    password = os.environ.get("ALERT_EMAIL_PASSWORD")
    recipient = os.environ.get("ALERT_EMAIL_RECIPIENT")

    if not all([sender, password, recipient]):
        print("Email credentials not configured; skipping alert.")
        return

    message = f"Subject: Price Drop Alert!\n\n{title} is now ${price}. Go get it!"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, message)


def check_price() -> None:
    """One full cycle: fetch, log, and alert if the price is low enough."""
    title, price = fetch_product_data(URL, HEADERS)
    today = datetime.date.today()

    log_to_csv(title, price, today)
    print(f"[{today}] {title} — ${price}")

    if float(price) < PRICE_THRESHOLD:
        send_price_alert(title, price)


if __name__ == "__main__":
    # Runs indefinitely, checking once every 24 hours.
    while True:
        check_price()
        time.sleep(86400)

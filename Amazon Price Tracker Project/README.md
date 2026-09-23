# Amazon Price Tracker (Portfolio Project)

A Python script that scrapes a product's title and price from an Amazon
listing, logs each reading to a CSV file, and sends an email alert when the
price drops below a set threshold. Built to practice web scraping,
data logging, and scheduled automation with `requests`, `BeautifulSoup`,
`csv`, and `smtplib`.

## ⚠️ Status: Not runnable against live Amazon pages

This project **cannot currently be executed against Amazon.com**, and that's
intentional documentation, not an oversight. Here's why:

- Amazon actively detects and blocks automated/non-browser traffic.
- Even with a spoofed `User-Agent` header, requests to Amazon product pages
  are served a CAPTCHA / bot-check page instead of the real listing —
  which is why parsing calls like `soup.find(id='productTitle')` return
  `None` and raise `AttributeError`.
- Amazon's [Terms of Service](https://www.amazon.com/gp/help/customer/display.html?nodeId=508088)
  prohibit scraping their site. Programmatic access is only available
  through the official **Product Advertising API**, which itself requires
  an approved Associates account with 3+ qualifying sales in the past 180
  days — not something available on request.

This repo exists to show the **scraping, parsing, logging, and alerting
logic** I built and understand, while being transparent that it's not a
tool meant to be run against Amazon in practice.

## What it does (by design)

1. Sends a GET request to a product URL with browser-like headers
2. Parses the returned HTML with BeautifulSoup to extract title and price
3. Cleans and formats the extracted values
4. Appends a timestamped row to `AmazonWebScraperDataset.csv`
5. Sends an email alert via `smtplib` if the price falls under a threshold
6. Repeats on a 24-hour loop using `time.sleep()`

## Tech stack

- Python 3
- `requests` — HTTP requests
- `beautifulsoup4` — HTML parsing
- `pandas` — reading back the logged CSV for analysis
- `smtplib` — email alerts (standard library)

## Setup (for reference only — see status note above)

```bash
pip install -r requirements.txt
```

Email alerts read credentials from environment variables rather than
hardcoded values:

```bash
export ALERT_EMAIL_SENDER="your_email@gmail.com"
export ALERT_EMAIL_PASSWORD="your_app_password"
export ALERT_EMAIL_RECIPIENT="recipient_email@gmail.com"
```

Never commit real credentials to the repo. Gmail also requires an
[app password](https://support.google.com/accounts/answer/185833) rather
than your account password for SMTP access.

## Known limitations / things I'd improve next

- Price comparison originally compared a raw string to an int (`price < 14`)
  — fixed here to cast to `float` first.
- CSV logging originally overwrote the file (`'w'` mode) on every run instead
  of appending — fixed here to append after the first write.
- No retry/backoff logic if a request fails.
- Selector IDs (`productTitle`, `priceblock_ourprice`) are hardcoded and
  would break if Amazon changes its markup, even without anti-bot blocking.

## Legitimate paths forward

If I wanted to actually run something like this:
- Point it at a site built for scraping practice, e.g.
  [books.toscrape.com](http://books.toscrape.com)
- Use Amazon's official **Product Advertising API** once eligible
- Use a paid, ToS-compliant product/price data API

## License

For educational/portfolio purposes.

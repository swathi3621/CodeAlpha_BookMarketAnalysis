"""
CodeAlpha Task 1 - Web Scraping
Project: Book Market Analysis

Scrapes the public Books to Scrape demo website.
This website is explicitly provided as a scraping practice site.
"""

import time
import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
OUTPUT = Path("data/books_scraped.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CodeAlphaStudentProject/1.0)"
}

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def get_soup(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_book(product_url):
    soup = get_soup(product_url)

    title = soup.find("h1").get_text(strip=True)

    price_tag = soup.select_one(".price_color")
    price_text = price_tag.get_text(strip=True) if price_tag else ""
    price = float(re.sub(r"[^0-9.]", "", price_text))

    availability_tag = soup.select_one(".availability")
    availability = availability_tag.get_text(" ", strip=True) if availability_tag else "Unknown"

    rating = None
    rating_tag = soup.select_one(".star-rating")
    if rating_tag:
        classes = rating_tag.get("class", [])
        for name, value in RATING_MAP.items():
            if name in classes:
                rating = value
                break

    category = "Unknown"
    breadcrumb = soup.select("ul.breadcrumb li a")
    if len(breadcrumb) >= 3:
        category = breadcrumb[2].get_text(strip=True)

    return {
        "title": title,
        "price_gbp": price,
        "availability": availability,
        "rating": rating,
        "category": category,
        "product_url": product_url
    }


def scrape_all_pages(max_pages=50):
    records = []
    next_url = BASE_URL
    page_no = 1

    while next_url and page_no <= max_pages:
        print(f"Scraping page {page_no}...")
        soup = get_soup(next_url)

        books = soup.select("article.product_pod h3 a")
        for book in books:
            href = book.get("href")
            product_url = requests.compat.urljoin(next_url, href)

            try:
                records.append(scrape_book(product_url))
                time.sleep(0.15)
            except Exception as error:
                print(f"Skipped: {product_url} -> {error}")

        next_link = soup.select_one("li.next a")
        if next_link:
            next_url = requests.compat.urljoin(next_url, next_link.get("href"))
            page_no += 1
        else:
            next_url = None

    return pd.DataFrame(records)


if __name__ == "__main__":
    df = scrape_all_pages(max_pages=50)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)

    print("\nScraping completed.")
    print(f"Rows collected: {len(df)}")
    print(f"Saved to: {OUTPUT}")
    print(df.head())

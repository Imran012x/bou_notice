# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import time

# Base URLs for the four sections
urls = {
    "Admissionmore": "https://www.bou.ac.bd/NoticeBoard/Admissionmore",
    "Exammore": "https://www.bou.ac.bd/NoticeBoard/Exammore",
    "Regimore": "https://www.bou.ac.bd/NoticeBoard/Regimore",
    "Resultmore": "https://www.bou.ac.bd/NoticeBoard/Resultmore"
}

# CSS Selectors for title and download link
title_selector = "td:nth-child(2) a"        # Selector for title link
download_selector = "td:nth-child(4) a"     # Selector for download link

# Function to scrape a single page and extract notices
def scrape_notices():
    notices_data = {}

    # Loop through each section and scrape the first three pages
    for section, base_url in urls.items():
        section_notices = []

        for page in range(1, 4):  # Pages 1 to 3
            page_url = f"{base_url}?page={page}"
            response = requests.get(page_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                rows = soup.select("section:nth-child(4) > div > div > table > tbody > tr")

                for row in rows:
                    notice = {}

                    # Get title and link
                    title_tag = row.select_one(title_selector)
                    if title_tag:
                        notice["title"] = title_tag.text.strip()
                    
                    download_link_tag = row.select_one(download_selector)
                    if download_link_tag:
                        download_link = download_link_tag.get("href")
                        if download_link and not download_link.startswith("http"):
                            download_link = "https://www.bou.ac.bd" + download_link
                        notice["download_link"] = download_link

                    if "title" in notice and "download_link" in notice:
                        section_notices.append(notice)
            
            time.sleep(1)  # Delay to prevent overloading the server

        notices_data[section] = section_notices

    return notices_data


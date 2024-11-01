import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json

def scrape_notices(section, page):
    url = f"https://www.bou.ac.bd/NoticeBoard/{section}?page={page}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to retrieve data."}

    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select("body > section:nth-child(4) table tbody tr")
    notices = []

    for row in rows:
        # Extract the actual serial number from the page
        serial = row.select_one("th, td:nth-child(1)")
        serial_text = serial.get_text(strip=True) if serial else "N/A"
        
        # Extract date and title
        date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
        title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
        
        # Use a different selector for the link in 'Exammore' section
        if section == 'Exammore':
            link = row.select_one("td:nth-child(4) > a")['href'] if row.select_one("td:nth-child(4) > a") else "N/A"
        else:
            link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"
        
        # Append the notice with the actual serial from the page
        notices.append(OrderedDict([
            ("acc", serial_text),
            ("date", date),
            ("title", title),
            ("link", link)
        ]))

    return notices

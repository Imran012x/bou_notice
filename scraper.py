import requests
from bs4 import BeautifulSoup
import json

def scrape_notices(section, page, start_serial=1):
    url = f"https://www.bou.ac.bd/NoticeBoard/{section}?page={page}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to retrieve data."}

    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select("body > section:nth-child(4) table tbody tr")
    notices = []

    for row in rows:
        serial = row.select_one("th, td:nth-child(1)")
        date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
        title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
        # Use a different selector for the link in 'Exammore' section
        if section == 'Exammore':
            link = row.select_one("td:nth-child(4) > a")['href'] if row.select_one("td:nth-child(4) > a") else "N/A"
        else:
            link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"
        
        notices.append([
            ("serial", serial),
            ("date", date),
            ("title", title),
            ("link", link)
        ])
    return notices

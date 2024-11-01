import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json

def scrape_notices(section, page):
    base_url = "https://www.bou.ac.bd/NoticeBoard/"
    section_urls = {
        'Admissionmore': f"{base_url}Admissionmore?page={page}",
        'Exammore': f"{base_url}Exammore?page={page}",
        'Regimore': f"{base_url}Regimore?page={page}",
        'Resultmore': f"{base_url}Resultmore?page={page}"
    }
    
    url = section_urls.get(section)
    if not url:
        return {"error": "Invalid section provided."}

    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to retrieve data."}

    soup = BeautifulSoup(response.content, 'html.parser')
    notices = []

    # Define row selection based on the section type
    if section in ['Admissionmore', 'Exammore']:
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
    elif section in ['Regimore', 'Resultmore']:
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")
    else:
        return {"error": "Invalid section provided."}

    # Scrape each row and build the notice dictionary
    for row in rows:
        serial = row.select_one("th, td:nth-child(1)")  # First column for serial number
        serial_number = serial.get_text(strip=True) if serial else "N/A"
        date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
        title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
        link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"
        
        # Append each notice with serial number as the first field
        notices.append(OrderedDict([
            ("serial", serial_number),
            ("date", date),
            ("title", title),
            ("link", link)
        ]))

    return notices


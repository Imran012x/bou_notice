import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json

def scrape_notices(section, page, start_serial=1):
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
    serial_number = start_serial  # Start from the provided serial number

    # Selectors for different sections
    if section == 'Admissionmore':
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
    elif section == 'Exammore':
        # Adjust selector specifically for 'Exammore' structure
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
    elif section in ['Regimore', 'Resultmore']:
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")
    else:
        return {"error": "Invalid section provided."}

    # Loop through each row to extract notice data
    for row in rows:
        # Extract the serial number if present; otherwise, increment manually
        serial = row.select_one("th, td:nth-child(1)")
        serial_number = serial.get_text(strip=True) if serial else str(serial_number)
        
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
        serial_number = int(serial_number) + 1  # Increment serial manually for next entry

    return notices

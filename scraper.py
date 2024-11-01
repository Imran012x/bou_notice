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

    # Common row selection for Admissionmore and Exammore
    rows_common = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
    rows_regi_result = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")

    if section in ['Admissionmore', 'Exammore']:
        for row in rows_common:
            date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
            title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
            link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"
            # Create OrderedDict with serial as the first key
            notices.append(OrderedDict([("serial", serial_number), ("date", date), ("title", title), ("link", link)]))
            serial_number += 1  # Increment the serial number

    elif section in ['Regimore', 'Resultmore']:
        for row in rows_regi_result:
            date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
            title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
            link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"
            # Create OrderedDict with serial as the first key
            notices.append(OrderedDict([("serial", serial_number), ("date", date), ("title", title), ("link", link)]))
            serial_number += 1  # Increment the serial number

    return notices

# Example of usage
# notices = scrape_notices('Admissionmore', 2, start_serial=5)  # Example call for the second page
# print(json.dumps(notices, indent=2))

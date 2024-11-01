import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json

# Initialize a global serial number tracker
serial_tracker = {}

def scrape_notices(section, page, start_serial=None):
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

    # Use a global tracker to retain the last serial across multiple calls to this function
    if section not in serial_tracker:
        serial_tracker[section] = start_serial if start_serial is not None else 1
    serial_number = serial_tracker[section]

    # Define row selection based on the section
    rows = []
    if section in ['Admissionmore', 'Exammore']:
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
    elif section in ['Regimore', 'Resultmore']:
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")

    # Scrape each row
    for row in rows:
        date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
        title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
        link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"
        # Create OrderedDict with serial as the first key to enforce JSON order
        notices.append(OrderedDict([("serial", serial_number), ("date", date), ("title", title), ("link", link)]))
        serial_number += 1  # Increment the serial number for the next notice

    # Update the serial tracker for the next page call
    serial_tracker[section] = serial_number

    return notices

# Example usage for two pages
# first_page_notices = scrape_notices('Admissionmore', 1)
# second_page_notices = scrape_notices('Admissionmore', 2)
# all_notices = first_page_notices + second_page_notices
# print(json.dumps(all_notices, indent=2))

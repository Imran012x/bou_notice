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

    if section == 'Admissionmore':
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
        for row in rows:
            date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
            title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
            link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"
            #notices.append({"serial": serial_number, "date": date, "title": title, "link": link})
            notices.append(OrderedDict([("serial", serial_number), ("date", date), ("title", title), ("link", link)]))
            serial_number += 1  # Increment the serial number

    elif section == 'Exammore':
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
        for row in rows:
            date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
            title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
            link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"
            notices.append(OrderedDict([("serial", serial_number), ("date", date), ("title", title), ("link", link)]))
            serial_number += 1  # Increment the serial number

    elif section == 'Regimore':
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")
        for row in rows:
            date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
            title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
            link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"
            notices.append(OrderedDict([("serial", serial_number), ("date", date), ("title", title), ("link", link)]))
            serial_number += 1  # Increment the serial number

    elif section == 'Resultmore':
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")
        for row in rows:
            date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
            title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
            link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"
            notices.append(OrderedDict([("serial", serial_number), ("date", date), ("title", title), ("link", link)]))
            serial_number += 1  # Increment the serial number

    #return notices
    return json.dumps(notices, indent=4)  # Use indent for pretty-printing

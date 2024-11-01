import requests
from bs4 import BeautifulSoup

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

    if section == 'Admissionmore':
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
        for row in rows:
            serial_number = row.select_one("td:nth-child(1)").get_text(strip=True)
            date = row.select_one("td:nth-child(3)").get_text(strip=True)
            title = row.select_one("td:nth-child(2)").get_text(strip=True)
            link = row.select_one("td:nth-child(4) a")['href']
            notices.append({"serial": serial_number, "date": date, "title": title, "link": link})

    elif section == 'Exammore':
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
        for row in rows:
            serial_number = row.select_one("td:nth-child(1)").get_text(strip=True)
            date = row.select_one("td:nth-child(3)").get_text(strip=True)
            title = row.select_one("td:nth-child(2)").get_text(strip=True)
            link = row.select_one("td:nth-child(4) a")['href']
            notices.append({"serial": serial_number, "date": date, "title": title, "link": link})

    elif section == 'Regimore':
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")
        for row in rows:
            serial_number = row.select_one("td:nth-child(1)").get_text(strip=True)
            date = row.select_one("td:nth-child(3)").get_text(strip=True)
            title = row.select_one("td:nth-child(2)").get_text(strip=True)
            link = row.select_one("td:nth-child(4) a")['href']
            notices.append({"serial": serial_number, "date": date, "title": title, "link": link})

    elif section == 'Resultmore':
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")
        for row in rows:
            serial_number = row.select_one("td:nth-child(1)").get_text(strip=True)
            date = row.select_one("td:nth-child(3)").get_text(strip=True)
            title = row.select_one("td:nth-child(2)").get_text(strip=True)
            link = row.select_one("td:nth-child(4) a")['href']
            notices.append({"serial": serial_number, "date": date, "title": title, "link": link})

    return notices

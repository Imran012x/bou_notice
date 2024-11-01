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
    serial_number = 1  # Initialize serial number counter

    # Select rows based on the section
    if section == 'Admissionmore':
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
    elif section == 'Exammore':
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
    elif section == 'Regimore' or section == 'Resultmore':
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")
    else:
        return {"error": "Invalid section specified"}

    # Loop through each row and extract data
    for row in rows:
        date = row.select_one("td:nth-child(3)").get_text(strip=True) if row.select_one("td:nth-child(3)") else "N/A"
        title = row.select_one("td:nth-child(2)").get_text(strip=True) if row.select_one("td:nth-child(2)") else "N/A"
        link = row.select_one("td:nth-child(4) a")['href'] if row.select_one("td:nth-child(4) a") else "N/A"

        notices.append({
            "serial": serial_number,
            "date": date,
            "title": title,
            "link": link
        })
        serial_number += 1  # Increment serial number

    return notices

# Example usage
if __name__ == "__main__":
    data = scrape_notices('Exammore', 1)
    print(data)

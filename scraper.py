import requests
from bs4 import BeautifulSoup

def scrape_notices(section, page):
    base_url = "https://www.bou.ac.bd/NoticeBoard/"
    
    # Map the section to the appropriate URL
    section_urls = {
        'Admissionmore': f"{base_url}Admissionmore?page={page}",
        'Exammore': f"{base_url}Exammore?page={page}",
        'Regimore': f"{base_url}Regimore?page={page}",
        'Resultmore': f"{base_url}Resultmore?page={page}"
    }
    
    # Fetch the page content
    url = section_urls.get(section)
    if not url:
        return {"error": "Invalid section provided."}

    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Failed to retrieve data."}

    soup = BeautifulSoup(response.content, 'html.parser')
    notices = []

    # Debugging: Print the HTML content to see what's fetched
    print(soup.prettify())  # This will help you see the actual content being scraped

    # Adjust selectors based on the section
    if section == 'Admissionmore':
        rows = soup.select("body > section:nth-child(4) > div > table > tbody > tr")
        for row in rows:
            title = row.select_one("td:nth-child(2)").get_text(strip=True)
            link = row.select_one("td:nth-child(4) a")['href']
            notices.append({"title": title, "link": link})

    elif section == 'Exammore':
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")
        for row in rows:
            title = row.select_one("td:nth-child(2)").get_text(strip=True)
            link = row.select_one("td:nth-child(4) a")['href']
            notices.append({"title": title, "link": link})

    elif section == 'Regimore':
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")
        for row in rows:
            title = row.select_one("td:nth-child(2)").get_text(strip=True)
            link = row.select_one("td:nth-child(4) a")['href']
            notices.append({"title": title, "link": link})

    elif section == 'Resultmore':
        rows = soup.select("body > section:nth-child(4) > div > div > table > tbody > tr")
        for row in rows:
            title = row.select_one("td:nth-child(2)").get_text(strip=True)
            link = row.select_one("td:nth-child(4) a")['href']
            notices.append({"title": title, "link": link})

    return notices

# Example usage
if __name__ == "__main__":
    # Change section and page as needed
    data = scrape_notices('Exammore', 1)
    print(data)

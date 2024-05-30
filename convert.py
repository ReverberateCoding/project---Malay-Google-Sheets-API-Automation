import requests
from bs4 import BeautifulSoup

def generate_text(word):
    url = f"https://prpm.dbp.gov.my/cari1?keyword={word}"

    response = requests.get(url=url)

    if response.status_code == 200:
        html_content = response.text
        
        soup = BeautifulSoup(html_content, 'html.parser')

        bold_tags = soup.find_all('b')
        definisis = []

        for tag in bold_tags:
            if str(tag.string)[0] == "D":
                definisis.append(tag)
        
        definisi = definisis[0]
        text = definisi.next_sibling
        text = str(text)
        text = text.split(";")

        added = 0
        answer = ""
        while added < len(text) and "~" not in answer:
            answer = answer + text[added]
            added += 1

        return answer
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
        return "NIL"
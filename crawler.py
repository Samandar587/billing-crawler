import requests
from bs4 import BeautifulSoup
import urllib.parse

url = "https://example.com"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

data = {
    "company_type": "Juridic",
    "company_name": "Company Name",
}

submit_url = "https://example.com/submit_form"
response = requests.post(submit_url, data=data)

pdf_link = soup.find("a", text="Download PDF")["href"]
# OR
pdf_link = urllib.parse.urljoin(url, pdf_link)

pdf_response = requests.get(pdf_link)
with open("cheque.pdf", "wb") as f:
    f.write(pdf_response.content)

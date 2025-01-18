#!/usr/bin/env python3

from requests_tor import RequestsTor
import os
import requests
from bs4 import BeautifulSoup
import argparse

parser.add_argument("-url", help="target onion url", required=True)
parser.add_argument("-dir", help="save the scraped content to your custom dir", required=False)
args = parser.parse_args()



url = args.arg1
if args.arg2:
	save_dir = args.arg2
else:
	save_dir = "scraped_pages"
	
os.makedirs(save_dir, exist_ok=True)
requests = RequestsTor(tor_ports=(9050,), tor_cport=9051)

response = requests.get(url)
print(f"Scraping {url}....")

soup = BeautifulSoup(response.content, "html.parser")
page_name = os.path.join(save_dir, "index.html")


with open(page_name, "w", encoding="utf-8") as f:
    f.write(str(soup))

for link in soup.find_all("a", href=True):
    link_url = link["href"]
    
    if link_url.startswith("http"):
        print(f"Recursive Scraping {link_url}....")
        link_response = requests.get(link_url)
        link_soup = BeautifulSoup(link_response.content, "html.parser")
        link_name = os.path.join(save_dir, link_url.split("/")[-1] + ".html")
        with open(link_name, "w", encoding="utf-8") as f:
            f.write(str(link_soup))

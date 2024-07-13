# homework 6 — BEAUTIFUL SOUP

import os, re, hashlib, json, requests
from bs4 import BeautifulSoup



def get_content(url):
	filename = hashlib.md5(url.encode('utf-8')).hexdigest()

	if os.path.exists(filename):
		with open(filename, 'r') as f:
			content = f.read()
		return content

	response = requests.get(
		url=url,
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
		}
	)
	return response.text



def make_soup():
	website = 'https://www.bbc.com/sport'
	content = get_content(website)
	soup = BeautifulSoup(content, 'lxml')

	data = []

	blocks = soup.find('ul', attrs={ "role": "list", "class": re.compile("-Grid") }).find_all('div', attrs={"class": re.compile("-UncontainedPromoWrapper")})
	
	for block in blocks:
		url   = block.find('a',    attrs={"class": re.compile("-PromoLink") }).get('href')
		topic = block.find('span', attrs={"class": re.compile("-MetadataText") })
		topic = topic.text.strip() if topic else ''
		data.append({ 
			"Link": "https://www.bbc.com"+url, 
			"Topics": topic
			} 
		)

	with open('sportnews.json', 'w', encoding='utf-8') as f:
		json.dump(data[:5], f, indent=4, ensure_ascii=False)



if __name__ == '__main__':
	make_soup()

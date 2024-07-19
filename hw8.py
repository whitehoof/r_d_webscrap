import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def parse_selenium():
	start_page = 1 # номер першої сторінки.
	grab_pages = 2 # скільки сторінок тягти.

	driver = webdriver.Chrome()
	result = []

	for page in range(start_page, start_page + grab_pages):
		driver.get(f'https://jobs.marksandspencer.com/job-search?page={ page }')
		wait = WebDriverWait(driver, 10)
		wait.until(EC.presence_of_element_located( (By.CLASS_NAME, 'c-btn__text') )) # the "Locator" argument a tuple!
		jobs = driver.find_elements(By.CLASS_NAME, 'ais-Hits-item')
		for job in jobs:
			title = job.find_element(By.TAG_NAME, 'h3').text
			link = job.find_element(By.CLASS_NAME, 'c-btn--primary').get_attribute('href')
			result.append({
				'title': title,
				'link': link
			})

	driver.quit()

	with open('jobs_selenium.json', 'w') as f:
		json.dump(result, f, indent=4)



if __name__ == '__main__':
	parse_selenium()

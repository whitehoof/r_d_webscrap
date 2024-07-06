import re
import requests
import time
import random
import html



def pause():
	pause_duration = random.uniform(1, 3) # тут буде float
	print(f'Pausing for {round(pause_duration,1)} seconds...\n')
	time.sleep(pause_duration)



def normalize_text(string):
	string = html.unescape(string) # unescape the string.
	string = ' '.join(string.split()) # trim whitespaces.
	return string




def use_post():
	jobs_list = [] # сюди складати вакансії.
	pattern_jobs = r'jobCard_title\">(.*?)<\/h3>'

	must_rewrite_jsonfile = True
	page = 1103
	count_pages = page + 1 # це мінімально задаю по дефолту, після першого запиту знатиму реальну кількість сторінок.


	while page <= count_pages:
		payload = {
			"action": "facetwp_refresh",
			"data": {
				"facets": {
					"recherche": [],
					"ou": [],
					"type_de_contrat": [],
					"fonction": [],
					"load_more": [page]
				},
				"frozen_facets": {
					"ou": "hard"
				},
				"http_params": {
					"get": [],
					"uri": "emplois",
					"url_vars": []
				},
				"template": "wp",
				"extras": {
					"counts": True,
					"sort": "default"
				},
				"soft_refresh": 1,
				"is_bfcache": 1,
				"first_load": 0,
				"paged": page
			}
		}
	
		my_headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
		response = requests.post('https://www.lejobadequat.com/emplois', json=payload, headers=my_headers)
		
		response.encoding = 'utf-8' # це, здається, не допомагає.
		
		if response.status_code==200:
			print('\nSTATUS CODE:', response.status_code, 'Все гаразд, тягнемо дані...')
		else:
			print('\nSTATUS CODE:', response.status_code, 'Нас розкрито, топи макбук, тікай в село!')
			break
		

		template_pretty = response.json()['template'] # витягую для парсингу значення ключа "template"
		

		# Рахую сторінки
		# та ставлю реальну кількість ітерацій для while loop:
		count_pages = response.json()['settings']['pager']['total_pages']
		print(count_pages, 'сторінок на сайті, тягнемо сторінку', page, '...')
		



		# # запис останньої відповіді у файл jobs.json:
		# with open('jobs.json', mode='w') as f: # перезапис останньої відповіді у файл.
		# 	f.write(f'PAGE {page}:\n\n')
		# 	f.write(response.text)
		
		
		jobs_match = re.findall(pattern_jobs, template_pretty)
		if len(jobs_match):
			jobs_match = [ normalize_text(j) for j in jobs_match ]
			jobs_list = jobs_list + jobs_match
		else:
			print('\n\n\n\n\n\t\tNO JOBS MATCHED!\n\n\n')

		pause()
		page += 1

		write_mode = 'w' if must_rewrite_jsonfile else 'a' # Для початку роблю порожній jobs.txt
		with open('jobs.txt', mode=write_mode) as fj:
			fj.write('\n'.join(jobs_list) + '\n')

		must_rewrite_jsonfile = False # а потім дописую в кінець наступні сторінки.
	return jobs_list



if __name__ == '__main__':
	print(use_post())

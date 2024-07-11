# НАЛАШТУВАННЯ СКРИПТА:

website = 'https://www.lejobadequat.com/emplois'
pattern_jobs = r'jobCard_title\">(.*?)<\/h3>'
pattern_urls = r'href=\"(https:\/\/.*?)\".*?class=\"jobCard_link'
my_headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}



# ДОПОМІЖНІ ФУНКЦІЇ:

def normalize_text(dirty_text):
	"""
	Unescapes the string (example: converts unreadable bullshit into accented Unicode letters (è, â, ç...), endash, emdash (–, —), fancy symbols (&, ©, ®, ∑) etc.) and then trims the excessive whitespaces.

	Args:
		dirty_text (str): Text to be normalized.

	Returns:
        str: The normalized and trimmed string.
	"""
	import html

	dirty_text = html.unescape(dirty_text) # unescape the dirty_text.
	return ' '.join(dirty_text.split()) # trim whitespaces and return a nice string.


def write_json(list_of_dicts):
	"""
	Writes the data in the list of dictionaries into a JSON file in the same folder as the running script.

	Args:
		list_of_dicts (list): a list of dictionaries that contains the jobs data and the unique IDs.
	"""
	import json
	with open('jobs.json', mode='w') as fj:
		json.dump(list_of_dicts, fj, indent=4)


def write_sql(list_of_dicts):
	"""
	Writes the data in the list of dictionaries into a SQLITE3 database file in the same folder as the running script.

	Args:
		list_of_dicts (list): a list of dictionaries that contains the jobs data and the unique IDs.
	"""
	import sqlite3

	filename = 'jobs.db'

	conn = sqlite3.connect(filename)
	c = conn.cursor()
	c.execute("drop table if exists jobs") # якшо вже є така БД, обнуляю її.
	c.execute("""
		create table jobs (
			id integer primary key,
			job_name text not null,
			job_url text not null
		)
		""")
	for job in list_of_dicts:
		c.execute("""
			insert into jobs (id, job_name, job_url) values (?,?,?)
		""", (job['id'], job['job_name'], job['job_url']))
	
	conn.commit()
	conn.close()



def read_sqlite():
	"""
	This can be used to read the sqlite db file. 
	No args, no vars, just run it and read the console.
	"""
	import sqlite3
	filename = 'jobs.db'

	conn = sqlite3.connect(filename)
	cursor = conn.cursor()
	sql = """
		select id, job_name, job_url
		from jobs
	"""
	rows = cursor.execute(sql).fetchall()
	for r in rows:
		print(r)
	conn.close()



# ГОЛОВНА ФУНКЦІЯ:

def get_jobs():
	"""
	Стягує зі вказаного вебсайту перші (12 штук або скільки умовна "перша сторінка" видасть) назви вакансій та лінки на них, складає ці дані у файл JSON та у базу даних SQLite.
	"""
	import re, requests
	
	payload = {
		"action": "facetwp_refresh",
		"data": {
			"facets": {
				"recherche": [],
				"ou": [],
				"type_de_contrat": [],
				"fonction": [],
				"load_more": [1]
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
			"paged": 1
		}
	}

	response = requests.post(website, json=payload, headers=my_headers)
	response.encoding = 'utf-8'
	
	if response.status_code != 200:
		raise ValueError(f"Server returned status code {response.status_code}. No vacancies for you!")
	else:
		template_pretty = response.json()['template'] # витягую для парсингу значення ключа "template" з відповіді сервера.
				
		urls_match = re.findall(pattern_urls, template_pretty)
		jobs_match = re.findall(pattern_jobs, template_pretty)

		if len(jobs_match) == 0:
			raise ValueError('No jobs found!')
		else:
			jobs_match = [ normalize_text(j) for j in jobs_match ] # тепер jobs_match має нормальні unicode букви.
			
			# Складую все докупи into the list of  dictionaries:
			jobs = []
			for i, (name, url) in enumerate(zip(jobs_match, urls_match)):
				job_dict = {"id": i + 1, "job_name": name, "job_url": url}
				jobs.append(job_dict)
			
			# пишу файли JSON та SQLITE:
			write_json(jobs)
			write_sql(jobs)
	
	# Here ends get_jobs() function.



# Викликаю головну функцію:

if __name__ == '__main__':
	get_jobs()

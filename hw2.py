import re
from lxml import etree
import requests



# ПАТТЕРНИ ДЛЯ МЕТЧИНГУ:

regex_emails = r'[\w\.\+_-]+\w@\w[\w\.\+-]+\w'
regex_dates =  r'(?:\b0?[1-9]|1[0-2])[-/\.](?:0?[1-9]|[12]\d|3[01])[-/\.](?:19\d\d|2[01]\d\d)\b|(?:\b0?[1-9]|[12]\d|3[01])[-/\.](?:0?[1-9]|1[0-2])[-/\.](?:19\d\d|2[01]\d\d)\b|(?:\b19\d\d|2[01]\d\d)[-/\.](?:0?[1-9]|1[0-2])[-/\.](?:0?[1-9]|[12]\d|3[01])\b|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December)\s(?:0?[1-9]|[12]\d|3[01]),\s?(?:19\d\d|2[01]\d\d)'
xpath1 = '//*[@id="text-input-what"]' # Input для введення пошукового запиту
xpath2 = '//*[@id="text-input-where"]' # Input для введення регіону
xpath3 = '//*/button[@type="submit"]' # Кнопка пошуку

xpath4 = '//*/button' # Будь-яка кнопка. Це перевірка, чи взагалі працює мій xpath-парсер.



# ДАНО:

url = "https://br.indeed.com/"

text = """Welcome to the Regex Training Center! Let's start with some dates:
01/11/2021, 12-25-2020, 2021.03.15, 2022/04/30, 2023.06.20, and 2021.07.04. Or even 13/3/2000 and 12/31/1900 You can
also find dates with words: March 14, 2022, Jul 1, 2024and December 25, 2020. 

WARNING:
А ЩЕ МИ ПЕРЕВІРИМО НЕКОРЕКТНІ ДАТИ, ТАКІ ЯК-ОТ: 2024-05-35 (не буває 35 травня), 2024-15-10 (не буває 15-го місяця)

Now let's move on to some phone numbers:
(123) 456-7890, +1-800-555-1234, 800.555.1234, 800-555-1234, and 123.456.7890. 
Other formats include international numbers: +44 20 7946 0958, +91 98765 43210.
 jun june June July Jul
Here are some email addresses to find:
john.doe@example.com, jane_doe123@domain.org, support@service.net, info@company.co.uk, 
and contact.us@my-website.com. You might also find these tricky: weird.address+spam@gmail.com,
"quotes.included@funny.domain", and this.one.with.periods@weird.co.in.

Need some URLs to extract? Try these:
http://example.com, https://secure.website.org, http://sub.domain.co, 
www.redirect.com, and ftp://ftp.downloads.com. Don't forget paths and parameters:
https://my.site.com/path/to/resource?param1=value1&param2=value2, 
http://www.files.net/files.zip, https://example.co.in/api/v1/resource, and 
https://another-site.org/downloads?query=search#anchor. 

Hexadecimal numbers appear in various contexts:
0x1A3F, 0xBEEF, 0xDEADBEEF, 0x123456789ABCDEF, 0xA1B2C3, and 0x0. You might also find these: 
#FF5733, #C70039, #900C3F, #581845, #DAF7A6, and #FFC300. RGB color codes can be tricky: 
rgb(255, 99, 71), rgba(255, 99, 71, 0.5).

For those interested in Social Security numbers, here's some data:
123-45-6789, 987-65-4321, 111-22-3333, 555-66-7777, and 999-88-7777. Note that Social 
Security numbers might also be written like 123 45 6789 or 123456789.

Let's throw in some random sentences for good measure:
- The quick brown fox jumps over the lazy dog.
- Lorem ipsum dolor sit amet, consectetur adipiscing elit.
- Jack and Jill went up the hill to fetch a pail of water.
- She sells seashells by the seashore.

Finally, let's include some special characters and numbers:
1234567890, !@#$%^&*()_+-=[]{}|;':",./<>?, 3.14159, 42, and -273.15.

That's it! I hope you find this useful for your regex training.


"""



# ФУНКЦІЇ:

def parse_re(pattern):
	result = re.findall(pattern, text)
	for x in result:
		print(x)


def parse_html_xpath(url, xpath):
	response = requests.get(url)

	tree = etree.HTML(response.content)
	element = tree.xpath(xpath)
	
	if not element:
		print(f"No elements found for pattern \"{xpath}\".")
		return

	inner_html = etree.tostring(element[0], method='html', encoding='utf-8').decode('utf-8')
	print(inner_html)



# ВИКОНАННЯ ФУНКЦІЙ:

print('\n\n\n    EMAILS    \n')
parse_re(regex_emails)

print('\n\n\n    DATES    \n')
parse_re(regex_dates)


print('\n\n\n    XPATH    \n')
parse_html_xpath(url, xpath1)
parse_html_xpath(url, xpath2)
parse_html_xpath(url, xpath3)

print('\n\n\n    ПЕРЕВІРКА, ЧИ ПРАЦЮЄ XPATH ФУНКЦІЯ    \n')
parse_html_xpath(url, xpath4)



print('\n\n\n    ОТЖЕ,    \n    шось не виходить з xpath знайти потрібні елементи.    \n\n\n')
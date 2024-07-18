import scrapy


class QuotezSpider(scrapy.Spider):
    name = "quotez"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    max_count_follow = 1

    custom_settings = {
         'DOWNLOAD_DELAY' : 1
    }

    def parse(self, response):
        rows = response.xpath('//div[@class="quote"]')
        
        for row in rows:
            print("\n\n\nrow ЩЕ:\n\n")
            print(row)
            text   = row.xpath('.//span[@class="text"]/text()').get() # крапка!!!!!
            author = row.xpath('.//small[@class="author"]/text()').get()

            yield {
                'text': text,
                'author': author
            }
        
        next_btn = response.xpath('//li[@class="next"]/a/@href').get()
        
        if next_btn and self.max_count_follow:
            self.max_count_follow -= 1
            yield response.follow(next_btn, callback=self.parse)

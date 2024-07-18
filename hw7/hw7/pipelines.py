# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class Hw7Pipeline:
    def process_item(self, item, spider):
        return item



class SqLitePipeline:
    def open_spider(self, spider):
        print('\n\n\nGALEMBA open_spider\n\n\n')
        self.connection = sqlite3.connect('crypto.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
                create table if not exists crypto (
                    name text,
                    price text
                )
            """
        )
        self.connection.commit()


    def close_spider(self, spider):
        print('\n\n\nGALEMBA close_spider\n\n\n')
        self.connection.close()


    def process_item(self, item, spider):
        print('\n\n\nGALEMBA process_item\n\n\n')
        self.cursor.execute(
            """
                insert into crypto (name, price) values (?, ?), 
            """, (item['name'], item['price'])
        )
        self.connection.commit()
        return item
    
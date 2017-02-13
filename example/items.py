# coding:utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
#from scrapy.loader import ItemLoader
#from scrapy.loader.processors import MapCompose, TakeFirst, Join

class youyuanItem(Item):
    # 个人照片地址
    header_url = Field()
    # 用户名：
    username = Field()
    # 内心独白：
    requer  = Field()
    # 个人相册所有照片url：
    pic_url = Field()
    # 年龄：
    age = Field()
    # 源自 youyuan
    source = Field()
    # response的url地址
    source_url = Field()
    # utc标准时间
    crawled = Field()
    # 爬虫名
    spider = Field()


'''
class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
   url = Field()


class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
'''

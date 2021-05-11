# 亚马逊项目使用的item，包括书籍以及评论item

import scrapy

class BookItem(scrapy.Item):
    name = scrapy.Field()
    paperback_price = scrapy.Field()
    kindle_price = scrapy.Field()
    img = scrapy.Field()
    quantity_review = scrapy.Field()
    details_url = scrapy.Field()

class ReviewItem(scrapy.Item):
    book_name = scrapy.Field()
    reviewer = scrapy.Field()
    star = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

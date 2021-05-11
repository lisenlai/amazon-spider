#根据爬取当月销量最高的书籍以及根据书籍名爬取书籍

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.http.response.html import HtmlResponse
import re
from amazonSpider.items import BookItem
from amazonSpider.items import ReviewItem


class BookSpider(CrawlSpider):
    name = 'book'
    rule1 = LinkExtractor(restrict_xpaths="//li[@class='a-normal']")
    rule2 = LinkExtractor(restrict_xpaths="//div[@class='sg-row']//h2/a[contains(@class,'a-link-normal') and contains(@class, 'a-text-normal')]")
    rule3 = LinkExtractor(restrict_xpaths='//a[@data-hook="see-all-reviews-link-foot"]')
    rule4 = LinkExtractor(restrict_xpaths='//li[@class="a-last"]/a')
    rules = (
        Rule(rule1, callback='parse_item', follow=True),
        Rule(rule2, callback='parse_book', follow=True),
        Rule(rule3, callback='parse_reviews', follow=True),
        Rule(rule4, callback='parse_reviews', follow=True)
    )

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        choose_num = input("输入数字选择：1爬取当月销量最高的书籍，2爬取查询书籍名\n")
        if (choose_num == '1'):
            self.start_urls = ['https://www.amazon.com/s?i=specialty-aps&rh=n%3A17143709011&fs=true&qid=1620530268&ref=sr_pg_1']
        else:
            book_name = input("输入书籍名：")
            self.start_urls = ["https://www.amazon.com/s?k="+ book_name +"&i=stripbooks-intl-ship&ref=nb_sb_noss"]
        self._compile_rules()

    def parse_item(self, response):
        pass

    def parse_reviews(self,response):
        #爬取书籍的评论，包括每个评论给出的星级，用户名，标题，评论内容及书籍名称，
        #记得属性前加@
        reviews = response.xpath("//div[@data-hook='review']")
        book_name = response.xpath("//a[@data-hook='product-link']/text()").extract_first()
        for review in reviews:
            reviewItem = ReviewItem()
            reviewItem["star"]= review.xpath(".//span[@class='a-icon-alt']/text()").extract_first()[0]
            reviewItem["reviewer"] = review.xpath(".//span[@class='a-profile-name']/text()").extract_first()
            reviewItem["title"] = review.xpath(".//a[@data-hook='review-title']/span/text()").extract_first()
            reviewItem["content"] = review.xpath(".//span[@data-hook='review-body']/span/text()").extract_first()
            reviewItem["book_name"] = book_name
            yield reviewItem

    def parse_book(self, response):
        #爬取每本书的书名，封面地址，评论数量，商品具体网址，以及kindle和平装的价格
        book_Item = BookItem()
        book_Item["name"] = response.xpath("//span[@id='productTitle']/text()").extract_first().replace("\n","")
        book_Item["img"] = response.xpath("//div[@id='img-canvas']/img/@src").extract_first()
        q_review = response.xpath("//span[@id='acrCustomerReviewText']/text()").extract_first()
        book_Item["quantity_review"] = int("".join(list(filter(str.isdigit,q_review))))
        book_Item["details_url"] = response.url
        price_div = response.xpath("//div[@id='formats']")
        kindle_price_str =  price_div.xpath("//span[contains(text(),'Kindle')]/following-sibling::span/span/text()").extract_first()
        if(kindle_price_str):
            book_Item["kindle_price"] = re.findall(r"\d+\.?\d*",kindle_price_str)[0]
        else:
            book_Item["kindle_price"] = 0
        paperback_price_str = price_div.xpath("//span[contains(text(),'Paperback') or contains(text(),'平装')]/following-sibling::span/span/text()").extract_first()
        if (paperback_price_str):
            book_Item["paperback_price"] = re.findall(r"\d+\.?\d*",paperback_price_str)[0]
        else:
            book_Item["paperback_price"] = 0
        yield book_Item

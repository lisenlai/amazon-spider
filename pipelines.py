# item处理管道，将书籍item和评论item里的值存到mysql数据库
from itemadapter import ItemAdapter
import pymysql
from amazonSpider.items import BookItem
from amazonSpider.items import ReviewItem
import redis
from pymysql.converters import escape_string

class MysqlPipeline():
    conn = None
    cursor = None
   
    def open_spider(self, spider):
        #打开管道，连接到mysql数据库，如果没有book和review数据表，就创建
        user = "root"
        password = "qwer4371273"
        database = "amazon"
        port = 3306
        self.conn = pymysql.Connect(host='127.0.0.1', port = port, user = user, password = password, db=database,charset='utf8')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("""create table if not exists `book`(
                name char(255),
                paperback_price float, 
                kindle_price float,
                img char(255),
                quantity_review int,
                details_url char(255))
            """)
            self.cursor.execute("""create table if not exists `review`(
                book_name char(255),
                reviewer char(255),
                title text,
                star tinyint,
                content mediumtext)
                 """)
        except Exception as e:
            self.conn.rollback()

    def process_item(self, item, spider):
        #判断item类别，然后根据类别将item值存到不同数据表中
        if isinstance(item, BookItem):
            sql = """
                    insert into `book` (name, img, quantity_review, details_url,kindle_price, paperback_price)
                    values(%s, %s, %s, %s, %s, %s)
                    """   
            self.cursor.execute(sql,(item['name'],item['img'],item['quantity_review'],item['details_url'],item['kindle_price'],item['paperback_price']))
            
        elif isinstance(item, ReviewItem):
                sql = """
                        insert into `review` (book_name, reviewer, star, title, content)
                        values(%s, %s, %s, %s, %s)
                      """
                self.cursor.execute(sql, (item['book_name'],item['reviewer'],item['star'],item['title'],item['content']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        #关闭数据库的连接
        self.cursor.close()
        self.conn.close()
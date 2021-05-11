## amazon-spider

使用 scrapy爬取亚马逊当月销量最高的书籍，以及根据书籍名爬取书籍。

## 开发环境

- Python: `3.6.6`
- Scrapy: `2.5.0`
- Mysql: `8.0.24`


## 注意事项

- 使用`pip install -r requirements.txt`安装项目所有依赖包
- 根据你的谷歌浏览器版本从<http://chromedriver.storage.googleapis.com/index.html>下载安装浏览器驱动
- Windows用户安装Scrapy可能出错，你可以根据以下步骤安装Scrapy：
    - `pip install wheel`
    - 下载twisted: 从<https://www.lfd.uci.edu/~gohlke/pythonlibs/>找到对应的wheel文件下载
    - cd到下载文件所在目录,使用`pip install 文件名`安装twisted
    - `pip install pywin32`
    - `pip install scrapy`
- 构建ip池所使用的ip来自<https://www.engeniusiot.com/pricing>，无论使用哪家网站的套餐，记得在middlewares.py里seleniumDownloadMiddleware类的update_proxys函数中修改参数
- 数据库使用的是mysql，为了在你的电脑成功连接到数据库，请修改pipelines.py里MysqlPipeline类的open_spider函数里相关参数
- 在项目目录下，使用`scrapy crawl book`运行爬虫
BOT_NAME = 'amazonSpider'

SPIDER_MODULES = ['amazonSpider.spiders']
NEWSPIDER_MODULE = 'amazonSpider.spiders'

ROBOTSTXT_OBEY = False
LOG_LEVEL = "ERROR"

DOWNLOADER_MIDDLEWARES = {
    'amazonSpider.middlewares.seleniumDownloadMiddleware': 543,
}

ITEM_PIPELINES = {
    'amazonSpider.pipelines.MysqlPipeline': 300,
}

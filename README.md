# Scraping with scrapy-playwright

How it was created
 - Set HTTP_PROXY and HTTPS_PROXY before opening VS Code
 - create devcontainer.env file with server username password variables for proxy setting for scrapy-playwright
 - Prepared devcontainer.json, Dockerfile, .gitignore
 - Create folder downloaded in /workspaces/macro_scrapy/
 - run
``` shell
 scrapy startproject macro_scrapy
 cd macro_scrapy
```
 - Change in settings.py
``` shell
 ROBOTSTXT_OBEY = False
 ITEM_PIPELINES = {
    "macro_scrapy.pipelines.MacroScrapyPipeline": 1,
 }
 FILES_STORE = r"/workspaces/macro_scrapy/downloaded"
 DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
 }
 DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
PLAYWRIGHT_LAUNCH_OPTIONS = {
        "headless": True,
}
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "proxy": {
        "server": os.environ.get("SERVER"),
        "username": os.environ.get("USERNAME"),
        "password": os.environ.get("PASSWORD"),
        },
    } 
```
 - Change in items.py
``` shell
 class MacroScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    file_urls = scrapy.Field()
    original_file_name = scrapy.Field()  
    files = scrapy.Field
 
 class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
```
 - Change in pipelines.py
``` shell
 class MacroScrapyPipeline(FilesPipeline):
	def file_path(self, request, item=None,response=None, info=None): 
		file_name: str = datetime.today().strftime('%Y%m%d')+"_"+item['original_file_name'][0]+"_"+request.url.split("/")[-1] 
		return file_name 
```
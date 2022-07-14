from scrapy.crawler import CrawlerProcess
from datetime import datetime
import pandas as pd
import logging
import os
import sys

from utilities import load_config, combine_csv
from news_scrape.scrape import BBCNewsSpider, ReutersNewsSpider, APNewsSpider

config = load_config()

log_name = os.path.join(sys.path[0], "logs", f'{datetime.today().strftime("%d%b%Y")}.log')
logging.basicConfig(
    filename=log_name,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
)

spider_dict = {
    "bbc": BBCNewsSpider,
    "ap": APNewsSpider,
    "reuters": ReutersNewsSpider,
}

# run crawler process
logging.info("=========== BEGINNING SCRAPE ===========")
process = CrawlerProcess()
for spider in config["run_spiders"]:
    process.crawl(
        spider_dict[spider],
        file_path=os.path.join(
            sys.path[0], "raw_scrapes", f'{spider}_raw_{datetime.today().strftime("%d%b%Y")}.csv'
        ),
        urls=config["site_urls"][spider],
    )
process.start(stop_after_crawl=True)
logging.info("=========== SCRAPE COMPLETE ===========")

logging.info("Combining csv files ...")
combine_csv("raw_scrapes", "raw_scrapes/raw_news.csv")
logging.info('Raw csv files combined into "raw_news.csv"')

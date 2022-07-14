import scrapy
import csv
import re


class APNewsSpider(scrapy.Spider):
    name = "ap_news"
    # specify different sections to get the list of articles
    urls = ["https://apnews.com/hub/business"]

    def __init__(self, file_path):
        self.file_path = file_path

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_section)

    def parse_section(self, response):
        """This function parses a news section page to identify links to news articles themselves, belonging to this particular news section.
        e.g. A business section page will be parsed for articles that presumably are business related.
        This does not guarantee that the articles are related to the section specified.

        Parameters
        ----------
        response : [scrapy.response]
            [A response returned by the urls given above]

        Yields
        -------
        [scrapy.response]
            [A response for a single url followed on this page]
        """
        section_urls = response.xpath("//a/@href").extract()
        # filter to urls which are valid articles
        section_urls = [
            url for url in section_urls if re.search("article/(\w+-)+(\w*\d*){15,}", url)
        ]
        for url in section_urls:
            yield response.follow(url=url, callback=self.parse_page)

    def parse_page(self, response):
        """This function parses a specific news article page for the article text

        Parameters
        ----------
        response : [None]
            [Returns None. Instead writes article to csv file path that the spider was initialized with.
            Article text is appended to existing csv file.]
        """
        article_url = response.url
        headline = " ".join(response.xpath("//h1[1]/text()").extract())
        article_text = " ".join(
            response.xpath('//div[contains(@class, "Article")]//p//text()').extract()
        )

        # only write successful article scrapes
        if len(headline) > 0 and len(article_text) > 0:
            # write raw scraped data into output file
            with open(self.file_path, "a", newline="\n", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([headline + " " + article_text, article_url])
        else:
            self.logger.info(f"Insufficient text scraped from {response.url}")


class BBCNewsSpider(scrapy.Spider):
    name = "bbc_news"
    urls = [
        "https://www.bbc.com/news/business",
        "https://www.bbc.com/news/world",
    ]

    def __init__(self, file_path):
        self.file_path = file_path

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_section)

    def parse_section(self, response):
        section_urls = response.xpath("//a/@href").extract()
        # filter to urls which are valid articles
        section_urls = [url for url in section_urls if re.search("(\w+-)+\d+", url)]
        for url in section_urls:
            yield response.follow(url=url, callback=self.parse_page)

    def parse_page(self, response):
        article_url = response.url
        headline = " ".join(response.xpath('//h1[@id="main-heading"]/text()').extract())
        article_text = " ".join(
            response.xpath('//article[1]//div[@data-component="text-block"]//p//text()').extract()
        )

        # only write successful article scrapes
        if len(headline) > 0 and len(article_text) > 0:
            # write raw scraped data into output file
            with open(self.file_path, "a", newline="\n", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([headline + " " + article_text, article_url])


class ReutersNewsSpider(scrapy.Spider):
    name = "reuters_news"
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }
    # specify different sections to get the list of articles
    urls = [
        "https://www.reuters.com/world/africa/",
        "https://www.reuters.com/world/americas/",
        "https://www.reuters.com/world/asia-pacific/",
        "https://www.reuters.com/world/china/",
        "https://www.reuters.com/world/europe/",
        "https://www.reuters.com/world/india/",
        "https://www.reuters.com/world/middle-east/",
        "https://www.reuters.com/world/uk/",
        "https://www.reuters.com/world/us/",
        "https://www.reuters.com/world/reuters-next/",
        "https://www.reuters.com/legal/",
        "https://www.reuters.com/business/finance/",
        "https://www.reuters.com/business/aerospace-defense/",
        "https://www.reuters.com/business/energy/",
        "https://www.reuters.com/business/environmentv/",
        "https://www.reuters.com/business/healthcare-pharmaceuticals/",
        "https://www.reuters.com/business/aerospace-defense/",
        "https://www.reuters.com/business/media-telecom/",
        "https://www.reuters.com/business/retail-consumer/",
        "https://www.reuters.com/business/sustainable-business/",
    ]

    def __init__(self, file_path):
        self.file_path = file_path

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_section)

    def parse_section(self, response):
        section_urls = response.xpath("//a/@href").extract()
        # filter to urls which are valid articles
        section_urls = [url for url in section_urls if re.search("(\w+-)+\d{4}-\d{2}-\d{2}", url)]
        for url in section_urls:
            yield response.follow(url=url, callback=self.parse_page)

    def parse_page(self, response):
        article_url = response.url
        headline = " ".join(response.xpath("//h1[1]/text()").extract())
        article_text = " ".join(
            response.xpath('//div[contains(@class, "ArticleBody__content")]//p//text()').extract()
        )

        # only write successful article scrapes
        if len(headline) > 0 and len(article_text) > 0:
            # write raw scraped data into output file
            with open(self.file_path, "a", newline="\n", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([headline + " " + article_text, article_url])
        else:
            self.logger.info(f"Insufficient text scraped from {response.url}")


class GenericNewsSpider(scrapy.Spider):
    name = "other_news"

    def __init__(self, file_path, urls):
        self.file_path = file_path
        self.urls = urls

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        article_url = response.url
        headline = " ".join(
            response.xpath("//h1[1]/text()").extract()
        )  # must be modified to suit DOM of your desired site
        article_text = " ".join(
            response.xpath("//article//p//text()").extract()
        )  # must be modified to suit DOM of your desired site

        # only write successful article scrapes
        if len(headline) > 0 and len(article_text) > 0:
            # write raw scraped data into output file
            with open(self.file_path, "a", newline="\n", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([headline + " " + article_text, article_url])
        else:
            self.logger.info(f"Insufficient text scraped from {response.url}")

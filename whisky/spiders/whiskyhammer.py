# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy import Spider, Request
from whisky.items import Whisky


class WhiskyhammerSpider(Spider):
    name = 'whiskyhammer_spider'
    allowed_domains = ['whiskyhammer.co.uk']

    def parse_products(self, response):
        products = response.css('.itemImageWrap > a::attr(href)').getall()
        for p in products:
            yield Request(p, self.parse_product_detail, meta=response.meta.copy())

        next_page = response.css('.next > a::attr(href)').get()
        if next_page:
            yield Request(response.urljoin(next_page), self.parse_products, meta=response.meta.copy())

    def parse_product_detail(self, response):
        whisky = Whisky()
        whisky['source'] = 'whiskyhammer'
        whisky['source_url'] = 'https://www.whiskyhammer.co.uk'
        whisky['start_date'] = response.meta.get('date')
        whisky['distilleries'] = response.css('.distilleryLogo > img::attr(atr)').get()
        whisky['images'] = [response.urljoin(img) for img in response.css('[data-zoom-gallery=itemImage] > li > a::attr(href)').getall()]
        lot_info = response.css('.properties > ul > li')
        whisky['country'] = lot_info[0].css('::text').getall()[-1]
        whisky['region'] = lot_info[1].css('::text').getall()[-1]
        whisky['distillery_status'] = lot_info[2].css('::text').getall()[-1]
        whisky['age'] = lot_info[4].css('::text').getall()[-1]
        whisky['lot_num'] = response.css('#itemDescription .lotNo::text').get().split('#')[-1]
        whisky['current_bid'] = response.css('microdata-price::text').getall()
        desc = response.css('.priceDesc')
        if len(desc) > 1:
            whisky['sold_on'] = desc[1].css('::text').get().replace('Sold', '')
            whisky['winning_bid'] = whisky['current_bid']
        else:
            whisky['reserve'] = desc[0].css('::text').get()
        yield whisky


class WhiskyhammerPastSpider(WhiskyhammerSpider):
    name = 'whiskyhammer_pastauction_spiders'
    start_urls = ['https://www.whiskyhammer.co.uk/previous-auctions']

    def parse(self, response):
        auctions = response.css('.itemImageWrap > a').getall()
        for auc in auctions:
            href = auc.css('::attr(href)').get()
            date = auc.css('::attr(title)')
            yield Request(auc, self.parse_products, meta={'date':date})

        next_page = response.css('.next > a::attr(href)').get()
        if next_page:
            yield Request(response.urljoin(next_page), self.parse)


class WhiskyhammerCurrentSpider(WhiskyhammerSpider):
    name = 'whiskyhammer_currentauction_spider'
    start_urls = ['https://whiskyhammer.co.uk/auction/current']

    def start_requests(self):
        yield Request(self.start_urls[0], self.parse_products, meta={'date':datetime.now().date()})

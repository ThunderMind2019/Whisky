# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy import Spider, Request
from whisky.items import Whisky


class WhiskyhammerSpider(Spider):
    name = 'whiskyhammer_spider'
    allowed_domains = ['whiskyhammer.co.uk']

    def parse_products(self, response):
        end_date = ''
        if '/auction/current' in response.url:
            end_date = response.css('.endDateWrap .title::text').get()

        meta = response.meta.copy()
        meta['end_date'] = end_date
        products = response.css('.itemImageWrap > a::attr(href)').getall()
        for p in products:
            yield Request(p, self.parse_product_detail, meta=meta)

        next_page = response.css('.next > a::attr(href)').get()
        if next_page:
            yield Request(response.urljoin(next_page), self.parse_products, meta=meta)

    def parse_product_detail(self, response):
        whisky = Whisky()
        whisky['source'] = 'whiskyhammer'
        whisky['source_url'] = 'https://www.whiskyhammer.co.uk'
        whisky['start_date'] = response.meta.get('date')
        whisky['end_date'] = response.meta.get('end_date')
        whisky['distilleries'] = response.css('.distilleryLogo > img::attr(alt)').get()
        whisky['images'] = [response.urljoin(img) for img in response.css('[data-zoom-gallery=itemImage] > li > a::attr(href)').getall()]
        lot_info = response.css('.properties > ul > li')

        for info in lot_info:
            info = info.css('::text').getall()
            key = info[0].strip()
            value = info[1].strip()
            if key == 'Country:':
                whisky['country'] = value
            elif key == 'Region:':
                whisky['region'] = value
            elif key == 'Distillery status:':
                whisky['distillery_status'] = value
            elif key == 'Age:':
                whisky['age'] = value
            elif key == 'Bottle Size:':
                whisky['bottle_size'] = value

        whisky['lot_num'] = response.css('#itemDescription .lotNo::text').get().split('#')[-1]
        whisky['current_bid'] = response.css('.microdata-price::text').get()
        whisky['currency'] = response.css('meta[itemprop="priceCurrency"]::attr(content)').get()
        desc = response.css('.priceDesc')

        if len(desc) > 1:
            whisky['sold_on'] = desc[1].css('::text').get().replace('Sold', '')
            whisky['winning_bid'] = whisky['current_bid']
        else:
            whisky['reserve'] = desc[0].css('span::text').get()

        whisky['url'] = response.url
        yield whisky


class WhiskyhammerPastSpider(WhiskyhammerSpider):
    name = 'whiskyhammer_past_spider'
    start_urls = ['https://www.whiskyhammer.co.uk/previous-auctions']

    def parse(self, response):
        auctions = response.css('.itemImageWrap > a')
        for auc in auctions:
            href = auc.css('::attr(href)').get()
            date = auc.css('::attr(title)').get().split('-')[-1]
            yield Request(response.urljoin(href), self.parse_products, meta={'date':date})

        next_page = response.css('.next > a::attr(href)').get()
        if next_page:
            yield Request(response.urljoin(next_page), self.parse)


class WhiskyhammerCurrentSpider(WhiskyhammerSpider):
    name = 'whiskyhammer_current_spider'
    start_urls = ['https://whiskyhammer.co.uk/auction/current']

    def start_requests(self):
        yield Request(self.start_urls[0], self.parse_products, meta={'date':datetime.now().date()})

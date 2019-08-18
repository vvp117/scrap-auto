import scrapy
import scrap_drom.items as items


class AutoSpider(scrapy.Spider):
    name = 'auto'
    allowed_domains = ['drom.ru']
    start_urls = ['https://novosibirsk.drom.ru/nissan/tiida/']

    list_auto_xpaths = {
        'title' : './/div[@class="b-advItem__title"]/text()',
        'url' : '@href',
        'engine_capacity' : './/div[@data-ftid="sales__bulls-item_volume-power"]/text()',
        'price' : './/div[@data-ftid="sales__bulls-item_price"]/text()',
    }

    page_auto_xpaths =  {
        'power' : '//span[@data-section="auto-description"]\
                        /div[@data-autodescription-container]/\
                            div[@data-triggers-container]/\
                                div/\
                                    div[1]/text()',
        'date' : '//div[@data-viewbull-views-counter]/text()[1]',
    }

    def parse(self, response):
        list_auto = response.xpath(
            '//div[@class="b-media-cont b-media-cont_modifyMobile_sm"]\
                //a[@class="b-advItem"]'
        )

        for sel_item in list_auto: 
            auto = items.Auto(
                items.get_data(sel_item, AutoSpider.list_auto_xpaths)
            ) 

            yield scrapy.Request(
                url=auto['url'],
                callback=self.parse_auto,
                cb_kwargs={'auto':auto}
                )

        next_page = response.xpath(
            '//div[@data-scroll-pagination]\
                /a[contains(@class, "item_next")]\
                    /@href'
        ).get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_auto(self, response, auto):
        auto.update(
            items.get_data(response, AutoSpider.page_auto_xpaths)
        )

        yield auto

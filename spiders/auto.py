import scrapy


class AutoSpider(scrapy.Spider):
    name = 'auto'
    allowed_domains = ['drom.ru']
    start_urls = ['https://novosibirsk.drom.ru/nissan/tiida/']
    
    limit_pages = 5

    list_auto_xpaths = {
        'auto_title' : './/div[@class="b-advItem__title"]/text()',
        'auto_url' : '@href',
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

    @classmethod
    def get_item_data(cls, sel_item, xpaths):
        return {
            field : sel_item.xpath(xpath).get()
            for field, xpath in xpaths.items()
        }

    def parse(self, response):
        list_auto = response.xpath(
            '//div[@class="b-media-cont b-media-cont_modifyMobile_sm"]'
            '//a[@class="b-advItem"]'
        )

        ix = 0
        for sel_item in list_auto:
            item_data = AutoSpider.get_item_data(
                sel_item,
                AutoSpider.list_auto_xpaths
            ) 

            yield scrapy.Request(
                url=item_data.pop('auto_url'),
                callback=self.parse_auto,
                cb_kwargs=item_data
                )

            ix += 1
            if ix > AutoSpider.limit_pages:
                break

    def parse_auto(self, response, auto_title, engine_capacity, price):
        list_item_data = {
            'auto_title' : auto_title,
            'engine_capacity' : engine_capacity,
            'price' : price,
        } 
        item_data = AutoSpider.get_item_data(
            response,
            AutoSpider.page_auto_xpaths
        )

        list_item_data.update(item_data)
        yield list_item_data

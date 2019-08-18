import scrapy


class Auto(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()
    engine_capacity = scrapy.Field()
    price = scrapy.Field()
    power = scrapy.Field()
    date = scrapy.Field()

    def __setitem__(self, key, value):

        if value:

            if key == 'engine_capacity':
                value = value.strip().split(' ')[0]
            
            elif key == 'price':
                value = int(value.strip().replace('\xa0',''))
            
            elif key == 'power':
                value = value.strip().split(' ')[0]
            
            elif key == 'date':
                value = value.strip().split(' ')[3]

        super().__setitem__(key, value)


def get_data(data_source, xpaths):
    return {
        field : data_source.xpath(xpath).get()
        for field, xpath in xpaths.items()
    }

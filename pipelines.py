from scrapy.exceptions import DropItem


class AutoPriceDromPipeline(object):
    
    def process_item(self, item, spider):

        # save item to file...

        return item

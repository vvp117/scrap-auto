# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class AutoPriceDromPipeline(object):
    
    def process_item(self, item, spider):
        
        if spider.name == 'auto':
            item['engine_capacity'] = item['engine_capacity'].strip().split(' ')[0]
            item['price'] = int(item['price'].strip().replace('\xa0',''))
            item['power'] = item['power'].strip().split(' ')[0]
            item['date'] = item['date'].strip().split(' ')[3]

        return item

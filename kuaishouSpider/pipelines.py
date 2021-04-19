from itemadapter import ItemAdapter
import csv
from scrapy.exceptions import DropItem
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings

setting = get_project_settings()  # 导入设置


class KuaishouspiderPipeline:
    def __init__(self):
        self.f = open('./a.csv', 'w+', encoding='utf-8-sig', newline='')
        header = ['user_id', 'photo_id', 'caption', 'likeCount', 'photoUrl', 'commentId', 'authorId', 'authorName',
                  'content', 'timestamp']
        self.writer = csv.DictWriter(self.f, header)
        self.writer.writeheader()

    def process_item(self, item, spider):
        print(item)
        self.writer.writerow(item)
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['commentId'] in self.ids_seen:
            raise DropItem("过滤重复微博: %s" % item)
        else:
            self.ids_seen.add(item['commentId'])
            return item





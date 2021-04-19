import scrapy


class KuaishouspiderItem(scrapy.Item):
    user_id = scrapy.Field()
    photo_id = scrapy.Field()
    caption = scrapy.Field()
    likeCount = scrapy.Field()
    photoUrl = scrapy.Field()
    commentId = scrapy.Field()
    authorId = scrapy.Field()
    authorName = scrapy.Field()
    content = scrapy.Field()
    timestamp = scrapy.Field()

# -*- coding: utf-8 -*-

BOT_NAME = 'kuaishouSpider'
SPIDER_MODULES = ['kuaishouSpider.spiders']
NEWSPIDER_MODULE = 'kuaishouSpider.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
DOWNLOAD_DELAY = 10
CONCURRENT_REQUESTS = 32
DOWNLOAD_TIMEOUT = 15
TELNETCONSOLE_ENABLED = False
COOKIES_ENABLED = False
LOG_LEVEL = 'ERROR'
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'cookie': 'did=web_f26beaf6116d4597983acd88bbe73ddb; clientid=3; client_key=65890b29; didv=1617374679038; kpf=PC_WEB; kpn=KUAISHOU_VISION; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1617709220; userId=1233619664; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABEdtFkyVGJlhRD534oSkTYHcXX9HkbAlNvqb4knv3GswcNnLOEi05X6oavnROerf5_SGvlisifVUj3tkIRn6jeg2G9vqPWaaHYsxsXt4eles1n1XWABr8qoS6p2MU1LCHvIfWKN-mTcB0ehmWkehFD8fTaZl4dVjUZKs8S_re5sVNGkurCcRieY_4ZhLtMGCjofPN8UsAuPeHyLuIXjCjgRoSS2UWrTnDahVDKzRYjzjLpJM-IiC2tPRD1lq4vhW8krGtrpWEMb0meP7NoP54YBl2IDE3DygFMAE; kuaishou.server.web_ph=db324cebced313e9dbdd7ff3e9fcffdee501',

}
ITEM_PIPELINES = {
    'kuaishouSpider.pipelines.DuplicatesPipeline': 301,
    'kuaishouSpider.pipelines.KuaishouspiderPipeline': 302,
}

# 二选一，默认是使用用户名字
# 设置需要搜索的用户名字
# 设置需要搜索的用户id
# 如果是使用用户id那么精度会大大提升，但是将会失去部分用户数据
# NAME = ['听安']
USER_ID = ['3x53jve2wmk2g32']

# 需要的作品数量
# 默认全部是0，需要多少设置多少，不要超出全部的作品数量
PHOTO_NUM = 0




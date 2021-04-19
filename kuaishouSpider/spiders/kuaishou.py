import scrapy
import json
import jmespath
from scrapy.utils.project import get_project_settings
from kuaishouSpider.items import KuaishouspiderItem
import time


class KuaishouSpider(scrapy.Spider):
    name = 'kuaishou'
    allowed_domains = ['https://video.kuaishou.com/']

    total_url = 'https://video.kuaishou.com/graphql'  # 接口地址
    setting = get_project_settings()  # 导入设置

    num = 0
    photo_num = setting.get('PHOTO_NUM')

    def start_requests(self):
        try:
            name_list = self.settings.get('NAME')
            for name in name_list:
                data = '"variables":{"keyword":"'+name+'"}}'
                body = '{"operationName":"graphqlSearchUser","query":"query graphqlSearchUser($keyword: String, $pcursor: String, $searchSessionId: String) {\n  visionSearchUser(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId) {\n    result\n    users {\n      fansCount\n      photoCount\n      isFollowing\n      user_id\n      headurl\n      user_text\n      user_name\n      verified\n      verifiedDetail {\n        description\n        iconType\n        newVerified\n        musicCompany\n        type\n        __typename\n      }\n      __typename\n    }\n    searchSessionId\n    pcursor\n    __typename\n  }\n}\n",'+data
                yield scrapy.Request(
                    url=self.total_url,
                    method='POST',
                    callback=self.get_user_id,
                    dont_filter=True,
                    body=repr(body).lstrip("'").rstrip("'"),
                    headers={'Content-Type': 'application/json'}
                )
        except:
            user_id_list = self.setting.get('USER_ID')
            for user_id in user_id_list:
                data = '"variables":{"userId":"' + user_id + '","pcursor":"","page":"profile"}}'
                body = '{"operationName":"visionProfilePhotoList","query":"query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",' + data
                yield scrapy.Request(
                    url=self.total_url,
                    method='POST',
                    callback=self.get_video,
                    dont_filter=True,
                    body=repr(body).lstrip("'").rstrip("'"),
                    headers={'Content-Type': 'application/json'},
                    meta={
                        'user_id': user_id,
                    }
                )

    def parse(self, response):
        commentInfo = json.loads(response.text)
        commentList = jmespath.search('data.visionCommentList.rootComments', commentInfo)

        items = KuaishouspiderItem()

        user_id = response.meta.get('user_id')
        caption = response.meta.get('caption')
        likeCount = response.meta.get('likeCount')
        photoUrl = response.meta.get('photoUrl')
        photo_id = response.meta.get('photo_id')

        items['user_id'] = user_id
        items['caption'] = caption
        items['likeCount'] = likeCount
        items['photoUrl'] = photoUrl
        items['photo_id'] = photo_id

        for i in commentList:
            subCommentsPcursor = str(jmespath.search('subCommentsPcursor', i))

            items['authorId'] = jmespath.search('authorId', i)
            items['authorName'] = jmespath.search('authorName', i)
            items['content'] = jmespath.search('content', i)
            items['commentId'] = jmespath.search('commentId', i)

            timestamp = jmespath.search('timestamp', i)
            items['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp/1000))
            yield items

            subComments = jmespath.search('subComments', i)
            if len(subComments) != 0:
                for j in subComments:
                    items['user_id'] = user_id
                    items['caption'] = caption
                    items['likeCount'] = likeCount
                    items['photoUrl'] = photoUrl
                    items['photo_id'] = photo_id

                    items['authorId'] = jmespath.search('authorId', j)
                    items['authorName'] = jmespath.search('authorName', j)
                    items['content'] = jmespath.search('content', j)
                    items['commentId'] = jmespath.search('commentId', j)

                    timestamp = jmespath.search('timestamp', j)
                    items['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000))
                    yield items

            if subCommentsPcursor != 'no_more' and subCommentsPcursor != 'None':
                rootCommentId = str(jmespath.search('commentId', i))

                data = '"variables":{"photoId":"' + photo_id + '","rootCommentId":"' + rootCommentId + '","pcursor":"' + subCommentsPcursor + '"}'
                body = '{' + data + ',"query":"mutation visionSubCommentList($photoId: String, $rootCommentId: String, $pcursor: String) {\n  visionSubCommentList(photoId: $photoId, rootCommentId: $rootCommentId, pcursor: $pcursor) {\n    pcursor\n    subComments {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      likedCount\n      realLikedCount\n      liked\n      status\n      replyToUserName\n      replyTo\n      __typename\n    }\n    __typename\n  }\n}\n"}'
                yield scrapy.Request(
                    url=self.total_url,
                    method='POST',
                    callback=self.comment_parse,
                    dont_filter=True,
                    body=repr(body).lstrip("'").rstrip("'"),
                    headers={'Content-Type': 'application/json'},
                    meta={
                        'user_id': user_id,
                        'caption': caption,
                        'likeCount': likeCount,
                        'photoUrl': photoUrl,
                        'photo_id': photo_id,
                        'rootCommentId': rootCommentId
                    }
                )

        pcursor = str(jmespath.search('data.visionCommentList.pcursor', commentInfo))
        if pcursor != 'no_more':
            data = '"variables":{"photoId":"' + photo_id + '","pcursor":"' + pcursor + '"}}'
            body = '{"operationName":"commentListQuery","query":"query commentListQuery($photoId: String, $pcursor: String) {\n  visionCommentList(photoId: $photoId, pcursor: $pcursor) {\n    commentCount\n    pcursor\n    rootComments {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      likedCount\n      realLikedCount\n      liked\n      status\n      subCommentCount\n      subCommentsPcursor\n      subComments {\n        commentId\n        authorId\n        authorName\n        content\n        headurl\n        timestamp\n        likedCount\n        realLikedCount\n        liked\n        status\n        replyToUserName\n        replyTo\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",' + data

            yield scrapy.Request(
                url=self.total_url,
                method='POST',
                callback=self.parse,
                dont_filter=True,
                body=repr(body).lstrip("'").rstrip("'"),
                headers={'Content-Type': 'application/json'},
                meta={
                    'photo_id': photo_id,
                    'caption': caption,
                    'likeCount': likeCount,
                    'photoUrl': photoUrl,
                    'user_id': response.meta.get('user_id'),
                }
            )

    def comment_parse(self, response):
        commentInfo = json.loads(response.text)
        commentList = jmespath.search('data.visionSubCommentList.subComments', commentInfo)
        items = KuaishouspiderItem()

        user_id = response.meta.get('user_id')
        caption = response.meta.get('caption')
        likeCount = response.meta.get('likeCount')
        photoUrl = response.meta.get('photoUrl')
        photo_id = response.meta.get('photo_id')
        rootCommentId = response.meta.get('rootCommentId')

        items['user_id'] = user_id
        items['caption'] = caption
        items['likeCount'] = likeCount
        items['photoUrl'] = photoUrl
        items['photo_id'] = photo_id

        for i in commentList:
            items['authorId'] = jmespath.search('authorId', i)
            items['authorName'] = jmespath.search('authorName', i)
            items['content'] = jmespath.search('content', i)
            items['commentId'] = jmespath.search('commentId', i)

            timestamp = jmespath.search('timestamp', i)
            items['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp/1000))
            yield items

        pcursor = str(jmespath.search('data.visionSubCommentList.pcursor', commentInfo))
        if pcursor != 'no_more':
            data = '"variables":{"photoId":"' + photo_id + '","rootCommentId":"' + str(rootCommentId) + '","pcursor":"' + pcursor + '"}'
            body = '{"operationName":"visionSubCommentList","query":"mutation visionSubCommentList($photoId: String, $rootCommentId: String, $pcursor: String) {\n  visionSubCommentList(photoId: $photoId, rootCommentId: $rootCommentId, pcursor: $pcursor) {\n    pcursor\n    subComments {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      likedCount\n      realLikedCount\n      liked\n      status\n      replyToUserName\n      replyTo\n      __typename\n    }\n    __typename\n  }\n}\n",' + data
            yield scrapy.Request(
                url=self.total_url,
                method='POST',
                callback=self.comment_parse,
                dont_filter=True,
                body=repr(body).lstrip("'").rstrip("'"),
                headers={'Content-Type': 'application/json'},
                meta={
                    'user_id': user_id,
                    'caption': caption,
                    'likeCount': likeCount,
                    'photoUrl': photoUrl,
                    'photo_id': photo_id,
                    'rootCommentId': rootCommentId
                }
            )

    def get_user_id(self, response):
        userInfo = json.loads(response.text)
        user_id = jmespath.search('data.visionSearchUser.users[0].user_id', userInfo)

        data = '"variables":{"userId":"' + user_id + '","pcursor":"","page":"profile"}}'
        body = '{"operationName":"visionProfilePhotoList","query":"query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",' + data
        yield scrapy.Request(
            url=self.total_url,
            method='POST',
            callback=self.get_video,
            dont_filter=True,
            body=repr(body).lstrip("'").rstrip("'"),
            headers={'Content-Type': 'application/json'},
            meta={
                'user_id': user_id,
            }
        )

    def get_video(self, response):
        videoInfo = json.loads(response.text)
        pcursor = str(jmespath.search('data.visionProfilePhotoList.pcursor', videoInfo))
        user_id = response.meta.get('user_id')

        videoList = jmespath.search('data.visionProfilePhotoList.feeds', videoInfo)

        for i in videoList:
            if self.num < self.photo_num or self.photo_num == 0:
                photo_id = jmespath.search('photo.id', i)
                caption = jmespath.search('photo.caption', i)
                likeCount = jmespath.search('photo.likeCount', i)
                photoUrl = jmespath.search('photo.photoUrl', i)

                data = '"variables":{"photoId":"' + photo_id + '","pcursor":""}}'
                body = '{"operationName":"commentListQuery","query":"query commentListQuery($photoId: String, $pcursor: String) {\n  visionCommentList(photoId: $photoId, pcursor: $pcursor) {\n    commentCount\n    pcursor\n    rootComments {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      likedCount\n      realLikedCount\n      liked\n      status\n      subCommentCount\n      subCommentsPcursor\n      subComments {\n        commentId\n        authorId\n        authorName\n        content\n        headurl\n        timestamp\n        likedCount\n        realLikedCount\n        liked\n        status\n        replyToUserName\n        replyTo\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",' + data

                self.num += 1
                yield scrapy.Request(
                    url=self.total_url,
                    method='POST',
                    callback=self.parse,
                    dont_filter=True,
                    body=repr(body).lstrip("'").rstrip("'"),
                    headers={'Content-Type': 'application/json'},
                    meta={
                        'photo_id': photo_id,
                        'caption': caption,
                        'likeCount': likeCount,
                        'photoUrl': photoUrl,
                        'user_id': response.meta.get('user_id'),
                    }
                )
            else:
                return None

        if pcursor != 'no_more':
            data = '"variables":{"userId":"' + user_id + '","pcursor":"' + pcursor + '","page":"profile"}}'
            body = '{"operationName":"visionProfilePhotoList","query":"query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",' + data
            yield scrapy.Request(
                url=self.total_url,
                method='POST',
                callback=self.get_video,
                dont_filter=True,
                body=repr(body).lstrip("'").rstrip("'"),
                headers={'Content-Type': 'application/json'},
                meta={
                    'user_id': user_id,
                }
            )



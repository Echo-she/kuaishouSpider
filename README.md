### 功能

本项目使用Scrapy框架进行爬取，获取指定作者，指定作品数量的所有评论信息，并将结果写入文件（csv）

### 输出

- 作者id：用于后面判断是否爬取到了想要的的作者

- 作品id：区分每个作者评论的作品

- 作品简介：看看就好（手动滑稽）

- 作品点赞数量：用于判断每个作品的质量，当作选择的一个权重

- 作品视频地址：看看就好（手动滑稽）

- 评论id：区分每个评论的依据

- 评论人id：区分每个评论人的依据，因为可能会存在重名

- 评论人名字：看看就好（手动滑稽）

- 评论：评论人发布的内容

- 评论时间：评论人发布的时间


### 使用说明

本程序的所有配置都在setting.py文件中完成

#### **1.下载脚本**

```bash
$ git clone https://github.com/Unlucky-she/kuaishouSpider.git
```

#### **2.安装Scrapy**

本程序依赖Scrapy，要想运行程序，需要安装Scrapy。如果系统中没有安装Scrapy，请根据自己的系统安装Scrapy，以Ubuntu为例，可以使用如下命令：

```bash
$ pip install scrapy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 3.设置Cookie

DEFAULT_REQUEST_HEADERS中的cookie是我们需要填的值，如何获取cookie详见[如何获取cookie](#如何获取cookie)，获取后将"your cookie"替换成真实的cookie即可。

#### 4.设置需要爬取的作者名字（二选一，默认是这个）

修改setting中NAME参数。如果你只想爬取一个作者，如“开心锤锤”：

```bash
NAME = ['开心锤锤']
```

当然也可以设置多个要爬取的作者

```bash
NAME = ['开心锤锤', '不白吃', '###'......]
```

注：这个方法适合爬取名声比较大的作者，因为程序是根据快手搜索出来的第一个进行选择，而一般第一个就是名声比较大的作者，如果想爬取指定的作者详见下面。

#### 5.设置需要爬取的作者id（二选一）

修改setting中NAME参数。如果你只想爬取一个作者，如“开心锤锤”，那么他的id是3xjqwcb3stdnz9k：

```bash
USER_ID = ['3xjqwcb3stdnz9k']
```

当然也可以设置多个要爬取的作者

```bash
USER_ID = ['3xjqwcb3stdnz9k', '###'......]
```

注：这个是专门为了指定作者而准备的，具体怎么获得作者id详见 [如何获取作者id](#如何获取作者id)

#### 6.设置需要爬取的作品数量（可选）

修改setting中PHOTO_NUM参数。如果想爬取10条作品，那么：

```bash
PHOTO_NUM = 10
```

#### 7.设置等待时间（可选）

DOWNLOAD_DELAY代表访问完一个页面再访问下一个时需要等待的时间，默认为10秒。如我想设置等待15秒左右，可以修改setting.py文件的DOWNLOAD_DELAY参数：

```bash
DOWNLOAD_DELAY = 15
```

### 如何获取cookie

打开浏览器，进入快手官网，登录，按F12，刷新网页，选择筛选xhr，选择容易一个请求，复制其中的cookie即可，如下图

![image-20210415185547058](C:\Users\SJ\AppData\Roaming\Typora\typora-user-images\image-20210415185547058.png)



### 如何获取作者id

打开快手官网，选择短视频，输入想要的用户名字，进入他的主页，导航栏后面的一串数字就是他的id，如见下图红框部分

![image-20210415183922239](C:\Users\SJ\AppData\Roaming\Typora\typora-user-images\image-20210415183922239.png)
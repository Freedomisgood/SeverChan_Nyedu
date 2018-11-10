# SeverChan_Nyedu
Crawl the infomation about competitons, when new infos comes, remind people on Wechat by ServerChan:

:heart_eyes:该程序通过爬取[南邮教务处](http://jwc.njupt.edu.cn/1594/list.htm),将当前时间与最新时间进行匹配,如果是当日则通过ServerChan发送到本人的微信,提醒有新的竞赛.





#### 完成笔记:

##### 1.关于`lxml`中`etree.xpath()`对于`tbody`的处理

> 该网页通过`table`对页面进行分布设置,其中`table`标签会自动生成`tbody`标签,如图..此时用`xpath`进行匹配的时候就不需要将`tbody`加上,否则匹配不到

布局`<Table>`

![Nonetbody](https://github.com/Freedomisgood/SeverChan_Nyedu/images/blob/master/Nonetbody.jpg)

表格`<table>`

![Table_tbody](https://github.com/Freedomisgood/SeverChan_Nyedu/images/blob/master/Table_tbody.jpg)



可以看到的是在Chrome调试助手里面,`<table>`下面都是会自动生成`<tbody>`标签的,而我们再通过**网页源码**看看..==>可以发现的是:

**`<table>`布局是没有`<tbody>`的,只有表格才有**,所以这也是为什么用xpath()表格里必须加上`tbody`才能匹配,而`table`布局中不能加`tbody`的原因

```python
#布局获得内容
for content in contentList:
    title = content.xpath('td/table/tr/td[1]/a/text()')[0]
    href = content.xpath('td/table/tr/td[1]/a/@href')[0]
    submittime = content.xpath('td/table/tr/td[2]/div/text()')[0]

#表格
if content.tag == 'table':
    tabletitle = content.xpath('tbody/tr[1]/td')  # 表格头
    tabletitleList = map(lambda x: x.xpath('string(.)'), tabletitle)
    tablehead = '|' + '|'.join(tabletitleList) + '|' 
    tableover = '|' + ':---:|' * len(tabletitle)  # 居中显示
```

![real_code](https://github.com/Freedomisgood/SeverChan_Nyedu/images/blob/master/real_code.jpg)



##### 2.`requests.get()`获得的response的编码问题

```python
html = requests.get('http://jwc.njupt.edu.cn/1594/list.htm',headers = headers)
html.encoding = 'utf-8'
#Requests库的自身编码为: r.encoding = ‘ISO-8859-1’
```
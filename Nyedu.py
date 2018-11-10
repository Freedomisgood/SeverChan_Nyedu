import requests
from lxml import etree
import time
import re
from logfile import logger


headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}
_time = time.strftime("%Y-%m-%d", time.localtime())


def get_newest_info(secret_key):
    html = requests.get('http://jwc.njupt.edu.cn/1594/list.htm',headers = headers)
    html.encoding = 'utf-8'
    #Requests库的自身编码为: r.encoding = ‘ISO-8859-1’
    data = etree.HTML(html.text)
    contentList = data.xpath('//*[@id="newslist"]/div/table/tr')
    for content in contentList:
        title = content.xpath('td/table/tr/td[1]/a/text()')[0]
        href = content.xpath('td/table/tr/td[1]/a/@href')[0]
        submittime = content.xpath('td/table/tr/td[2]/div/text()')[0]
        if title.startswith('【实践科】') and submittime=="2018-11-09":
            if href.endswith('.htm'):
                detail = getDetailpage(href)
                data_info = {
                    'text': title ,
                    'desp': detail
                }
                # submit_info(secret_key,data_info)
                logger.info('完成发送')


def getDetailpage(aurl):
    prefix = 'http://jwc.njupt.edu.cn'
    url = prefix + aurl
    html = requests.get(url=url,headers=headers)
    html.encoding = 'utf-8'
    data = etree.HTML(html.text)
    contentList = data.xpath('//div[@id="container_content"]/table/tr/td/table[5]/tr/td/div/div/div')[0]
    str = ''
    for content in contentList:
        if content.tag == 'table':
            tabletitle = content.xpath('tbody/tr[1]/td')  # 表格头
            tabletitleList = map(lambda x: x.xpath('string(.)'), tabletitle)
            tablehead = '|' + '|'.join(tabletitleList) + '|'  # 效果为|序号|学号|姓名|性别|学院|专业|
            tableover = '|' + ':---:|' * len(tabletitle)  # 居中显示

            tablecontent = ''
            trs = content.xpath('tbody/tr')
            for tr in trs[1:]:                                 #多行row
                tds = map(lambda x: x.xpath('string(.)'), tr)  # 一行内容
                tablecontent += '|' + '|'.join(tds) + '|' + '\n'

            tableinfo = tablehead + '\n' + tableover + '\n' + tablecontent
            str += '\n' + tableinfo + '\n' #将表格分离开一点
        else:
            Pcontent = content.xpath('string(.)')
            if re.match('["一二三四五六七八九十"]+、', Pcontent):
                str += "####" + Pcontent + '\n\n'
            elif re.match('\d+.', Pcontent):
                str += "#####" + Pcontent + '\n\n'
            else:
                str += content.xpath('string(.)') + '\n\n'
    return str


def submit_info(secret_key,info):
    requests.post(url = 'https://sc.ftqq.com/{}.send'.format(secret_key),data=info)


if __name__ == "__main__" :
    get_newest_info('SCU35113Te369cebc21f6e483c03fffc400c4c5c05bdad63995c32')



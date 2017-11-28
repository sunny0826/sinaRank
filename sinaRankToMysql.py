#!/usr/bin/env python
#encoding: utf-8
#Author: guoxudong
import sys
import pymysql.cursors
import uuid

from datetime import datetime
from lxml import etree
from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf-8')
def sinaRankToMysql():
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='xxxxxx',
        passwd='xxxxxx',
        db='djangodb',
        charset='utf8'
    )

    driver = webdriver.PhantomJS()
    url = 'http://s.weibo.com/top/summary?cate=realtimehot'
    driver.get(url)
    pageSource = driver.page_source
    driver.close()
    tree = etree.HTML(pageSource)
    trinfo = tree.xpath('//table/tbody/tr')

    # 获取游标
    cursor = connect.cursor()
    # 插入数据
    sql = "INSERT INTO dashboard_sinarank VALUES('%s', '%i','%s', '%s', '%s', '%s')"

    for index,info in enumerate(trinfo):
        trtext = info.xpath('td/div/p/a')[0].text
        if(str(info.xpath('td/div/p/a')[0].attrib).split("'")[3]=='realtimehot_ad'):
            trhref = str(info.xpath('td/div/p/a')[0].attrib).split("'")[7]
        else:
            trhref = str(info.xpath('td/div/p/a')[0].attrib).split("'")[3]
        trnum = info.xpath('td/p/span')[0].text
        id = index+1
        now_time = datetime.now()
        truuid = str(uuid.uuid1())
        data = (truuid, id, trtext, trhref, trnum, now_time)
        cursor.execute(sql % data)
        connect.commit()
        print('成功插入', cursor.rowcount, '条数据')
        print index+1
        print trtext
        print trhref
        print trnum
    # 关闭连接
    cursor.close()
    connect.close()
    print None

sinaRankToMysql()

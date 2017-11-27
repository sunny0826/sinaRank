#!/usr/bin/env python
#encoding: utf-8
#Author: guoxudong
import json
import sys
import urllib
import urllib2
import uuid

from lxml import etree
import sqlite3
from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf-8')

def sinaRank():
    driver = webdriver.PhantomJS()
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    url = 'http://s.weibo.com/top/summary?cate=realtimehot'
    driver.get(url)
    pageSource = driver.page_source
    driver.close()
    tree = etree.HTML(pageSource)
    trinfo = tree.xpath('//table/tbody/tr')
    for index,info in enumerate(trinfo):
        trtext = info.xpath('td/div/p/a')[0].text
        if(str(info.xpath('td/div/p/a')[0].attrib).split("'")[3]=='realtimehot_ad'):
            trhref = str(info.xpath('td/div/p/a')[0].attrib).split("'")[7]
        else:
            trhref = str(info.xpath('td/div/p/a')[0].attrib).split("'")[3]
        trnum = info.xpath('td/p/span')[0].text
        id = index+1
        now_time = sqlite3.datetime.datetime.now()
        truuid = str(uuid.uuid1())
        cursor.execute('INSERT INTO sinarank VALUES(?,?,?,?,?,?) ', (truuid, id, trtext, trhref, trnum, now_time))
        print index+1
        print trtext
        print trhref
        print trnum
    conn.commit()
    conn.close()
    print None

def ticketsInfo():
    url = 'https://search.damai.cn/searchajax.html'
    textmod = {'keyword': '陈奕迅周杰伦五月天', 'cty': '上海','ctl':'','tn':'','sctl':'','singleChar':'','order':''}
    textmod = urllib.urlencode(textmod)     #将参数格式化
    req = urllib2.Request(url=url, data=textmod)
    res = urllib2.urlopen(req)
    res = res.read()
    info = json.loads(res)
    info = info.get('pageData').get('resultData')
    leninfo = len(info)
    for port in info:
        name = port.get('nameNoHtml')
        price = port.get('pricestr')
        venue = port.get('venue')
        # star = port.get('actors')
        stars = ''
        for starname in port.get('starname'):
            # stars.append(starname.decode('utf8'))
            stars += starname+' '
        print '名称：%s' % name
        print '价格：%s' % price
        print '场馆：%s' % venue
        # print star
        print '艺人：%s' % stars
        print '-----------------------'
    print info

sinaRank()
# ticketsInfo()
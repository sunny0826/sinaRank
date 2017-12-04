#!/usr/bin/env python
#encoding: utf-8
#Author: guoxudong
import json
import urllib
import urllib2
import uuid

import datetime
import pymysql
import re

def bilibililist():
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='xxx',
        passwd='xxx',
        db='djangodb',
        charset='utf8'
    )
    opener = urllib2.build_opener()
    f = opener.open('https://bangumi.bilibili.com/web_api/timeline_global')
    page = f.read()
    resluts = json.loads(page)
    # 获取游标
    cursor = connect.cursor()
    # 插入数据
    datesql = "INSERT INTO dashboard_bilibilidate VALUES('%s', '%s', '%s', '%i', '%i')"
    detailsql = "INSERT INTO dashboard_bilibiledetail VALUES('%s', '%s', '%s', '%s', '%s', '%s')"
    if resluts.get('message') == 'success':
        resultList = resluts.get('result')
        for list in resultList:
            date = list.get('date')
            date_ts = datetime.datetime.fromtimestamp(list.get('date_ts'))
            day_of_week = list.get('day_of_week')
            is_today = list.get('is_today')
            id = str(uuid.uuid1())
            data = (id, date, date_ts, day_of_week, is_today)
            cursor.execute(datesql % data)
            connect.commit()
            for info in list.get('seasons'):
                pkid = str(uuid.uuid1())
                fkid = id
                square_cover = info.get('square_cover')
                title = info.get('title')
                pub_time = info.get('pub_time')
                pub_index = info.get('pub_index')
                data = (pkid, fkid, square_cover, title, pub_time, pub_index)
                cursor.execute(detailsql % data)
                connect.commit()
        return True
    else:
        return False

# def bilibiliphoto():
#     #http://i0.hdslb.com/bfs/bangumi/cc78256da3f4aa3162d5933382900986c1a7e67f.jpg
#     # opener = urllib2.build_opener()
#     # f = opener.open('http://i0.hdslb.com/bfs/bangumi/cc78256da3f4aa3162d5933382900986c1a7e67f.jpg')
#     # page = f.read()
#     f = open( '1.jpg', "wb")  # 打开文件
#     req = urllib2.urlopen('http://i0.hdslb.com/bfs/bangumi/cc78256da3f4aa3162d5933382900986c1a7e67f.jpg')
#     buf = req.read()
#     f.write(buf)
#     return buf

if __name__ == '__main__':
    bilibililist()
    # bilibiliphoto()
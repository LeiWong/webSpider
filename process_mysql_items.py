#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import MySQLdb
import json

# 创建Redis数据库连接
rediscli = redis.StrictRedis(host="192.168.13.26", port = 6379, db = 0)

# 创建MySQL数据库连接
mysqlcli = MySQLdb.connect(host="127.0.0.1", user = "power", passwd = "60055969", db = "youyuan", port = 3306)

while True:
    # 从redis里获取数据，放到data里
    source, data = rediscli.blpop("youyuan:items")
    # loads(data), 转换为item
    item = json.loads(data)

    try:
                # 使用cursor() 获取数据库操作游标
        cursor = mysqlcli.cursor()
                # sql语句：向指定的表插入数据，数据来自于item
        cursor.execute('insert into beijing (username, header_url, requer, pic_url,age, source, source_url, crawled, spider) \
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', \
                    item["username"], [item["header_url"],item["requer"],item["pic_url"], \
                    item["age"],item["source"],item["source_url"],item["crawled"],item["spider"]])
                # 提交mysql事务
        mysqlcli.commit()
        print "插入数据成功"
            # 关闭操作游标
        cursor.close()
    except MySQLdb.Error, e:
        print "插入出错 %d : %d ", e.args[0], e.args[1]




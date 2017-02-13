#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import pymongo
import json

def start():
    # 创建redis数据库连接
    rediscli = redis.Redis(host = "192.168.13.26", port = 6379, db = "0")
    # 创建mongodb数据库连接
    mongodbcli = pymongo.MongoClient(host = "127.0.0.1", port = 27017)

    # 指定mongod数据库名称
    database = mongodbcli["youyuan"]
    # 指定mongod数据库对应的表
    datasheet = database["beijing"]

    while True:
        source, data = rediscli.blpop(["youyuan:items"])
        item = json.loads(data)
        datasheet.insert(item)

        print "插入成功"

if __name__ == "__main__":
    start()



# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/10/18

import pymysql

mariadb = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='tupu', charset='GBK')

def get_topn(query, name, topn=10):
    '''
    query: query string
    name: entity name
    topn: return num of results
    :return: list of (relation_name, answer)
    '''

    with mariadb.cursor() as cursor:
        sql = 'select `predicate`, `value` from tupu_triple wher `name`=%s limit=10'
        cursor.execute(sql, name)
        result_list = cursor.fetchall()

    return list(result_list)

mariadb.close()

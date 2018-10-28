# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/3/25 0025

import pymysql


class MysqlHelper(object):
    """链接mysql类"""
    def __init__(self, host, port, db, user, password, charset):
        """
        初始化方法
        :param str host: 主机ip地址
        :param int port: 端口
        :param str db: 数据库名
        :param str user: 用户
        :param str password: 密码
        :param str charset: 编码
        """
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.charset = charset
        self.conn = None
        self.cursor = None

    def open(self):
        """链接mysql数据库"""
        self.conn = pymysql.connect(host=self.host, port=self.port, db=self.db, user=self.user,
                                    password=self.password, charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        """关闭mysql数据库"""
        self.cursor.close()
        self.conn.close()

    def cud(self, sql, params):
        """

        :param sql:
        :param list params:
        :return:
        """
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            print('OK')
        except Exception as e:
            print(e)

    def all(self, table):
        try:
            sql = 'select * from %s' % table
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(e)

    def specific(self, sql):
        """
        执行特定的sql语句
        :param str sql: 要执行的sql语句
        :return:
        """
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(e)

    def specific_update(self, sql):
        """
        执行特定的update，sql语句
        :param str sql: 要执行的update sql语句
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
    
    def __del__(self):
        self.close()

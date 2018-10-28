# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/10/15

from mysql_help.mysql_helper import MysqlHelper

import sys
sys.path.insert(0, '/search/odin/wanjie/MatchZoo-master/matchzoo')
import matchzoo


class GetData(object):
    """获取数据类"""
    def __init__(self):
        """初始化方法"""
        self.mysql_helper = MysqlHelper(
            host='10.143.16.25', port=3306, db='tupu', user='wanjie', password='wanjie', charset='gbk')
        self.mysql_helper.open()

    def get_data(self, name):
        """
        获取数据方法
        :param str name: name字段
        :return:
        """
        result_dict = {}
        sql = "select * from tupu_triple where name='{}'".format(name)
        result_tuple = self.mysql_helper.specific(sql)
        for item in result_tuple:
            if item[2] not in result_dict:
                result_dict[item[2]] = [item[3]]
            else:
                result_dict[item[2]].append(item[3])
        for key, value in result_dict.items():
            result_dict[key] = sorted(value)
        return result_dict

    def get_entity_list(self, query):
        """
        获取实体方法
        :param str query: query字段内容
        :rtype: list
        :return: 实体列表
        """
        sql = "select * from biaozhu_query where query='{}' and is_done=2".format(query)
        result_tuple = self.mysql_helper.specific(sql)
        one_id, query, entities, is_done = result_tuple[0]
        entity_list = entities.split('|')
        return one_id, entity_list

    # def get_entity_relationship(self, query, name, top=10):
    #     """
    #     获取
    #     :param query:
    #     :param name:
    #     :param top:
    #     :return:
    #     """
    #     sql = "select `predicate`, `value` from tupu_triple where name='{}' limit 10".format(name)
    #     entity_relationship_tuple = self.mysql_helper.specific(sql)
    #     return entity_relationship_tuple

    def get_entity_relationship(self, query, entity, top=10):
        """
        获取
        :param query: query
        :param entity: 实体
        :param top:
        :return:
        """
        result = matchzoo.get_topn(query, entity)
        if len(result) < top:
            return result
        else:
            return result[:top]

    def insert_into_result_and_update(self, query, entity, relation, answer, is_fault, one_id):
        """
        插入数据库并修改之前的数据库
        :param str query:
        :param str entity:
        :param str relation:
        :param str answer:
        :param int is_fault:
        :param str one_id:
        :return:
        """
        sql = 'insert into biaozhu_query_result VALUE (%s, %s, %s, %s, %s, %s)'
        self.mysql_helper.cud(sql, [0, query, entity, relation, answer, is_fault])

        one_id = int(one_id)
        sql1 = "update `biaozhu_query` set `is_done`={} where `id`={} and `is_done`=2".format(1, one_id)
        self.mysql_helper.specific_update(sql1)

    def get_next(self, one_id):
        """
        获取下一个query
        :param str one_id:
        :rtype: int
        :return:
        """
        next_id = int(one_id)
        while True:
            next_id += 1
            sql = "select query, is_done from biaozhu_query where id={}".format(next_id)
            result = self.mysql_helper.specific(sql)
            if result:
                next_query, next_is_done = result[0]
                if next_is_done == 0:
                    sql1 = "update biaozhu_query set is_done=2 where `id`={}".format(next_id)
                    self.mysql_helper.specific_update(sql1)
                    break
            else:
                return None
        return next_query

    def get_first_query_not_done(self):
        """
        获取第一个没有被核查的query
        :return:
        """
        sql = "select `id`, query from biaozhu_query where is_done=0 limit 1"
        result = self.mysql_helper.specific(sql)
        one_id, query = result[0]
        sql_update = "update biaozhu_query set is_done=2 where `id`={}".format(one_id)
        self.mysql_helper.specific_update(sql_update)
        return query

# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/10/22

# -*- coding: utf8 -*-
import sys
import os
sys.path.insert(0, '/search/odin/wanjie/MatchZoo-master/matchzoo')
import matchzoo


# print('=========')
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.getcwd())

# os.chdir("/search/odin/wanjie/MatchZoo-master")
# result = matchzoo.get_topn('刘德华身高是多少', '刘德华')
# print result


def test_result():
    return matchzoo.get_topn('刘德华身高是多少', '刘德华')
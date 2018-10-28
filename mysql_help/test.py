# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/10/17

from mysql_help.get_data import GetData


def main():
    get_data = GetData()
    # entity_list = get_data.get_data('五险是哪五险'.decode('utf-8').encode('gbk'))
    # # for key, value in data.items():
    # #     data[key] = sorted(value)
    # print(entity_list)
    # for i in entity_list:
    #     print(i)

    print get_data.get_entity_relationship('五险是哪五险', '五险')


if __name__ == '__main__':
    main()

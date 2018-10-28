# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from mysql_help.get_data import GetData


def search(request):
    """搜索view"""
    return render(request, 'search/search.html')


def result(request):
    """结果view"""
    get_data = GetData()
    post = request.POST
    keyword = post.get('keyword')
    result_list = get_data.get_data(keyword.encode('gbk'))
    context = {
        'result_list': result_list
    }
    return render(request, 'search/result.html', context=context)


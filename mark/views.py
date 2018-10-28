# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import unicode_literals

from django.shortcuts import render
from mysql_help.get_data import GetData

import sys
sys.path.insert(0, '/search/odin/wanjie/MatchZoo-master/matchzoo')
import matchzoo


def search(request):
    """搜索view"""
    get_data = GetData()
    query = get_data.get_first_query_not_done()
    context = {
        'query': query
    }
    return render(request, 'mark/search.html', context)


def result(request):
    """结果view"""
    context = {}
    get_data = GetData()
    post = request.POST
    query = post.get('query')
    one_id, entity_list = get_data.get_entity_list(query.encode('gbk'))
    context['one_id'] = one_id
    context['query'] = query
    context['entity_list'] = entity_list
    if 'entity' in post.keys() and 'relationship' in post.keys():
        context['entity'] = post.get('entity')
        context['relationship'] = post.get('relationship')
        entity_relationship_list = []
        # count = 0
        # while not entity_relationship_list:
        #     entity_relationship_list = matchzoo.get_topn(query.encode('utf-8'), context['entity'].encode('utf-8'))
        #     count += 1
        #     if count == 100:
        #         break
        entity_relationship_list = matchzoo.get_topn(query.encode('utf-8'), context['entity'].encode('utf-8'))
        # entity_relationship_list = get_data.get_entity_relationship('刘德华身高是多少', '刘德华')
        # entity_relationship_list = matchzoo.get_topn('刘德华身高是多少'.encode('utf-8'), '刘德华'.encode('utf-8'))
        context['entity_relationship_list'] = entity_relationship_list
    else:
        # print entity_list[0]
        # print type(entity_list[0])
        # print type(entity_list[0].encode('gbk'))
        # print query, entity_list[0]
        entity_relationship_list = []
        # count = 0
        # while not entity_relationship_list:
        #     entity_relationship_list = matchzoo.get_topn(query.encode('utf-8'), entity_list[0].encode('utf-8'))
        #     count += 1
        #     if count == 100:
        #         break
        entity_relationship_list = matchzoo.get_topn(query.encode('utf-8'), entity_list[0].encode('utf-8'))
        # print '100000000000000000000000:'
        # print entity_relationship_list
        # entity_relationship_list = get_data.get_entity_relationship('刘德华身高是多少', '刘德华')
        # entity_relationship_list = matchzoo.get_topn('刘德华身高是多少'.encode('utf-8'), '刘德华'.encode('utf-8'))
        context['entity_relationship_list'] = entity_relationship_list
    return render(request, 'mark/result.html', context)


def submit(request):
    """提交view"""
    get_data = GetData()
    post = request.POST
    entity = post.get('entity')
    relationship = post.get('relationship')
    input1 = post.get('input1')
    input2 = post.get('input2')
    if input1 and input2:
        relation = post.get('input1').encode('gbk')
        answer = post.get('input2').encode('gbk')
        is_fault = 0
    else:
        if entity == '没有候选实体' and relationship == '没有候选关系':
            entity = None
            relation = None
            answer = None
            is_fault = 1
        elif entity != '没有候选实体' and relationship == '没有候选关系':
            relation = None
            answer = None
            is_fault = 1
        elif entity == '没有候选实体' and relationship != '没有候选关系':
            entity = None
            relation = None
            answer = None
            is_fault = 1
        else:
            relation, answer = relationship.split(':')
            relation = relation.encode('gbk')
            answer = answer.encode('gbk')
            is_fault = 0
    query = post.get('query')
    one_id = post.get('one_id')
    get_data.insert_into_result_and_update(query.encode('gbk'), entity, relation, answer, is_fault, one_id)
    context = {
        'next_query': get_data.get_next(one_id)
    }
    return render(request, 'mark/submit.html', context)
    # return HttpResponseRedirect('/mark/result/')
    # request.POST['query'] = get_data.get_next(one_id)
    # request.session['query'] = context['next_query']
    # # request.POST['query'] = context['next_query']
    # return redirect('/mark/search/')


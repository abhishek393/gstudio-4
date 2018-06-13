import os
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Node
from django.utils import timezone
from elasticsearch import Elasticsearch
es = Elasticsearch()

def create(request):
    if request.method == 'POST':
        data = request.POST
        node_obj = Node(
            name=data.get('name'),
            created_at=data.get('created_at'),
            created_by=data.get('created_by'),
            last_update=data.get('last_update'))
        path_to_data_dir = 'data/node/'
        try:
            create.version_id += 1
        except AttributeError:
            create.version_id = 0
        json_data = node_obj.get_json()
        res = es.index(index="data", doc_type='node', id=create.version_id, body=json_data)
        return HttpResponse(json.dumps({'SUCCESS': 'SUCCESS'}), content_type='application/json')
    else:
        return HttpResponse(
            json.dumps({'ERROR': 'Wrong request method'}), content_type='application/json')


def read(request):
    data = request.POST
    data_dict = dict(data)
    json_query = {}
    for key in data_dict.keys():
        json_query[key] = data_dict[key][0]
    searched_data = es.search(index='data', doc_type='node', body={'query': {'match': json_query}})
    return HttpResponse(json.dumps(searched_data), content_type='application/json')


def update(request):
    data = request.POST
    data_dict = dict(data)   
    json_query = {}
    for key in data_dict.keys():
        json_query[key] = data_dict[key][0]
    for key_2 in json_query.keys():
        value = json_query[key_2]
    searched_list = value.split(",")
    reqd_dict= {}
    update_dict = {}
    for k in json_query.keys():
        reqd_dict[k] = searched_list[0]
        update_dict[k] = searched_list[1]
    searched_data = es.search(index='data', doc_type='node', body={'query': {'match': reqd_dict}})
    reqd_id = []
    for hit in searched_data['hits']['hits']:
         reqd_id.append(hit['_id'])
    i=0
    for z in reqd_id:   
        searched_data['hits']['hits'][i]['_source'][key_2] = searched_list[1]
        res = es.index(index="data", doc_type='node', id= int(z), body=searched_data['hits']['hits'][i]['_source'])
        i=i+1
    return HttpResponse(json.dumps({'SUCCESS': 'SUCCESS'}), content_type='application/json')
	


def delete(request):
    data = request.POST
    data_dict = dict(data)
    json_query = {}
    for key in data_dict.keys():
        json_query[key] = data_dict[key][0]
    searched_data = es.search(index='data', doc_type='node', body={'query': {'match': json_query}})
    reqd_id = []
    for hit in searched_data['hits']['hits']:
        reqd_id.append(hit['_id'])
    for z in reqd_id:  
        res = es.delete(index="data", doc_type='node', id= int(z))
    return HttpResponse(json.dumps({'SUCCESS': 'SUCCESS'}), content_type='application/json')
        


    
    

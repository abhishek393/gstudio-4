import os
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Node
from django.utils import timezone
from elasticsearch import Elasticsearch

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
        json_file = open(path_to_data_dir + 'file_' + str(create.version_id) + '.json', 'w+')
        json_data = node_obj.get_json()
        json_file.write('POST data/node/' + '\n' + json_data)
        json_file.close()
        return HttpResponse(json.dumps({'SUCCESS': 'SUCCESS'}), content_type='application/json')
    else:
        return HttpResponse(
            json.dumps({'ERROR': 'Wrong request method'}), content_type='application/json')


def read(request):
    data = request.POST
    es = Elasticsearch()
    searched_data = es.search(index='data', doc_type='node', body={'query': {'match': data }})
    return HttpResponse(json.dumps(searched_data), content_type='application/json')


def update(request):
    pass


def delete(request):
    pass

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import os
from .models import Node
from django.utils import timezone


@static_vars(ver=0)
def create(request):
	if request.method == 'POST':
		data = request.POST
		node_obj = Node(name = data.get('name'), created_at = data.get('created_at'),created_by = data.get('created_by'),last_update = data.get('last_update'))
		currunt_dir = os.pwd()
		path_to_data_dir = os.path.join(currunt_dir, '/data/')
		fl = open(path_to_data_dir + "node_file_" + ver + ".json", "w+")
		json_file = node_obj.get_json()
		fl.write(json_file)
		ver = ver + 1
		return HttpResponse((json.dumps('SUCCESS' : 'SUCCESS')), content_type="application/json")
	else:
		return HttpResponse((json.dumps('ERROR' : 'Wrong request method')), content_type="application/json")
		
	
def read(request):
	data = request.POST
	ver_id=data.get('version_id')
		
	return HttpResponse((), content_type="application/json")

	
def update(request):
	pass


def delete(request):
	pass


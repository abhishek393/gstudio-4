from .models.node import Node
from django.http import HttpResponse
import json

def create(request):
    """This function receives a request from the Client,
        fetches the fields provided in the request body and 
        then creates a Node object.The created Node object after 
        being converted into JSON file is indexed in the ElasticSearch server """
    if request.method == 'POST':
        data = request.POST
        node_obj = Node(
            name=data.get('name'),
            created_at=data.get('created_at'),
            created_by=data.get('created_by'),
            last_update=data.get('last_update'))
        # TODO: Integrate RCS when creating a node object.
        result = node_obj.create()
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return HttpResponse(
            json.dumps({'ERROR': 'Wrong request method'}), content_type='application/json')


def read(request):
    """This function receives a request, uses ElasticSearch to find 
        the corresponding JSON object and returns the JSON object found"""
    return Node.read(request.POST)


def update(request):
    """This function receives a request and uses ElasticSearch to find 
        the corresponding object and then updates the respective fields"""
    return Node.update(request.POST)


def delete(request):
    """This function receives a request and uses ElasticSearch to find 
        all the files that matches the criteria and then removes them from ElasticSearch server"""
    return Node.delete(request.POST)

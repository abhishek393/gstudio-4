from .models.node import Node
from django.http import HttpResponse
import json
import datetime

def create(request):
    """This function receives a request from the Client,
        fetches the fields provided in the request body and
        then creates a Node object.The created Node object after
        being converted into JSON file is indexed in the ElasticSearch server.
        """
    if request.method == 'POST':
        data = request.POST
        node_obj = Node(
            name=data.get('name'),
            created_by=data.get('created_by'),
            altnames=data.get('altnames'),
            plural=data.get('plural'),
            language=data.get('language'),
            access_policy=data.get('access_policy'),
            modified_by=data.get('modified_by'))
        result = node_obj.create()
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return HttpResponse(
            json.dumps({'ERROR': 'Wrong request method'}), content_type='application/json')


def read(request):
    """This function receives a request, uses ElasticSearch to find
        the corresponding JSON object and returns the JSON object found.
        """
    return Node.read(request.POST)


def update(request):
    """This function receives a request and uses ElasticSearch to find
        the corresponding object and then updates the respective fields.
        """
    return Node.update(request.POST)


def delete(request):
    """This function receives a request and uses ElasticSearch to find
        all the files that matches the criteria and then removes them from ElasticSearch server.
        """
    return Node.delete(request.POST)

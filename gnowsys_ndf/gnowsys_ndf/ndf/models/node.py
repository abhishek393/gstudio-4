import json
from django.db import models
from django.http import HttpResponse
from elasticsearch import Elasticsearch

es = Elasticsearch()


class Node(models.Model):
    """The basic model for all objects."""
    name = models.CharField(max_length=50)
    created_at = models.CharField(max_length=50)
    created_by = models.CharField(max_length=30)
    last_update = models.CharField(max_length=50)

    def get_json(self):
        """Converts the object into json."""
        json_rep = {}
        json_rep['name'] = self.name
        json_rep['created_at'] = self.created_at
        json_rep['created_by'] = self.created_by
        json_rep['last_update'] = self.last_update
        return json.dumps(json_rep)

    def create(self):
        """Docstring to be added."""
        try:
            self.create.version_id += 1
        except AttributeError:
            self.create.version_id = 0
        json_data = self.get_json()
        result = es.index(index="data", doc_type='node', id=self.create.version_id, body=json_data)
        return result

    @staticmethod
    def read(data):
        """Docstring to be added."""
        data_dict = dict(data)
        json_query = {}
        for key in data_dict.keys():
            json_query[key] = data_dict[key][0]
        searched_data = es.search(index='data', doc_type='node', body={'query': {'match': json_query}})
        return HttpResponse(json.dumps(searched_data), content_type='application/json')

    @staticmethod
    def update(data):
        """Docstring to be added."""
        data_dict = dict(data)
        json_query = {}
        for key in data_dict.keys():
            json_query[key] = data_dict[key][0]
        key_2 = json_query.keys()[0]
        value = json_query[key_2]
        searched_list = value.split(',')
        reqd_dict = {}
        update_dict = {}

        reqd_dict[key_2] = searched_list[0]
        update_dict[key_2] = searched_list[1]
        searched_data = es.search(index='data', doc_type='node', body={'query': {'match': reqd_dict}})
        reqd_id = []
        for hit in searched_data['hits']['hits']:
            reqd_id.append(hit['_id'])
        i = 0
        for z in reqd_id:
            searched_data['hits']['hits'][i]['_source'][key_2] = searched_list[1]
            res = es.index(
                index="data",
                doc_type='node',
                id=int(z),
                body=searched_data['hits']['hits'][i]['_source'])
            i = i + 1
        return HttpResponse(json.dumps({'SUCCESS': 'SUCCESS'}), content_type='application/json')

    @staticmethod
    def delete(data):
        """Docstring to be added."""
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

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
        """This function converts the Node object into a JSON file and indexes the JSON objects in the ElasticSearch server at the same instance so that it can be used by other operations. It returns a success or failure message depending on whether the operation is successful."""
        try:
            self.create.version_id += 1
        except AttributeError:
            self.create.version_id = 0
        json_data = self.get_json()
        result = es.index(index="data", doc_type='node', id=self.create.version_id, body=json_data)
        return result

    @staticmethod
    def read(data):
        """This function receives a search query from the Client. It then fetches the search query and uses ElasticSearch to find the corresponding JSON object. The Read function then returns the JSON object found.
"""
        data_dict = dict(data)
        json_query = {}
        for key in data_dict.keys():
            json_query[key] = data_dict[key][0]
        searched_data = es.search(index='data', doc_type='node', body={'query': {'match': json_query}})
        return HttpResponse(json.dumps(searched_data), content_type='application/json')

    @staticmethod
    def update(data):
        """This function receives the field to be modified or updated,as { Key: Value } pairs from the Client.It then uses ElasticSearch to find the corresponding object and then updates the respective field. It returns a success or failure message depending on whether the operation is successful.
 """
        data_dict = dict(data)
        json_query = {}
        for key in data_dict.keys():
            json_query[key] = data_dict[key][0]
        json_query_key = json_query.keys()[0]
        value = json_query[json_query_key]
        searched_list = value.split(',')
        reqd_dict = {}
        reqd_dict[json_query_key] = searched_list[0]
        searched_data = es.search(index='data', doc_type='node', body={'query': {'match': reqd_dict}})
        searched_data_ids = []
        for hit in searched_data['hits']['hits']:
            searched_data_ids.append(hit['_id'])
        for counter,data_id in enumerate(searched_data_ids,0):
            searched_data['hits']['hits'][i]['_source'][json_query_key] = searched_list[1]
            res = es.index(
                index="data",
                doc_type='node',
                id=int(data_id),
                body=searched_data['hits']['hits'][counter]['_source'])
        return HttpResponse(json.dumps({'SUCCESS': 'SUCCESS'}), content_type='application/json')

    @staticmethod
    def delete(data):
        """This function receives a criteria for which the JSON object has to be deleted, as { Key: Value } pairs. It uses ElasticSearch server to find all the files which match the criteria and then deletes it from the ElasticSearch index. It returns a success or failure message depending on whether the operation is successful"""
        data_dict = dict(data)
        json_query = {}
        for key in data_dict.keys():
            json_query[key] = data_dict[key][0]
        searched_data = es.search(index='data', doc_type='node', body={'query': {'match': json_query}})
        searched_data_ids = []
        for hit in searched_data['hits']['hits']:
            searched_data_ids.append(hit['_id'])
        for data_id in searched_data_ids:
            res = es.delete(index="data", doc_type='node', id= int(data_id))
        return HttpResponse(json.dumps({'SUCCESS': 'SUCCESS'}), content_type='application/json')

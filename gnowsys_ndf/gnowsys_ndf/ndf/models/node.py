import json
import uuid
from django.db import models
from django.http import HttpResponse,HttpRequest
from elasticsearch import Elasticsearch
#from past.builtins import basestring # pip install future
#from future.utils import python_2_unicode_compatible
import datetime

es = Elasticsearch()

class Node(models.Model):
    '''Everything is a Node.  Other classes should inherit this Node class.

    According to the specification of GNOWSYS, all nodes, including
    types, metatypes and members of types, edges of nodes, should all
    be Nodes.

    Member of this class must belong to one of the NODE_TYPE_CHOICES.

    Some in-built Edge names (Relation types) are defined in this
    class: type_of, member_of, prior_node, post_node, collection_set,
    group_set.

    type_of is used to express generalization of Node. And member_of
    to express its type. This type_of should not be confused with
    _type.  The latter expresses the Python classes defined in this
    program that the object inherits.  The former (type_of) is about
    the data the application represents.

    _type is useful in seggregating the nodes from the mongodb
    collection, where all nodes are stored.

    prior_node is to express that the current node depends in some way
    to another node/s.  post_node is seldom used.  Currently we use it
    to define sub-Group, and to set replies to a post in the Forum App.

    Nodes are publisehed in one group or another, or in more than one
    group. The groups in which a node is publisehed is expressed in
    group_set.'''
    objects = models.Manager()
    collection_name = 'Nodes'
    structure = {
        '_type': str, # check required: required field, Possible
                          # values are to be taken only from the list
                          # NODE_TYPE_CHOICES
        'name': str,
        'altnames': str,
        'plural': str,
        'prior_node': [uuid.UUID],
        'post_node': [uuid.UUID],

        # 'language': unicode, # previously it was unicode.
        'language': (str, str), # Tuple are converted into a simple list
        'type_of': [uuid.UUID], # check required: only ObjectIDs of GSystemType
        'member_of': [uuid.UUID], # check required: only ObjectIDs of
                                 # GSystemType for GSystems, or only
                                 # ObjectIDs of MetaTypes for
                                 # GSystemTypes
        'access_policy': str, # check required: only possible
                                  # values are Public or Private.  Why
                                  # is this unicode?

      	'created_at': datetime.datetime,
        'created_by': int, # test required: only ids of Users

        'last_update': datetime.datetime,
        'modified_by': int, # test required: only ids of Users

        'contributors': [int], # test required: set of all ids of
                               # Users of created_by and modified_by
                               # fields
        'location': [dict], # check required: this dict should be a
                            # valid GeoJason format
        'content': str,
        'content_org': str,

        'group_set': [uuid.UUID], # check required: should not be
                                 # empty. For type nodes it should be
                                 # set to a Factory Group called
                                 # Administration
        'collection_set': [uuid.UUID],  # check required: to exclude
                                       # parent nodes as children, use
                                       # MPTT logic
        'property_order': [],  # Determines the order & grouping in
                               # which attribute(s)/relation(s) are
                               # displayed in the form

        'start_publication': datetime.datetime,
        'tags': [str],
        'featured': bool,
        'url': str,
        'comment_enabled': bool,
      	'login_required': bool,
      	# 'password': basestring,

        #'status': STATUS_CHOICES_TU,
        'rating':[{'score':int,
                   'user_id':int,
                   'ip_address':str}],
        'snapshot':dict
    }

    required_fields = ['name', '_type', 'created_by'] # 'group_set' to be included
                                        # here after the default
                                        # 'Adminiation' group is
                                        # ready.
    default_values = {
                        'name': u'',
                        'altnames': u'',
                        'plural': u'',
                        'prior_node': [],
                        'post_node': [],
                        'language': ('en', 'English'),
                        'type_of': [],
                        'member_of': [],
                        'access_policy': u'PUBLIC',
                        'created_at': datetime.datetime.now,
                        # 'created_by': int,
                        'last_update': datetime.datetime.now,
                        # 'modified_by': int,
                        # 'contributors': [],
                        'location': [],
                        'content': u'',
                        'content_org': u'',
                        'group_set': [],
                        'collection_set': [],
                        'property_order': [],
                        # 'start_publication': datetime.datetime.now,
                        'tags': [],
                        # 'featured': True,
                        'url': u'',
                        # 'comment_enabled': bool,
                        # 'login_required': bool,
                        # 'password': basestring,
                        'status': u'PUBLISHED',
                        'rating':[],
                        'snapshot':{}
                    }

    validators = {
        'name': lambda x: x.strip() not in [None, ''],
        'created_by': lambda x: isinstance(x, int) and (x != 0),
        'access_policy': lambda x: x in (list(NODE_ACCESS_POLICY) + [None])
    }

    use_dot_notation = True

    """The basic model for all objects."""
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=30)
    last_update = models.DateTimeField()
    altnames = models.CharField(max_length=50)
    plural = models.CharField(max_length=30)
    language = models.CharField(max_length=50)
    access_policy = models.CharField(max_length=50) 
    modified_by = models.CharField(max_length=30)
    object_id = models.CharField(max_length=64)

    def get_json(self):
        """Converts the object into json."""
        json_rep = {}
        json_rep['name'] = self.name
        json_rep['created_at'] = str(self.created_at)
        json_rep['created_by'] = self.created_by
        json_rep['last_update'] = str(self.last_update)
        json_rep['altnames'] = self.altnames
        json_rep['plural'] = self.plural
        json_rep['language'] = self.language
        json_rep['access_policy'] = self.access_policy
        json_rep['modified_by'] = self.modified_by
        json_rep['object_id'] = self.object_id
        return json.dumps(json_rep)

    def __get_id(self):
        """This function creates a unique ID of a Node object."""
        self.object_id = str(uuid.uuid4())

    def create(self):
        """This function converts the Node object into a JSON file and
            indexes the JSON objects in the ElasticSearch server at the
            same instance so that it can be used by other operations.
            It returns a success or failure message depending on whether
            the operation is successful."""
        self.last_update = self.created_at = datetime.datetime.now()
        self.__get_id()
        json_data = self.get_json()
        result = es.index(index="data", doc_type='node', id=self.object_id, body=json_data)
        return result

    @staticmethod
    def read(data):
        """This function receives a search query from the Client.
            It then fetches the search query and uses ElasticSearch to find
            the corresponding JSON object. The Read function then returns
            the JSON object found."""
        data_dict = dict(data)
        json_query = {}
        for key in data_dict.keys():
            json_query[key] = data_dict[key][0]
        searched_data = es.search(
            index='data', doc_type='node', body={'query': {'match': json_query}})
        return HttpResponse(json.dumps(searched_data), content_type='application/json')

    @staticmethod
    def update(data):
        """This function receives the field to be modified or updated,
            as { Key: Value } pairs from the Client.It then uses ElasticSearch
            to find the corresponding object and then updates the respective field.
            It returns a success or failure message depending on whether the
            operation is successful."""
        data_dict = dict(data)
        json_query = {}
        for key in data_dict.keys():
            json_query[key] = data_dict[key][0]
        json_query_keys = list(json_query)
        value = json_query[json_query_keys[0]]
        searched_list = value.split(',')
        reqd_dict = {}
        reqd_dict[json_query_keys[0]] = searched_list[0]
        searched_data = es.search(
            index='data', doc_type='node', body={'query': {'match': reqd_dict}})
        searched_data_ids = []
        for hit in searched_data['hits']['hits']:
            searched_data_ids.append(hit['_id'])
        for counter, data_id in enumerate(searched_data_ids):
            searched_data['hits']['hits'][counter]['_source'][json_query_keys[0]] = searched_list[1]
            searched_data['hits']['hits'][counter]['_source']['last_update'] = str(datetime.datetime.now())
            res = es.index(
                index="data",
                doc_type='node',
                id=data_id,
                body=searched_data['hits']['hits'][counter]['_source'])
        if res:
            return HttpResponse(json.dumps({'SUCCESS':'SUCCESS'}), content_type='application/json')

    @staticmethod
    def delete(data):
        """This function receives a criteria for which the JSON object has to be deleted,
            as { Key: Value } pairs. It uses ElasticSearch server to find all the files
            which match the criteria and then deletes it from the ElasticSearch index.
            It returns a success or failure message depending on whether
            the operation is successful"""
        data_dict = dict(data)
        json_query = {}
        for key in data_dict.keys():
            json_query[key] = data_dict[key][0]
        searched_data = es.search(
            index='data', doc_type='node', body={'query': {'match': json_query}})
        searched_data_ids = []
        for hit in searched_data['hits']['hits']:
            searched_data_ids.append(hit['_id'])
        for data_id in searched_data_ids:
            res = es.delete(index="data", doc_type='node', id=data_id)
        if res:
            return HttpResponse(json.dumps({'SUCCESS': 'SUCCESS'}), content_type='application/json')
    
    # custom methods provided for Node class
    def fill_node_values(self, request=HttpRequest(), **kwargs):

        user_id = kwargs.get('created_by', None)
        # dict to sum both dicts, kwargs and request.POST
        values_dict = {}
        if request:
            if request.POST:
                values_dict.update(request.POST.dict())
            if (not user_id) and request.user:
                user_id = request.user.id
        # adding kwargs dict later to give more priority to values passed via kwargs.
        values_dict.update(kwargs)

        # handling storing user id values.
        if user_id:
            if not self['created_by'] and ('created_by' not in values_dict):
                # if `created_by` field is blank i.e: it's new node and add/fill user_id in it.
                # otherwise escape it (for subsequent update/node-modification).
                values_dict.update({'created_by': user_id})
            if 'modified_by' not in values_dict:
                values_dict.update({'modified_by': user_id})
            if 'contributors' not in values_dict:
                values_dict.update({'contributors': add_to_list(self.contributors, user_id)})

        if 'member_of' in values_dict  and not isinstance(values_dict['member_of'], uuid.UUID):
            from gsystem_type import GSystemType
            gst_node = GSystemType.get_gst_name_id(values_dict['member_of'])
            if gst_node:
                values_dict.update({'member_of': uuid.UUID(gst_node[1])})

        # filter keys from values dict there in node structure.
        node_str = Node.structure
        node_str_keys_set = set(node_str.keys())
        values_dict_keys_set = set(values_dict.keys())

        for each_key in values_dict_keys_set.intersection(node_str_keys_set):
            temp_prev_val = self[each_key]
            # checking for proper casting for each field
            if isinstance(node_str[each_key], type):
                node_str_data_type = node_str[each_key].__name__
            else:
                node_str_data_type = node_str[each_key]
            casted_new_val = cast_to_data_type(values_dict[each_key], node_str_data_type)
            # check for uniqueness and addition of prev values for dict, list datatype values
            self[each_key] = casted_new_val
        return self

    @staticmethod
    def get_node_by_id(node_id):
        '''
            Takes ObjectId or objectId as string as arg
                and return object
        '''
        if node_id and (isinstance(node_id, uuid.UUID)):
            return node_collection.one({'_id': uuid.UUID(node_id)})
        else:
            # raise ValueError('No object found with id: ' + str(node_id))
            return None

    @staticmethod
    def get_nodes_by_ids_list(node_id_list):
        '''
            Takes list of ObjectIds or objectIds as string as arg
                and return list of object
        '''
        try:
            node_id_list = map(uuid.UUID, node_id_list)
        except:
            node_id_list = [uuid.UUID(nid) for nid in node_id_list if nid]
        if node_id_list:
            return node_collection.find({'_id': {'$in': node_id_list}})
        else:
            return None


    @staticmethod
    def get_node_obj_from_id_or_obj(node_obj_or_id, expected_type):
        # confirming arg 'node_obj_or_id' is Object or oid and
        # setting node_obj accordingly.
        node_obj = None

        if isinstance(node_obj_or_id, expected_type):
            node_obj = node_obj_or_id
        elif isinstance(node_obj_or_id, uuid.UUID):
            node_obj = node_collection.one({'_id': uuid.UUID(node_obj_or_id)})
        else:
            # error raised:
            raise RuntimeError('No Node class instance found with provided arg for get_node_obj_from_id_or_obj(' + str(node_obj_or_id) + ', expected_type=' + str(expected_type) + ')')

        return node_obj

    def type_of_names_list(self, smallcase=False):
        """Returns a list having names of each type_of (GSystemType, i.e Wiki page,
        Blog page, etc.), built from 'type_of' field (list of ObjectIds)
        """
        type_of_names = []
        if self.type_of:
            node_cur = node_collection.find({'_id': {'$in': self.type_of}})
            if smallcase:
                type_of_names = [node.name.lower() for node in node_cur]
            else:
                type_of_names = [node.name for node in node_cur]

        return type_of_names


    @staticmethod
    def get_name_id_from_type(node_name_or_id, node_type, get_obj=False):
        '''
        e.g:
            Node.get_name_id_from_type('pink-bunny', 'Author')
        '''
        if not get_obj:
            # if cached result exists return it

            slug = slugify(node_name_or_id)
            cache_key = node_type + '_name_id' + str(slug)
            cache_result = cache.get(cache_key)

            if cache_result:
                # todo:  return OID after casting
                return (cache_result[0], uuid.UUID(cache_result[1]))
            # ---------------------------------

        node_id = uuid.UUID(node_name_or_id) if isinstance(node_name_or_id, uuid.UUID) else None
        node_obj = node_collection.one({
                                        "_type": {"$in": [
                                                # "GSystemType",
                                                # "MetaType",
                                                # "RelationType",
                                                # "AttributeType",
                                                # "Group",
                                                # "Author",
                                                node_type
                                            ]},
                                        "$or":[
                                            {"_id": node_id},
                                            {"name": str(node_name_or_id)}
                                        ]
                                    })

        if node_obj:
            node_name = node_obj.name
            node_id = node_obj._id

            # setting cache with ObjectId
            cache_key = node_type + '_name_id' + str(slugify(node_id))
            cache.set(cache_key, (node_name, node_id), 60 * 60)

            # setting cache with node_name
            cache_key = node_type + '_name_id' + str(slugify(node_name))
            cache.set(cache_key, (node_name, node_id), 60 * 60)

            if get_obj:
                return node_obj
            else:
                return node_name, node_id

        if get_obj:
            return None
        else:
            return None, None


    def get_tree_nodes(node_id_or_obj, field_name, level, get_obj=False):
        '''
        node_id_or_obj: root node's _id or obj
        field_name: It can be either of collection_set, prior_node
        level: starts from 0
        '''
        node_obj = Node.get_node_obj_from_id_or_obj(node_id_or_obj, Node)
        nodes_ids_list = node_obj[field_name]
        while level:
           nodes_ids_cur = Node.get_nodes_by_ids_list(nodes_ids_list)
           nodes_ids_list = []
           if nodes_ids_cur:
               [nodes_ids_list.extend(i[field_name]) for i in nodes_ids_cur]
           level = level - 1

        if get_obj:
            return Node.get_nodes_by_ids_list(nodes_ids_list)

        return nodes_ids_list

    ########## Setter(@x.setter) & Getter(@property) ##########
    @property
    def member_of_names_list(self):
        """Returns a list having names of each member (GSystemType, i.e Page,
        File, etc.), built from 'member_of' field (list of ObjectIds)

        """
        from gsystem_type import GSystemType
        return [GSystemType.get_gst_name_id(gst_id)[0] for gst_id in self.member_of]


    @property
    def group_set_names_list(self):
        """Returns a list having names of each member (Group name),
        built from 'group_set' field (list of ObjectIds)

        """
        from group import Group
        return [Group.get_group_name_id(gr_id)[0] for gr_id in self.group_set]


    @property
    def user_details_dict(self):
        """Retrieves names of created-by & modified-by users from the given
        node, and appends those to 'user_details' dict-variable

        """
        user_details = {}
        if self.created_by:
            user_details['created_by'] = User.objects.get(pk=self.created_by).username

        contributor_names = []
        for each_pk in self.contributors:
            contributor_names.append(User.objects.get(pk=each_pk).username)
        user_details['contributors'] = contributor_names

        if self.modified_by:
            user_details['modified_by'] = User.objects.get(pk=self.modified_by).username

        return user_details


    @property
    def prior_node_dict(self):
        """Returns a dictionary consisting of key-value pair as
        ObjectId-Document pair respectively for prior_node objects of
        the given node.

        """

        obj_dict = {}
        i = 0
        for each_id in self.prior_node:
            i = i + 1

            if each_id != self._id:
                node_collection_object = node_collection.one({"_id": uuid.UUID(each_id)})
                dict_key = i
                dict_value = node_collection_object

                obj_dict[dict_key] = dict_value

        return obj_dict

    @property
    def collection_dict(self):
        """Returns a dictionary consisting of key-value pair as
        ObjectId-Document pair respectively for collection_set objects
        of the given node.

        """

        obj_dict = {}

        i = 0;
        for each_id in self.collection_set:
            i = i + 1

            if each_id != self._id:
                node_collection_object = node_collection.one({"_id": uuid.UUID(each_id)})
                dict_key = i
                dict_value = node_collection_object

                obj_dict[dict_key] = dict_value

        return obj_dict

    @property
    def html_content(self):
        """Returns the content in proper html-format.

        """
        if MARKUP_LANGUAGE == 'markdown':
            return markdown(self.content, MARKDOWN_EXTENSIONS)
        elif MARKUP_LANGUAGE == 'textile':
            return textile(self.content)
        elif MARKUP_LANGUAGE == 'restructuredtext':
            return restructuredtext(self.content)
        return self.content

    @property
    def current_version(self):
        history_manager = HistoryManager()
        return history_manager.get_current_version(self)

    @property
    def version_dict(self):
        """Returns a dictionary containing list of revision numbers of the
        given node.

        Example:
        {
         "1": "1.1",
         "2": "1.2",
         "3": "1.3",
        }

        """
        history_manager = HistoryManager()
        return history_manager.get_version_dict(self)

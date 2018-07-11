# gstudio-3
A Python 3.6 and Django 2.0 port of the Node Description Framework used in GStudio.

## About the project:
This project follows the same directory structure as the presently-in-use [ndf app](https://github.com/gnowledge/gstudio/tree/master/gnowsys-ndf/gnowsys_ndf/ndf).
It uses the latest stable versions of all technologies -- Python 3.6+, Django 2.0 and Elasticsearch 6.2.4.
It is essentially a graph database and is powered by an indexing system, provided by Elasticsearch and a file system which uses a revision control system (RCS). All Mongo-related dependencies have been completely removed. The file system itself is used as a database.

## Functionality:
The app includes the four basic CRUD operations:
1. Create
2. Read
3. Update
4. Delete

In the [models](https://github.com/apb7/gstudio-3/tree/master/gnowsys_ndf/gnowsys_ndf/ndf/models) directory, the basic [node](https://github.com/apb7/gstudio-3/tree/master/gnowsys_ndf/gnowsys_ndf/ndf/models/node.py) has been placed.
The CRUD operations have been implemented in this basic node model. All processing pertaining to the operations as well as elasticsearch has been done in this file.

Each of these operations in [`node.py`](https://github.com/apb7/gstudio-3/tree/master/gnowsys_ndf/gnowsys_ndf/ndf/models/node.py) override a function with the same name in [`views.py`](https://github.com/apb7/gstudio-3/tree/master/gnowsys_ndf/gnowsys_ndf/ndf/views.py). The functions defined in views call the corresponding function in the node model.

To run the framework, each operation also requires an API endpoint to be exposed. This has been done in the [urls](https://github.com/apb7/gstudio-3/tree/master/gnowsys_ndf/gnowsys_ndf/ndf/urls.py) file.

### API documentation:
1. Create:
Query:
`POST /ndf/create/`

```json
{
    "name": "MICHAEL",
    "created_by": "BOT",
    "altnames": "MIKE",
    "plural": "MANAGERS",
    "language": "EN",
    "access_policy": "PUBLIC",
    "modified_by": "BOT"
}
```

The result of the above operation is:

```json
{
    "_type": "node",
    "result": "created",
    "_id": "9b8fdc58-0844-47e0-bb5a-dba110d6353c",
    "_index": "data",
    "_primary_term": 4,
    "_version": 1,
    "_shards": {
        "total": 2,
        "failed": 0,
        "successful": 1
    },
    "_seq_no": 4
}
```

The `_shards` header provides information about the replication process of the index operation.

`total` - Indicates to how many shard copies (primary and replica shards) the index operation should be executed on.  
`successful` - Indicates the number of shard copies the index operation succeeded on.  
`failed` - An array that contains replication related errors in the case an index operation failed on a replica shard.  
The index operation is successful in the case `successful` is at least 1.  

2. Read:
Query: `POST /ndf/read/`

```json
{
    "object_id": "9b8fdc58-0844-47e0-bb5a-dba110d6353c"
}
```

The result of the above operation is:

```json
{
    "timed_out": false,
    "_shards": {
        "total": 5,
        "failed": 0,
        "skipped": 0,
        "successful": 5
    },
    "took": 222,
    "hits": {
        "total": 1,
        "max_score": 1.4384104,
        "hits": [
            {
                "_index": "data",
                "_type": "node",
                "_score": 1.4384104,
                "_source": {
                    "altnames": "MIKE",
                    "name": "MICHEAL",
                    "modified_by": "BOT",
                    "plural": "MANAGERS",
                    "object_id": "9b8fdc58-0844-47e0-bb5a-dba110d6353c",
                    "language": "EN",
                    "created_by": "BOT",
                    "created_at": "2018-07-11 13:26:29.465566",
                    "last_update": "2018-07-11 13:26:29.465566",
                    "access_policy": "PUBLIC"
                },
                "_id": "9b8fdc58-0844-47e0-bb5a-dba110d6353c"
            }
        ]
    }
}
```

3. Update:
Query: `POST /ndf/update/`

```json
{
    "access_policy": "PUBLIC,PRIVATE"
}
```

The result of the above operation is:

```json
{
    "SUCCESS": "SUCCESS"
}
```

The `SUCCESS` message only appears when the update operation is completed. This can be verified by the read operation query:

Query: `POST /ndf/read/`

```json
{
    "object_id": "9b8fdc58-0844-47e0-bb5a-dba110d6353c"
}
```

The result of the above query is:

```json
{
    "timed_out": false,
    "_shards": {
        "total": 5,
        "failed": 0,
        "skipped": 0,
        "successful": 5
    },
    "took": 23,
    "hits": {
        "total": 1,
        "max_score": 1.4384104,
        "hits": [
            {
                "_index": "data",
                "_type": "node",
                "_score": 1.4384104,
                "_source": {
                    "altnames": "MIKE",
                    "name": "MICHEAL",
                    "modified_by": "BOT",
                    "plural": "MANAGERS",
                    "object_id": "9b8fdc58-0844-47e0-bb5a-dba110d6353c",
                    "created_by": "BOT",
                    "created_at": "2018-07-11 13:26:29.465566",
                    "last_update": "2018-07-11 13:42:24.568822",
                    "access_policy": "PRIVATE",
                    "language": "EN"
                },
                "_id": "9b8fdc58-0844-47e0-bb5a-dba110d6353c"
            }
        ]
    }
}
```

As you can see, the `access_policy` field has now been changed to `PRIVATE`.

4. Delete:
Query: `POST /ndf/delete`

```json
{
    "SUCCESS": "SUCCESS"
}
```

The `SUCCESS` message only appears when the operation is successful. This can be verified by trying to read the same node object:

Query: `POST /ndf/read/`

```json
{
    "object_id": "9b8fdc58-0844-47e0-bb5a-dba110d6353c"
}
```

The result of the above query is:

```json
{
    "timed_out": false,
    "_shards": {
        "total": 5,
        "failed": 0,
        "skipped": 0,
        "successful": 5
    },
    "took": 12,
    "hits": {
        "total": 0,
        "max_score": null,
        "hits": []
    }
}
```

As you can see, the `hits` field is now empty, which indicates that there are no node objects with the given `object_id`.

## Future work to be done:

1. Integrate the `history_manager` with the models and elasticsearch server.

2. Add more models to the `models` directory.

3. Increase the test coverage to around 100% for the codebase. This is an important step to release this app as an independent PyPI package.

## Team:
Abhishek -- [@abhishek393](https://github.com/abhishek393)  
Apurv -- [@apb7](https://github.com/apb7)  
Vikram -- [@vickysingh17](https://github.com/vickysingh17)  

## References:
#### Source code for MongoDB ObjectId:
Source code [MongoDB](http://mongodb.github.io/node-mongodb-native/2.0/tutorials/objectid/)

#### ObjectId:
MonoDB's ObjectId documentation can be found [here](https://docs.mongodb.com/manual/reference/method/ObjectId/).  
The documentation for `is_valid` method of ObjectId can be found [here](https://stackoverflow.com/questions/28774526/how-to-check-that-mongo-objectid-is-valid-in-python?rq=1).  
[No replacement](https://github.com/ramsey/uuid/issues/178) of `is_valid` method exists for UUID.

#### Postman:
This is the [documentation](https://www.getpostman.com/docs/v6/postman/sending_api_requests/requests) for sending API requests via the Postman framework.

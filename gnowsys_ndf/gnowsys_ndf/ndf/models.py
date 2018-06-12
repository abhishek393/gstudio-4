from __future__ import unicode_literals

import json
from django.db import models

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

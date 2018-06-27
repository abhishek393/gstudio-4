from models.node import Node


def create(request):
    """Docstring to be added."""
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
    """Docstring to be added."""
    return Node.read(request.POST)


def update(request):
    """Docstring to be added."""
    return Node.update(request.POST)


def delete(request):
    """Docstring to be added."""
    return Node.delete(request.POST)

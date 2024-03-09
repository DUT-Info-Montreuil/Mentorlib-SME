addCourse = {
    'type': 'object',
    'properties' : {
        "description": { 'type': 'string' },
        "resource_id": { 'type': 'integer' },
        "date" : { 'formet': 'date'},
        "duration" : { 'type': 'integer' },
        "remote" : { 'type': 'boolean' }
    },
    'required': ['resource_id', 'date', 'remote', 'duration']
}

askCourse = {
    'type': 'object',
    'properties' : {
        "resourceId": { 'type': 'integer' },
        "description": { 'type': 'string' },
        "date" : { 'format': 'date'},
        "duration" : { 'type': 'integer' },
        "remote" : { 'type': 'boolean' },
    },
    'required': ['resource_id', 'date', 'remote', 'duration']
}
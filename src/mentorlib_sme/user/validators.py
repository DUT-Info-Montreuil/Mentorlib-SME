userlogin = {
    "type": "object",
    "properties": {"email": {"type": "string"}, "password": {"type": "string"}},
    "required": ["email", "password"],
}

userregister = {
    'type':'object',
    'properties':{
        "email": { 'type': 'string' },
        "password": { 'type': 'string' },
        "firstname": { 'type': 'string' },
        "lastname": { 'type': 'string' },
    },
    'required': ['email', 'password', 'firstname', 'lastname']
}

userupdate = {
    "type": "object",
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "student_year": {"type": "integer"},
    },
    "required": ["firstname", "lastname", "email", "password", "student_year"],
}

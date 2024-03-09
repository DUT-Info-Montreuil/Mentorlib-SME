userlogin = {
    "type": "object",
    "properties": {"email": {"type": "string"}, "password": {"type": "string"}},
    "required": ["email", "password"],
}

userupdate = {
    "type": "object",
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "email": {"type": "string"},
        "student_year": {"type": "integer"},
    },
    "required": ["firstname", "lastname", "email", "student_year"],
}

userupdatepassword = {
    "type": "object",
    "properties": {
        "old_password": {"type": "string"},
        "new_password": {"type": "string"},
    },
    "required": ["old_password", "new_password"],
}

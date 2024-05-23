from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True)
    student_year = fields.Int(required=True)
    is_mentor = fields.Bool(dump_only=True)
    is_admin = fields.Bool(dump_only=True)

class UserNoteSchema(Schema):
    id = fields.Int(dump_only=True)
    resource_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    mentor_id = fields.Int(required=True)
    note = fields.Str(required=True)
    date = fields.DateTime(dump_only=True)

    mentor = fields.Nested(UserSchema, only=["id", "firstname", "lastname", "email", "student_year"])
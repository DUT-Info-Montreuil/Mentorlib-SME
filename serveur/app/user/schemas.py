from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    public_id = fields.Str(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    student_year = fields.Int(required=True)
    date_created = fields.DateTime(dump_only=True)
    is_mentor = fields.Bool(dump_only=True)
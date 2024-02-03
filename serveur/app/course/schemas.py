from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

from app.course.models import Course, AskedCourse, Resource, CourseRegisteredUser
from app.user.schemas import UserSchema

class ResourceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Resource
        include_relationships = True
        load_instance = True
class CourseSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Course
        include_fk = True
        load_instance = True

    resource = fields.Nested(ResourceSchema)
    user = fields.Nested(UserSchema)

class AskedCourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AskedCourse

class CourseRegisteredUserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CourseRegisteredUser
        include_relationships = True
        load_instance = True

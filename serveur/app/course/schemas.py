from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, fields

from app.course.models import Course, AskedCourse, Resource

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


class AskedCourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AskedCourse
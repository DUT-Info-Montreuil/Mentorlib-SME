from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,fields

from mentorlib_sme.course.models import Course, AskedCourse, Resource, CourseRegisteredUser
from mentorlib_sme.user.schemas import UserSchema

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

    resource = fields.Nested(ResourceSchema, exclude=("courses",))
    user = fields.Nested(UserSchema)
    course_registered_users = fields.Nested("CourseRegisteredUserSchema", many=True)

class AskedCourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AskedCourse
        include_fk = True
        load_instance = True

    resource = fields.Nested(ResourceSchema, exclude=("courses",))
    user = fields.Nested(UserSchema)

class CourseRegisteredUserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CourseRegisteredUser
        include_relationships = True
        load_instance = True

    user = fields.Nested(UserSchema)
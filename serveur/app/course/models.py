from app import db
from sqlalchemy.orm import backref
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    remote = db.Column(db.Boolean, default=False)

    resource = db.relationship("Resource", backref=backref("asked_course"))


class AskedCourse(db.Model):
    __tablename__ = 'asked_course'
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    duration = db.Column(db.Integer)
    remote = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved_date = db.Column(db.DateTime, default=None)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    year = db.Column(db.Integer)
class CourseRegisteredUser(db.Model):
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

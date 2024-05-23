from mentorlib_sme import db,Base
from sqlalchemy.orm import backref
from datetime import datetime
class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    remote = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(255))
    status = db.Column(db.Integer, default=0)
    
    resource = db.relationship("Resource", backref=backref("courses", lazy='dynamic'))
    user = db.relationship("User", back_populates="courses")
    course_registered_users = db.relationship('CourseRegisteredUser', back_populates='course')

class AskedCourse(Base):
    __tablename__ = 'asked_course'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    duration = db.Column(db.Integer)
    remote = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved_date = db.Column(db.DateTime, default=None)

    resource = db.relationship("Resource", backref=backref("asked_courses", lazy='dynamic'))
    user = db.relationship("User", back_populates="asked_courses")


class Resource(Base):
    __tablename__ = 'resource'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, default=0)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    semester = db.Column(db.Integer, default=1)
    banner = db.Column(db.String(255))


class CourseRegisteredUser(Base):
    __tablename__ = 'course_registered_user'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user_level = db.Column(db.Integer, default=0)

    course = db.relationship("Course", back_populates="course_registered_users")
    user = db.relationship("User", back_populates="course_registered_users")

class Comments(Base):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="comments")
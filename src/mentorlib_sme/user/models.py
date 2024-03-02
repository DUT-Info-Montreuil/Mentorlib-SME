from mentorlib_sme import db, Base

class User(Base):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(255))
    student_year = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_mentor = db.Column(db.Boolean, default=False)

    courses = db.relationship("Course", back_populates="user")
    asked_courses = db.relationship("AskedCourse", back_populates="user")
    course_registered_users = db.relationship("CourseRegisteredUser", back_populates="user")


class Mentor(Base):
    __tablename__ = 'mentor'

    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


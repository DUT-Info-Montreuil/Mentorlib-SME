from flask import jsonify, request, make_response, g, Blueprint
from mentorlib_sme import db, token_required
from sqlalchemy import and_
from flask_expects_json import expects_json, ValidationError
from mentorlib_sme.course.validators import askCourse
from mentorlib_sme.course.models import AskedCourse, Course, Resource
from mentorlib_sme.user.models import User
from mentorlib_sme.course.schemas import CourseSchema, ResourceSchema, AskedCourseSchema, CourseRegisteredUser

from copy import deepcopy

from datetime import datetime, timedelta

course_bp = Blueprint('course', __name__, url_prefix='/course')

@course_bp.route("/courses", methods=["GET"])
def all_courses():
    allCourses = db.session.query(Course)\
    .order_by(Course.date.desc())\
    .all()

    schema = CourseSchema(many=True)

    return jsonify(schema.dump(allCourses))

@course_bp.route("/<id>", methods=["GET"])
def course(id):
    allCourses = db.session.query(Course)\
    .filter_by(id = id)\
    .order_by(Course.date.desc())\
    .first()

    schema = CourseSchema(many=False)


    return jsonify(schema.dump(allCourses))

@course_bp.route("/mycourse", methods=["GET"])
@token_required
def my_course(f):
    allCourses = db.session.query(Course)\
    .filter_by(user_id = f.id)\
    .order_by(Course.date.desc())\
    .all()
    
    schema = CourseSchema(many=True)
    return jsonify(schema.dump(allCourses))


@course_bp.route("/ask", methods=['GET'])
@token_required
def asked_course(f):
    allAsked = db.session.query(AskedCourse).filter(AskedCourse.approved_date==None).all()
    schema = AskedCourseSchema(many=True)
    return jsonify(schema.dump(allAsked))

@course_bp.route("/ask", methods=["POST"])
@token_required
@expects_json(askCourse)
def ask_course(f):
    try:
        data = request.json
        askCourse = AskedCourse(
            resource_id = data['resource_id'],
            duration = data['duration'],
            remote = data['remote'],
            date = datetime.strptime(data['date'], '%d/%m/%Y %H:%M'),
            user_id = f.id
        )

        db.session.add(askCourse)
        db.session.commit()

        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error'}), 500)
    
@course_bp.route("/accept/<id>", methods=["POST"])
@token_required
def accept_course(f, id):
    try:
        askedCourse = db.session.query(AskedCourse)\
        .filter(and_(AskedCourse.id == id, AskedCourse.approved_date == None))\
        .first()

        if askedCourse:
            askedCourse.approved_date = datetime.now()
            db.session.commit()

            course = Course(
                resource_id = askedCourse.resource_id,
                user_id = f.id,
                date = askedCourse.date,
                duration = askedCourse.duration,
                remote = askedCourse.remote
            )
            db.session.add(course)
            db.session.commit()

            # Register the user to the course
            courseRegisteredUser = CourseRegisteredUser(
                course_id = course.id,
                user_id = askedCourse.user_id
            )
            db.session.add(courseRegisteredUser)
            db.session.commit()

        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'Error'}), 500)
    

@course_bp.route("/resource", methods=["GET"])
def resource():
    allResources = db.session.query(Resource) \
    .order_by(Resource.name.asc()) \
    .all()

    results = []
    for resource in allResources:
        val = deepcopy(resource.__dict__)
        del val['_sa_instance_state']
        results.append(val)

    return jsonify(results)

@course_bp.route("/register/<id>", methods=["POST"])
@token_required
def register_course(f, id):
    try:
        course = db.session.query(Course)\
        .filter_by(id = id)\
        .first()

        if course:
            courseRegisteredUser = db.session.query(CourseRegisteredUser)\
            .filter(and_(CourseRegisteredUser.course_id == id, CourseRegisteredUser.user_id == f.id))\
            .first()

            if not courseRegisteredUser:
                courseRegisteredUser = CourseRegisteredUser(
                    course_id = id,
                    user_id = f.id
                )
                db.session.add(courseRegisteredUser)
                db.session.commit()

        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'Error'}), 500)
    
@course_bp.route("/unregister/<id>", methods=["POST"])
@token_required
def unregister_course(f, id):
    try:
        courseRegisteredUser = db.session.query(CourseRegisteredUser)\
        .filter(and_(CourseRegisteredUser.course_id == id, CourseRegisteredUser.user_id == f.id))\
        .first()

        if courseRegisteredUser:
            db.session.delete(courseRegisteredUser)
            db.session.commit()

        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'Error'}), 500)
    

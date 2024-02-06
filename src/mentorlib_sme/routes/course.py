from flask import jsonify, request, make_response, g, Blueprint
from mentorlib_sme import db, token_required
from sqlalchemy import and_
from flask_expects_json import expects_json, ValidationError
from mentorlib_sme.course.validators import askCourse
from mentorlib_sme.course.models import AskedCourse, Course, Resource
from mentorlib_sme.user.models import User
from mentorlib_sme.course.schemas import CourseSchema, ResourceSchema, AskedCourseSchema

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
    allAsked = db.session.query(AskedCourse, Resource, User).join(Resource, AskedCourse.resource_id == Resource.id).join(User, AskedCourse.user_id == User.id).filter(AskedCourse.approved_date == None).all()
    results = []
    for askedCourse, resource, student in allAsked:
        val = deepcopy(askedCourse.__dict__)
        val["resource"] = {"name": resource.name, "year":resource.year}
        val["student"] = {"firstname": student.firstname or "Inconnu", "lastname":student.lastname or "Inconnu", "year": student.student_year}
        del val['_sa_instance_state']
        del val["resource_id"]
        del val["user_id"]
        results.append(val)

    return jsonify(results)

@course_bp.route("/ask", methods=["POST"])
@token_required
@expects_json(askCourse)
def ask_course(f):
    try:
        data = request.json
        askCourse = AskedCourse(
            resource_id = data['resourceId'],
            duration = data['duration'],
            remote = data['remote'],
            date = datetime.strptime(data['date'], '%d/%m/%Y %H:%M'),
            user_id = f.id
        )

        db.session.add(askCourse)
        db.session.commit()

        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        print(e)
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
                user_id = askedCourse.user_id,
                date = askedCourse.date,
                duration = askedCourse.duration,
                remote = askedCourse.remote
            )
            db.session.add(course)
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
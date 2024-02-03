from flask import jsonify, request, make_response, g
from app import app, db, token_required
from sqlalchemy import and_
from flask_expects_json import expects_json, ValidationError
from app.course.validators import askCourse
from app.course.models import AskedCourse, Course, Resource
from app.user.models import User
from app.course.schemas import CourseSchema, ResourceSchema, AskedCourseSchema

from copy import deepcopy

from datetime import datetime, timedelta

@app.route("/course", methods=["GET"])
def all_courses():
    allCourses = Course.query\
    .order_by(Course.date.desc())\
    .all()

    schema = CourseSchema(many=True)


    return jsonify(schema.dump(allCourses))

@app.route("/course/<id>", methods=["GET"])
def course(id):
    allCourses = Course.query\
    .filter_by(id = id)\
    .order_by(Course.date.desc())\
    .first()

    schema = CourseSchema(many=False)


    return jsonify(schema.dump(allCourses))

@app.route("/mycourse", methods=["GET"])
@token_required
def my_course(f):
    allCourses = Course.query\
    .filter_by(user_id = f.id)\
    .order_by(Course.date.desc())\
    .all()
    
    schema = CourseSchema(many=True)
    return jsonify(schema.dump(allCourses))


@app.route("/course/ask", methods=['GET'])
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

@app.route("/course/ask", methods=["POST"])
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
    
@app.route("/course/accept/<id>", methods=["POST"])
@token_required
def accept_course(f, id):
    try:
        askedCourse = AskedCourse.query.filter(and_(AskedCourse.id == id, AskedCourse.approved_date == None)).first()
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
    

@app.route("/resource", methods=["GET"])
def resource():
    allResources = Resource.query \
    .order_by(Resource.name.asc()) \
    .all()

    results = []
    for resource in allResources:
        val = deepcopy(resource.__dict__)
        del val['_sa_instance_state']
        results.append(val)

    return jsonify(results)

@app.route("/test", methods=['GET'])
def test():
    pass
    # course = Course(
    #     resource_id = 1,
    #     user_id = 1,
    #     date = datetime.now(),
    #     duration = 2,
    #     remote = False

    # )

    # db.session.add(course)
    # db.session.commit()
 
    
    # resource = Resource(
    #                 name = "R1.01 - Initiation au développement",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.02 - Développement d'interfaces web",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.03 - Introduction à l'Architecture des Ordinateurs",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.04 - Introduction aux Systèmes d'exploitation",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.05 - Introduction aux bases de données SQL",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.06 - Mathématiques Discrètes",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.07 - Outils Mathématiques Fondamentaux",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.08 - Gestion de projet et des organisations",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.09 - Économie durable et numérique",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.10 - Anglais Technique",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.11 - Bases de la Communication",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    
    # resource = Resource(
    #                 name = "R1.12 - Projet professionnel et personnel",
    #                 description = "",
    #                 year = 1
    #             )
    #             # insert user
    # db.session.add(resource)
    # db.session.commit()
    

    # return make_response(jsonify({'message': 'Success'}), 200)
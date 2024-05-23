from flask import jsonify, request, make_response, g, Blueprint
from mentorlib_sme import db, token_required, admin
from sqlalchemy import and_
from flask_expects_json import expects_json
from mentorlib_sme.course.validators import askCourse
from mentorlib_sme.course.models import AskedCourse, Course, Comments
from mentorlib_sme.user.models import User
from mentorlib_sme.course.schemas import CourseSchema, AskedCourseSchema, CourseRegisteredUser, CourseCommentSchema

from copy import deepcopy

from datetime import datetime, timedelta

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')


@comments_bp.route("/course/<id>", methods=["GET"])
@token_required
def get_course_comments(f, id):
    allCourseComments = db.session.query(Comments) \
    .order_by(Comments.date.desc()) \
    .filter_by(course_id=id) \
    .all()

    schema = CourseCommentSchema(many=True)

    return jsonify(schema.dump(allCourseComments))

@comments_bp.route("/course/<id>", methods=["POST"])
@token_required
def add_course_comment(f, id):
    try:
        data = request.json
        if not data['comment'] or data['comment'] == '':
            return make_response(jsonify({'message': 'Comment is required'}), 400)
        comment = Comments(
            course_id = id,
            user_id = f.id,
            comment = data['comment']
        )

        db.session.add(comment)
        db.session.commit()

        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'Error'}), 500)
    
@comments_bp.route("/course/<course_id>/<id>", methods=["DELETE"])
@token_required
def delete_course_comment(f, course_id, id):
    try:
        comment = db.session.query(Comments).filter_by(course_id=course_id, id=id).first()
        if not comment:
            return make_response(jsonify({'message': 'Comment not found'}), 404)
        db.session.delete(comment)
        db.session.commit()
        
        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'Error'}), 500)
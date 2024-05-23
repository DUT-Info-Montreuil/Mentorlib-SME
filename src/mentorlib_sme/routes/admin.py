from mentorlib_sme import app, db, token_required, admin
import uuid
from flask import jsonify, request, make_response, g, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from mentorlib_sme.user.models import User
from mentorlib_sme.course.models import Resource
from datetime import datetime, timedelta
from mentorlib_sme.user.schemas import UserSchema
from flask_expects_json import expects_json, ValidationError
from mentorlib_sme.user.validators import userlogin, userupdate, userregister

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route("/users", methods=["GET"])
@token_required
@admin
def all_users(f):
    allUsers = db.session.query(User).all()
    schema = UserSchema(many=True)
    return jsonify(schema.dump(allUsers))
    
#Admin
@admin_bp.route('/resource', methods=['PUT'])
@token_required
@admin
def add_resource(f):
    try:
        data = request.json
        resource = Resource(
            **data
        )

        db.session.add(resource)
        db.session.commit()

        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'Error'}), 500)


#Admin
@admin_bp.route('/resource/<id>', methods=['DELETE'])
@token_required
@admin
def delete_resource(f, id):
    try:

        resource = db.session.query(Resource).filter_by(id=id).first()
        db.session.delete(resource)
        db.session.commit()

        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'Error'}), 500)

#Admin
@admin_bp.route('/resource/<id>', methods=['PATCH'])
@token_required
@admin
def patch_resource(f, id):
    try:
        resource = db.session.query(Resource).filter_by(id=id).first()
        data = request.json
        
        for key in Resource.__table__.columns.keys():
            if key != "id":
                setattr(resource, key, data.get(key))

        print(resource.__dict__)
        db.session.commit()

        return make_response(jsonify({'message': 'Success'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error'}), 500)

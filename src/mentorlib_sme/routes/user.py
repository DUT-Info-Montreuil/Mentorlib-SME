from mentorlib_sme import app, db, token_required, admin
import uuid
from flask import jsonify, request, make_response, g, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from mentorlib_sme.user.models import User, UserNote
from mentorlib_sme.course.models import Course
from datetime import datetime, timedelta
import jwt
from flask_expects_json import expects_json, ValidationError
from mentorlib_sme.user.validators import userlogin, userupdate, userregister
from mentorlib_sme.user.schemas import UserNoteSchema

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route("/me")
@token_required
def index(f):
    return jsonify({
        'email' : f.email,
        'firstname' : f.firstname,
        'lastname' : f.lastname,
        'student_year' : f.student_year,
        'is_mentor' : f.is_mentor,
        'is_admin' : f.is_admin or False,
        'id': f.id
    })


@user_bp.route("/login", methods=["POST"])
@expects_json(userlogin)
def login():
    try:
        user = db.session.query(User).filter_by(email=g.data.get("email")).first()
        if not user:
            return make_response(jsonify({"message": "Wrong login or password"}), 401)
        
        if check_password_hash(user.password, g.data.get("password")):
            # generates the JWT Token
            token = jwt.encode(
                {"public_id": user.public_id, "exp": datetime.utcnow() + timedelta(minutes=45)},
                app.config["SECRET"],
                "HS256",
            )

            # redirect to home page
            resp = make_response(jsonify({"token": token}), 200)

            return resp
        # returns 403 if password is wrong
        return make_response(
            jsonify({"message": "Could not verify"}), 403, {"WWW-Authenticate": 'Basic realm ="Wrong Password"'}
        )
    except ValidationError as ve:
        return make_response(jsonify({"message": "Wrong login or password"}), 401)

@user_bp.route('/register', methods=['POST'])
@expects_json(userregister)
def register():

    email = g.data.get('email')
    password = g.data.get('password')
    firstname = g.data.get('firstname')
    lastname = g.data.get('lastname')
  
    # checking for existing user
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        # database ORM object
        if not password or not email:
            return make_response("Password and email are required.", 400)
        else:
            user = User(
                public_id = str(uuid.uuid4()),
                email = email,
                firstname = firstname,
                lastname = lastname,
                password = generate_password_hash(password)
            )
            # insert user
            db.session.add(user)
            db.session.commit()

        return make_response("Successfully registered.", 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)
    
@user_bp.route("/profile/update", methods=["PUT"])
@token_required
@expects_json(userupdate)  # Assure que les données JSON attendues sont présentes dans la requête
def update_profile(f, current_user):
    """Mise à jour du profil utilisateur"""
    try:

        updated_data = g.data

        # Mise à jour donnees utilisateur
        current_user.email = updated_data.get("email", current_user.email)
        current_user.firstname = updated_data.get("firstname", current_user.firstname)
        current_user.lastname = updated_data.get("lastname", current_user.lastname)
        current_user.password = generate_password_hash(updated_data.get("password", current_user.password))
        current_user.student_year = updated_data.get("student_year", current_user.student_year)

        # Mise à jour en base de données
        db.session.commit()

        return jsonify({"message": "Profile updated successfully"})

    except ValidationError:
        return make_response(jsonify({"message": "Could not update profile"}), 400)
    
@user_bp.route("/profile/<id>", methods=["GET"])
def get_profile(id):
    """Récupère les informations du profil utilisateur"""
    try:
        user = db.session.query(User).filter_by(id=id).first()
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        nb_courses = db.session.query(Course).filter_by(user_id=id).count()
        return jsonify({
            "id": user.id,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "student_year": user.student_year,
            "nb_courses": nb_courses,
        })

    except Exception as e:
        return make_response(jsonify({"message": "Error"}), 500)
    
@user_bp.route("/profile/<id>/notes", methods=["GET"])

def get_user_notes(id):
    """Récupère les informations du profil utilisateur"""
    try:
        user = db.session.query(User).filter_by(id=id).first()
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        nb_courses = db.session.query(Course).filter_by(user_id=id).count()
        return jsonify({
            "id": user.id,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "student_year": user.student_year,
            "nb_courses": nb_courses,
        })

    except Exception as e:
        return make_response(jsonify({"message": "Error"}), 500)
    
@user_bp.route("/profile/<id>/notes/<resource_id>", methods=["GET"])
@token_required
def get_user_note(f, id, resource_id):
    """Récupère les informations du profil utilisateur"""
    try:
        user = db.session.query(User)\
        .filter_by(id=id)\
        .first()

        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        notes = db.session.query(UserNote)\
        .filter_by(user_id=id, resource_id=resource_id)

        schema = UserNoteSchema(many=True)

        return jsonify(schema.dump(notes))
        

    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Error"}), 500)
    
@user_bp.route("/profile/<id>/notes/<resource_id>", methods=["POST"])
@token_required
def add_user_note(f, id, resource_id):
    try:
        user = db.session.query(User)\
        .filter_by(id=id)\
        .first()

        
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        data = request.json
        
        note = UserNote(
            user_id=id,
            note=data["note"],
            resource_id=resource_id,
            mentor_id= f.id
        )

        db.session.add(note)
        db.session.commit()

        return make_response("Successfully added note.", 201)
        

    except Exception as e:
        print("exception", e.__traceback__)
        return make_response(jsonify({"message": "Error"}), 500)
    
@user_bp.route("/profile/<id>/notes/<resource_id>/<note_id>", methods=["DELETE"])
@token_required
def delete_user_note(f, id, resource_id, note_id):
    try:
        user = db.session.query(User)\
        .filter_by(id=id)\
        .first()

        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        note = db.session.query(UserNote)\
        .filter_by(user_id=id, id=note_id, resource_id=resource_id)\
        .first()

        if not note:
            return make_response(jsonify({"message": "Note not found"}), 404)
        else:
            db.session.delete(note)
            db.session.commit()

        return make_response("Successfully added note.", 201)
        

    except Exception as e:
        print("exception", e.__traceback__)
        return make_response(jsonify({"message": "Error"}), 500)
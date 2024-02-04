from mentorlib_sme import app, db, token_required
import uuid
from flask import jsonify, request, make_response, g, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from mentorlib_sme.user.models import User
from datetime import datetime, timedelta
import jwt
from flask_expects_json import expects_json, ValidationError
from mentorlib_sme.user.validators import userlogin

user_bp = Blueprint('user', __name__)

@user_bp.route('/me')
@token_required
def index(f):
    return jsonify({
        'email' : f.email,
        'firstname' : f.firstname,
        'lastname' : f.lastname,
        'student_year' : f.student_year,
        'is_mentor' : f.is_mentor
    })

@user_bp.route('/login', methods=['POST'])
@expects_json(userlogin)
def login():
    try:
        user = db.session.query(User)\
                .filter_by(email = g.data.get('email'))\
                .first()
        if not user:
            return make_response(
                jsonify({"message":'Could not verify'}),
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist'}
            )
        
        if check_password_hash(user.password, g.data.get("password")):
            # generates the JWT Token
            token = jwt.encode({
                'public_id' : user.public_id,
                'exp' : datetime.utcnow() + timedelta(minutes=45)
                }, app.config['SECRET'], "HS256")

            # redirect to home page
            resp = make_response(jsonify({'token' : token}), 200)
            
            return resp
        # returns 403 if password is wrong
        return make_response(
            jsonify({"message":'Could not verify'}),
            403,
            {'WWW-Authenticate' : 'Basic realm ="Wrong Password"'}
        )
    except ValidationError as ve:
        return make_response(
                jsonify({"message":'Could not verify'}),
                401,
                {'WWW-Authenticate': 'Basic realm ="Login required"'}
            )

@user_bp.route('/register', methods=['POST'])
def register():
    # creates a dictionary of the form data
    data = request.form
  
    # gets name, email and password
    email = data.get('email')
    password = data.get('password')
  
    # checking for existing user
    user = User.query\
        .filter_by(email = email)\
        .first()
    if not user:
        # database ORM object
        if not password or not email:
            return make_response('Password and email are required.', 400)
        else:
            user = User(
                public_id = str(uuid.uuid4()),
                email = email,
                password = generate_password_hash(password)
            )
            # insert user
            db.session.add(user)
            db.session.commit()
  
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)
    
# @app.route("/create")
# def create():
#     user = User()
#     user.email = 'kourzik@iut.univ-paris8.fr'
#     user.password = generate_password_hash('1234')
#     user.firstname = 'Kamel'
#     user.lastname = 'Ourzik'
#     user.is_mentor = True

#     db.session.add(user)
#     db.session.commit()

#     return make_response('Successfully created.', 201)
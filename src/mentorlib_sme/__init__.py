from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://mentorlib:+&&i$5Y+n,zG,4nzf?|W@5.135.143.117:5432/mentorlib"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET"] = "thisissecret"
cors = CORS(app, resources={r"*": {"origins": "*"}})
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from mentorlib_sme.user.models import User
from mentorlib_sme.course.models import Course, AskedCourse, Resource, CourseRegisteredUser


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response


with app.app_context():
    db.create_all()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        bearer = request.headers.get("Authorization")

        if bearer:
            token = bearer.split(" ")[1]
        else:
            token = None

        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            # decoding the payload to fetch the stored details

            data = jwt.decode(token, app.config["SECRET"], algorithms=["HS256"])
            current_user = db.session.query(User).filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users context to the routes
        print(current_user)
        return f(current_user, *args, **kwargs)

    return decorated


from mentorlib_sme.routes.user import user_bp
from mentorlib_sme.routes.course import course_bp

app.register_blueprint(user_bp)
app.register_blueprint(course_bp)

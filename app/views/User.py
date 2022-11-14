# import Bcrypt as Bcrypt
from flask import *
from marshmallow import *
import app.models as models
import app.db as db
from marshmallow_enum import EnumField
from enum import Enum

# bcrypt = Bcrypt()

user_bp = Blueprint('user', __name__, url_prefix='/user')



class UserRole(Enum):
    user = 1
    administrator = 2


@user_bp.route('/', methods=['POST'])
def create_user():
    class User(Schema):
        firstname = fields.Str(required=True)
        lastname = fields.Str(required=True)
        email = fields.Email(required=True)
        phone = fields.Str(required=True)
        password = fields.Str(required=True)
        role = EnumField(UserRole, required=True)


    try:
        user = User().load(request.json)

    except ValidationError as error:
        return jsonify(error.messages), 400

    if db.session.query(models.User).filter(models.User.email == user["email"]).count() != 0:
        return jsonify({"message": "email is not used"}), 400


    # password = bcrypt.generate_password_hash(user['password']).decode('utf-8')


    new_user = models.User(firstname= user["firstname"], lastname= user["lastname"], email= user["email"], phone= user["phone"], password= user["password"], role= user["role"])

    if new_user is None:
        return jsonify({"User doesn't exist"}), 404


    try:
        db.session.add(new_user)

    except:
        db.session.rollback()
        return jsonify({"message": "invalid input"}), 400

    db.session.commit()

    return get_user(new_user.userId)[0], 201


@user_bp.route('/<int:userId>', methods=['GET'])
def get_user (userId):
    user = db.session.query(models.User).filter(models.User.userId == userId).first()

    if not user:
        return jsonify({"message": "invalid input"}), 400

    res = {}
    res["user id"] = user.userId
    return jsonify(res), 200


@user_bp.route('/<int:userId>', methods=['DELETE'])
def delete_user (userId):
    user1 = db.session.query(models.User).filter(models.User.userId == userId).first()

    if not user1:
        return jsonify({"message": "invalid input"}), 400

    try:
        db.session.delete(user1)

    except:
        db.session.rollback()
        return jsonify({"message": "invalid input"}), 400

    db.session.commit()

    return jsonify("user deleted"), 200



@user_bp.route('/<int:userId>', methods=['PUT'])
def update_user(userId):
    try:
        class User(Schema):
            firstname = fields.Str(required=False)
            lastname = fields.Str(required=False)
            email = fields.Email(required=False)
            phone = fields.Str(required=False)
            password = fields.Str(required=False)
            role = EnumField(UserRole, required=False)


        user = User().load(request.json)

    except ValidationError as error:
            return jsonify(error.messages), 400


    # updated.password = generate_password_hash(updated.password)
    user_new = db.session.query(models.User).filter(models.User.userId == userId).first()
    try:
        if 'firstname' in user:
            user_new.firstname = user['firstname']
        if 'lastname' in user:
            user_new.lastname = user['lastname']
        if 'email' in user:
            user_new.email = user['email']
        if 'phone' in user:
            user_new.phone = user['phone']
        if 'password' in user:
            user_new.password = user['password']
        if 'role' in user:
            user_new.role = user['role']
    except:
        db.session.rollback()
        return jsonify('Invalid input', 400)

    db.session.commit()
    return jsonify("user updated"), 200
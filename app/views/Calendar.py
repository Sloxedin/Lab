from flask import *
from marshmallow import *
import app.models as models
import app.db as db

calendar_bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@calendar_bp.route('/', methods=['POST'])
def create_calendar ():
    class Calendar(Schema):
        day = fields.Str(required = True)
        month = fields.Str(required=True)
        events_id = fields.List(fields.Integer(required=True))
    try:
        calendar = Calendar().load(request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    new_calendar = models.Calendar(day=calendar["day"], month=calendar["month"], events_id=calendar["events_id"])

    try:
        db.session.add(new_calendar)

    except:
        db.session.rollback()
        return jsonify({"message": "error creating calendar"}), 400

    db.session.commit()

    return get_calendar(new_calendar.calendarId)[0], 201



@calendar_bp.route('/<int:calendarId>', methods=['GET'])
def get_calendar (calendarId):
    calendar = db.session.query(models.Calendar).filter(models.Calendar.calendarId == calendarId).first()

    if not calendar:
        return jsonify({"message": "calendar not found"}), 400

    ress = {}
    ress["calendar id"] = calendar.calendarId
    return jsonify(ress), 200



@calendar_bp.route('/<int:calendarId>', methods=['DELETE'])
def delete_calendar (calendarId):
    calendar1 = db.session.query(models.Calendar).filter(models.Calendar.calendarId == calendarId).first()

    if not calendar1:
        return jsonify({"message": "invalid input"}), 400


    try:
        db.session.delete(calendar1)
    except:

        db.session.rollback()
        return jsonify({"message": "invalid input"}), 400

    db.session.commit()

    return jsonify("calendar deleted"), 200




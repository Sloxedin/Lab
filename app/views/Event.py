from flask import *
from marshmallow import *
import app.models as models
import app.db as db


event_bp = Blueprint('event', __name__, url_prefix='/event')


@event_bp.route('/', methods=['POST'])
def create_event ():
    class Event (Schema) :
        day = fields.Str(required=True)
        month = fields.Str(required=True)
        nameOfEvent = fields.Str(required=True)
        joined_users_id = fields.List(fields.Int(required=True))
        creator_id = fields.Int(required=True)


    try:
        event = Event().load(request.json)

    except ValidationError as error:
        return jsonify(error.messages), 400


    new_event = models.Event(day=event["day"], month=event["month"], nameOfEvent=event["nameOfEvent"], joined_users_id=event["joined_users_id"], creator_id=event["creator_id"])

    if new_event is None:
        return jsonify({"Event doesn't exist"}), 404

    try:
        db.session.add(new_event)

    except:
        db.session.rollback()
        return jsonify({"message": "error creating event"}), 400

    db.session.commit()

    return get_event(new_event.eventId)[0], 201



@event_bp.route('/<int:eventId>', methods=['GET'])
def get_event(eventId):
    event = db.session.query(models.Event).filter(models.Event.eventId == eventId).first()

    if not event:
        return jsonify({"message": "event not found"}), 400

    res = {}
    res["event id"] = event.eventId
    return jsonify(res), 200



@event_bp.route('/<int:eventId>', methods=['DELETE'])
def delete_event (eventId):
    event1 = db.session.query(models.Event).filter(models.Event.eventId == eventId).first()

    if not event1:
        return jsonify({"message": "invalid input"}), 400


    try:
        db.session.delete(event1)

    except:
        db.session.rollback()
        return jsonify({"message": "invalid input"}), 400

    db.session.commit()

    return jsonify("event deleted"), 200



@event_bp.route('/<int:eventId>', methods=['PUT'])
def update_event(eventId):
    try:
        class Event(Schema):
            day = fields.Str(required=True)
            month = fields.Str(required=True)
            nameOfEvent = fields.Str(required=True)
            joined_users_id = fields.List(fields.Int(required=True))
            creator_id = fields.Int(required=True)


        event = Event().load(request.json)

    except ValidationError as error:
            return jsonify(error.messages), 400


    event_new = db.session.query(models.Event).filter(models.Event.eventId == eventId).first()
    try:
        if 'day' in event:
            event_new.day = event['day']
        if 'month' in event:
            event_new.month = event['month']
        if 'nameOfEvent' in event:
            event_new.nameOfEvent = event['nameOfEvent']
        if 'joined_users_id' in event:
            event_new.joined = event['joined_users_id']
        if 'creator_id' in event:
            event_new.creator_id = event['creator_id']

    except:
        db.session.rollback()
        return jsonify('Invalid input', 400)

    db.session.commit()
    return jsonify("event updated"), 200

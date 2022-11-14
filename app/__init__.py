from flask import Flask
from app.views import User, Event, Calendar


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'


app.register_blueprint(Event.event_bp)
app.register_blueprint(User.user_bp)
app.register_blueprint(Calendar.calendar_bp)
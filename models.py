from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
engine = create_engine("mysql+pymysql://root:max25012004@localhost:3306/calendar_main")
Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    userId = Column('userId', Integer, primary_key=True)
    firstname = Column('firstname', String(50))
    lastname = Column('lastname', String(50))
    email = Column('email', String(50))
    phone = Column('phone', String(50))
    password = Column('password', String(50))
    role = Column('role', String(50))

class Event(Base):
    __tablename__ = "Event"
    eventId = Column('eventId', Integer, primary_key=True)
    day = Column('day', String(50))
    month = Column('month', String(50))
    nameOfEvent = Column('nameOfEvent', String(50))
    joined_users_id = Column('joinedUsers', Integer, ForeignKey(User.userId))
    creator_id = Column('creator', Integer)



class Calendar(Base):
    __tablename__ = "Calendar"
    calendarId = Column('calendarId', Integer, primary_key=True)
    day = Column('day', String(50))
    month = Column('month', String(50))
    events_id = Column('events', Integer, ForeignKey(Event.eventId))


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


user1 = [User(firstname='Maksym', lastname='Pechonkin', email='maksym@gmail.com', phone='+380687500053', password ='root123', role='admin')]
event1 = [Event(day='monday', month='july', nameOfEvent='deadline', joined_users_id=1, creator_id=1)]
calendar1 = [Calendar(day='monday', month='july', events_id=1)]
session.add_all(user1)
session.add_all(event1)
session.add_all(calendar1)
session.commit()
session.close()
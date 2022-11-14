from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from app.models import *

engine = create_engine(url='mysql+pymysql://root:max25012004@localhost:3306/calendar_main')

metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()
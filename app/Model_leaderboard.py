from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# create a base class for our models
Base = declarative_base()

# define a Leaderboard model
class Leaderboard(Base):
    __tablename__ = 'leaderboards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    name = Column(String(50))
    message = Column(String)
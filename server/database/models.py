from sqlalchemy.orm import relationship

from database.database import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func


class DbUser(Base):
    __tablename__ = "users"
    userId = Column(String, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    posts = relationship('DbPost', back_populates='user', cascade='all, delete, delete-orphan')

class DbPost(Base):
    __tablename__ = "post"
    postid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    image = Column(String)
    dateshared = Column(DateTime, default=func.now())
    userid = Column(String, ForeignKey('users.userId'))
    user = relationship('DbUser', back_populates='posts')
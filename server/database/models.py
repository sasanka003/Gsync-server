from datetime import datetime

from sqlalchemy.orm import relationship

from database.database import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, Text, Enum
from sqlalchemy.sql import func

# Association table for the many-to-many relationship between users and posts through comments
comments_table = Table(
    'comments', Base.metadata,
    Column('commentId', Integer, ForeignKey('comments.commentId'), primary_key=True, index=True),
    Column('userId', Integer, ForeignKey('users.userId'),primary_key=True,index=True),
    Column('postId', Integer, ForeignKey('posts.postId'),primary_key=True,index=True),
    Column('content', Text, nullable=False),
    Column('lastUpdated', DateTime, nullable=True),
    Column('createdAt', DateTime, efault=datetime.utcnow)
)

class DbUser(Base): #userId ?
    __tablename__ = "users"
    userName = Column(String, primary_key=True, index=True, unique=True, autoincrement=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    createdAt = Column(DateTime, default=DateTime.utcnow)
    posts = relationship("DbPost", back_populates="user")
    comments = relationship("DbComment", secondary=comments_table,back_populates="user")
    # votes = relationship("DbVote", back_populates="user")

class DbPost(Base):
    __tablename__ = "posts"
    postId = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    media = Column(String, nullable=True)
    postType = Column(Enum('Question', 'Answer', name='post_types'))
    userId = Column(String, ForeignKey("users.userId"))
    parentPostId = Column(Integer, ForeignKey("posts.postId"), nullable=True)
    createdAt = Column(DateTime, default=DateTime.utcnow)
    user = relationship("DbUser", back_populates="posts")
    comments = relationship("DbComment", secondary=comments_table,back_populates="post")
    # votes = relationship("DbVote", back_populates="post")
    # tags = relationship("DbTag", secondary=post_tags, back_populates="posts")

class DbComment(Base):
    __tablename__ = "comments"
    commentId = Column(Integer, primary_key=True, index=True) #autoincremet ?
    content = Column(Text, nullable=False)
    lastUpdated = Column(DateTime, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    postId = Column(Integer, ForeignKey("posts.postId"))
    userId = Column(String, ForeignKey("users.userId"))
    user = relationship("DbUser", secondary=comments_table,  back_populates="comments")
    post = relationship("DbPost", secondary=comments_table, back_populates="comments")
    # votes = relationship("DbVote", back_populates="comment")

# class DbUser(Base):
#     __tablename__ = "users"
#     userId = Column(Integer, primary_key=True, index=True)
#     username = Column(String)
#     email = Column(String, unique=True)
#     password = Column(String)
#     posts = relationship('DbPost', back_populates='user', cascade='all, delete, delete-orphan')
#     comments = relationship('DbComment', back_populates='user', cascade='all, delete, delete-orphan')


# class DbPost(Base):
#     __tablename__ = "post"
#     postid = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     title = Column(String)
#     description = Column(String)
#     image = Column(String)
#     dateshared = Column(DateTime, default=func.now())
#     userid = Column(String, ForeignKey('users.userId'))
#     user = relationship('DbUser', back_populates='posts')
#     comments = relationship('DbComment', back_populates='post', cascade='all, delete, delete-orphan')


# class DbComment(Base):
#     __tablename__ = 'comments'
#     commentid = Column(Integer, primary_key=True, autoincrement=True)
#     userid = Column(String, ForeignKey('users.userId'))
#     postid = Column(Integer, ForeignKey('post.postid'))
#     comment = Column(String)
#     datecommented = Column(DateTime, default=func.now())
#     user = relationship('DbUser', back_populates='comments')
#     post = relationship('DbPost', back_populates='comments')
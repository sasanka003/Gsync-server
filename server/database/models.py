import datetime
from sqlalchemy.orm import relationship

from database.database import Base
from sqlalchemy import Column, Enum, String, Integer, DateTime, ForeignKey, Table, Text


post_tags = Table('post_tags', Base.metadata,
    Column('postId', Integer, ForeignKey('posts.postId'), primary_key=True),
    Column('tagId', Integer, ForeignKey('tags.tagId'), primary_key=True)
)

class DbUser(Base):
    __tablename__ = "users"
    userName = Column(String, primary_key=True, index=True, unique=True, autoincrement=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    createdAt = Column(DateTime, default=DateTime.utcnow)
    posts = relationship("DbPost", back_populates="user")
    comments = relationship("DbComment", back_populates="user")
    votes = relationship("DbVote", back_populates="user")


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
    comments = relationship("DbComment", back_populates="post")
    votes = relationship("DbVote", back_populates="post")
    tags = relationship("DbTag", secondary=post_tags, back_populates="posts")


class DbComment(Base):
    __tablename__ = "comments"
    commentId = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    lastUpdated = Column(DateTime, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    postId = Column(Integer, ForeignKey("posts.postId"))
    userId = Column(String, ForeignKey("users.userId"))
    user = relationship("DbUser", back_populates="comments")
    post = relationship("DbPost", back_populates="comments")
    votes = relationship("DbVote", back_populates="comment")


class DbTag(Base):
    __tablename__ = "tags"
    tagId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tagName = Column(String, unique=True)
    posts = relationship("DbPost", secondary=post_tags, back_populates="tags",)


class DbContact(Base):
    __tablename__ = "contact"
    contactId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    organization = Column(String, nullable=True)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)

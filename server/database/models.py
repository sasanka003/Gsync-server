from datetime import datetime

from sqlalchemy.orm import relationship

from database.database import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, Text, Enum

# Association table for the many-to-many relationship between users and posts through comments
comments_table = Table(
    'comments', Base.metadata,
    Column('voteId', Integer, ForeignKey('comments.voteId'), primary_key=True, index=True),
    Column('userId', Integer, ForeignKey('users.userId'),primary_key=True,index=True),
    Column('postId', Integer, ForeignKey('posts.postId'),primary_key=True,index=True),
    Column('content', Text, nullable=False),
    Column('lastUpdated', DateTime, nullable=True),
    Column('createdAt', DateTime, efault=datetime.utcnow)
)

# Association table for the many-to-many relationship between users and posts through votes
votes_table = Table(
    'votes', Base.metadata,
    Column('commentId', Integer, ForeignKey('votes.voteId'), primary_key=True, index=True),
    Column('userId', Integer, ForeignKey('users.voteId'), primary_key=True, index=True),
    Column('postId', Integer, ForeignKey('posts.postId'), primary_key=True, index=True),
    Column('createdAt', DateTime, efault=datetime.utcnow),
    Column('voteType', Enum('Upvote', 'Downvote', name='vote_types'))

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
    votes = relationship("DbVote", secondary=votes_table,back_populates="user")

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
    voteCount = Column(Integer, default=0)
    user = relationship("DbUser", back_populates="posts")
    comments = relationship("DbComment", secondary=comments_table,back_populates="post")
    votes = relationship("DbVote", secondary=votes_table, back_populates="post")
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

class DbVote(Base):
    __tablename__ = "votes"
    voteId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    voteType = Column(Enum('Upvote', 'Downvote', name='vote_types'))
    userId = Column(Integer, ForeignKey("users.userId"))
    postId = Column(Integer, ForeignKey("posts.postId"))
    createdAt = Column(DateTime, default=datetime.utcnow)
    user = relationship("DbUser", secondary=votes_table, back_populates="votes")
    post = relationship("DbPost", secondary=votes_table,  back_populates="votes")


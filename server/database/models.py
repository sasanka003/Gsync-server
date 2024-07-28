from datetime import datetime
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base
from sqlalchemy import Column, Enum, String, Float, DateTime, ForeignKey, Table, Text, UUID, Integer, Boolean


post_tags = Table('postTags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.post_id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.tag_id'), primary_key=True)
)

class DbUser(Base):
    __tablename__ = "profiles"
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(Text, nullable=True)
    email = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    phone = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    posts = relationship("DbPost", back_populates="user")
    comments = relationship("DbComment", back_populates="user")
    votes = relationship("DbVote", back_populates="user")
    plantations = relationship("DbPlantation", back_populates="user")


class DbPost(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    media = Column(String, nullable=True)
    post_type = Column(Enum('Question', 'Answer', name='post_types'))
    user_id = Column(UUID, ForeignKey("profiles.user_id"))
    parent_post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("DbUser", back_populates="posts")
    comments = relationship("DbComment", back_populates="post")
    votes = relationship("DbVote", back_populates="post")
    tags = relationship("DbTag", secondary=post_tags, back_populates="posts")


class DbComment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    last_updated = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    user_id = Column(UUID, ForeignKey("profiles.user_id"))
    user = relationship("DbUser", back_populates="comments")
    post = relationship("DbPost", back_populates="comments")
    votes = relationship("DbVote", back_populates="comment")


class DbTag(Base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tag_name = Column(String, unique=True)
    posts = relationship("DbPost", secondary=post_tags, back_populates="tags",)


class DbContact(Base):
    __tablename__ = "contact"
    contact_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    organization = Column(Text, nullable=True)
    email = Column(Text, nullable=False)
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    checked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DbVote(Base):
    __tablename__ = "votes"
    vote_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vote_type = Column(Enum('Upvote', 'Downvote', name='vote_types'))
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("comments.comment_id"), nullable=True)
    user_id = Column(UUID, ForeignKey("profiles.user_id"))
    user = relationship("DbUser", back_populates="votes")
    post = relationship("DbPost", back_populates="votes")
    comment = relationship("DbComment", back_populates="votes")


class DbPlantation(Base):
    __tablename__ = "plantation"
    plantation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    city = Column(Text, nullable=False)
    province = Column(Text)
    country = Column(Text, nullable=False, default="Srilanka")
    plantation_length = Column(Float, nullable=False)
    plantation_width = Column(Float, nullable=False)
    subscription = Column(Enum('Basic', 'Gardener', 'Enterprise', name="subscription_types"), nullable=False, default="Basic")
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.user_id"), nullable=False)
    verified = Column(Boolean, default=False)
    user = relationship("DbUser", back_populates="plantations")

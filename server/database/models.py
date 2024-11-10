from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base
from sqlalchemy import Column, Enum, String, Float, DateTime, ForeignKey, Table, Text, UUID, Integer, Boolean
from sqlalchemy.orm import validates


post_tags = Table('postTags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.post_id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.tag_id'), primary_key=True)
)

class DbUser(Base):
    __tablename__ = "profiles"
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(Text, nullable=True)
    email = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(Enum('Verified', 'Pending', 'Disabled', name='profile_status'), nullable=False, default='Pending')
    type = Column(Enum('SysAdmin', 'User', 'EnterpriseAdmin', 'EnterpriseUser', name='profile_types'), nullable=False, default='User')
    enterprise_users = relationship("DbEnterpriseUser", back_populates="admin", foreign_keys="[DbEnterpriseUser.admin_id]")
    posts = relationship("DbPost", back_populates="user")
    comments = relationship("DbComment", back_populates="user")
    votes = relationship("DbVote", back_populates="user")
    plantations = relationship("DbPlantation", back_populates="user", foreign_keys="[DbPlantation.user_id]")

class DbEnterpriseUser(Base):
    __tablename__ = "enterprise_users"
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.user_id", ondelete="CASCADE"), primary_key=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("profiles.user_id", ondelete="CASCADE"), nullable=False)
    admin = relationship("DbUser", back_populates="enterprise_users", foreign_keys=[admin_id], single_parent=True)
    plantation_access = relationship("DbPlantationAccess", back_populates="user", cascade="all, delete-orphan")

class DbPost(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    media = Column(Text, nullable=True)
    post_type = Column(Enum('Question', 'Answer', name='post_types'))
    user_id = Column(UUID, ForeignKey("profiles.user_id"))
    parent_post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), nullable=True)
    user = relationship("DbUser", back_populates="posts")
    comments = relationship("DbComment", back_populates="post", cascade="all, delete-orphan")
    votes = relationship("DbVote", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("DbTag", secondary=post_tags, back_populates="posts")


class DbComment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    user_id = Column(UUID, ForeignKey("profiles.user_id"))
    user = relationship("DbUser", back_populates="comments")
    post = relationship("DbPost", back_populates="comments")
    votes = relationship("DbVote", back_populates="comment")


class DbTag(Base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tag_name = Column(Text, unique=True)
    posts = relationship("DbPost", secondary=post_tags, back_populates="tags",)

    @validates('tag_name')
    def lowercase_tag_name(self, key, tag_name):
        return tag_name.lower() if tag_name else None
    
    def __repr__(self):
        return f"<Tag(tag_id={self.tag_id}, tag_name='{self.tag_name}')>"


class DbContact(Base):
    __tablename__ = "contact"
    contact_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    organization = Column(Text, nullable=True)
    email = Column(Text, nullable=False)
    subject = Column(Text, nullable=False)
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
    statuses = relationship("DbPlantationStatus", back_populates="plantation")
    user_access = relationship("DbPlantationAccess", back_populates="plantation", cascade="all, delete-orphan")

class DbPlantationStatus(Base):
    __tablename__ = "plantation_statuses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    plantation_id = Column(Integer, ForeignKey('plantation.plantation_id'), nullable=False)
    status = Column(Enum('Unapproved', 'Approved', 'Declined', name="plantation_status_types"), nullable=False, default='Unapproved')
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    plantation = relationship("DbPlantation", back_populates="statuses")


class DbPlantationAccess(Base):
    __tablename__ = "plantation_access"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("enterprise_users.user_id", ondelete="CASCADE"), nullable=False)
    plantation_id = Column(Integer, ForeignKey("plantation.plantation_id", ondelete="CASCADE"), nullable=False)
    user = relationship("DbEnterpriseUser", back_populates="plantation_access")
    plantation = relationship("DbPlantation", back_populates="user_access")

class DbSensor(Base):
    __tablename__ = "sensors"
    sensor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    plantation_id = Column(Integer, ForeignKey("plantation.plantation_id"), nullable=False)
    # plantation = relationship("DbPlantation", back_populates="sensors")

class DbSensorImage(Base):
    __tablename__ = "sensor_images"
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(Text, nullable=False)
    sensor_id = Column(Integer, ForeignKey("sensors.sensor_id"), nullable=False)
    # sensor = relationship("DbSensor", back_populates="images")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    plantation_id  = Column(Integer, ForeignKey("plantation.plantation_id"), nullable=False)

class DbSensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey("sensors.sensor_id"), nullable=False)
    # sensor = relationship("DbSensor", back_populates="data")
    temperature = Column(Float, nullable=False)
    soil_moisture = Column(Float, nullable=False)
    # other sensor data
    created_at = Column(DateTime(timezone=True), server_default=func.now())

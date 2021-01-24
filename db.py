from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy import Column, DateTime, String, Integer

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column('id', Integer, primary_key=True)
    telegram_id = Column('telegram_id', String(255),
                         nullable=False, unique=True)
    name = Column('name', String(255), nullable=False)

    messages = relationship('Message', secondary='groups_messages')


class Message(Base):
    __tablename__ = 'messages'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(255), nullable=False)
    content = Column('content', String(255), nullable=False)
    date_time = Column('date_time', String, nullable=False)

    groups = relationship('Group', secondary='groups_messages')


class GroupMessage(Base):
    __tablename__ = 'groups_messages'

    message_id = Column('message_id', Integer, ForeignKey(
        'messages.id',  ondelete='CASCADE'), primary_key=True)
    group_id = Column('group_id', Integer,  ForeignKey(
        'groups.id', ondelete='CASCADE'), primary_key=True)


engine = create_engine(config("DB_URL"), echo=True)
engine.connect()
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

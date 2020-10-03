from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy import Column, DateTime, String, Integer, Time

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column('id', Integer, primary_key=True)
    link = Column('link', String, nullable=False, unique=True)


class Group(Base):
    __tablename__ = 'groups'
    id = Column('id', Integer, primary_key=True)
    telegram_id = Column('telegram_id', String, nullable=False, unique=True)
    name = Column('name', String, nullable=False, unique=True)


class GroupMessage(Base):
    __tablename__ = 'groups_messages'

    id = Column('id', Integer, primary_key=True)
    message_id = Column('message_id', Integer, ForeignKey(
        'messages.id'), nullable=False)
    group_id = Column('group_id', Integer, ForeignKey(
        'groups.id'), nullable=False)
    time = Column('time', Time, nullable=False)

    message = relationship(Message, backref=backref('messages', uselist=True))
    group = relationship(Group, backref=backref('groups', uselist=True))


engine = create_engine('sqlite:///database.sqlite', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)
from typing import List

from sqlalchemy import Column, Enum, ForeignKey, Integer, TIMESTAMP, Text, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Images(Base):
    __tablename__ = 'Images'

    image_name = mapped_column(Text, nullable=False)
    image_hash = mapped_column(Text, nullable=False)
    id = mapped_column(Integer, primary_key=True)

    Note_Image: Mapped[List['NoteImage']] = relationship('NoteImage', uselist=True, back_populates='image')


class Notes(Base):
    __tablename__ = 'Notes'

    title = mapped_column(Text, nullable=False)
    note_text = mapped_column(Text, nullable=False)
    id = mapped_column(Integer, primary_key=True)
    description = mapped_column(Text)
    creation_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    Note_Image: Mapped[List['NoteImage']] = relationship('NoteImage', uselist=True, back_populates='note')
    User_Note: Mapped[List['UserNote']] = relationship('UserNote', uselist=True, back_populates='note')


class Users(Base):
    __tablename__ = 'Users'

    login = mapped_column(Text, nullable=False, unique=True)
    e_mail = mapped_column(Text, nullable=False, unique=True)
    password_ = mapped_column(Text, nullable=False)
    id = mapped_column(Integer, primary_key=True)
    account_type = mapped_column(Enum('User', 'Admin'), server_default=text("'User'"))

    Sessions: Mapped['Sessions'] = relationship('Sessions', uselist=False, back_populates='user')
    User_Note: Mapped[List['UserNote']] = relationship('UserNote', uselist=True, back_populates='user')


class NoteImage(Base):
    __tablename__ = 'Note_Image'

    note_id = mapped_column(ForeignKey('Notes.id'), nullable=False)
    image_id = mapped_column(ForeignKey('Images.id'), nullable=False)
    id = mapped_column(Integer, primary_key=True)

    image: Mapped['Images'] = relationship('Images', back_populates='Note_Image')
    note: Mapped['Notes'] = relationship('Notes', back_populates='Note_Image')


class Sessions(Base):
    __tablename__ = 'Sessions'

    user_id = mapped_column(ForeignKey('Users.id', ondelete='CASCADE'), nullable=False, unique=True)
    token = mapped_column(Text, nullable=False, unique=True)
    ip_address = mapped_column(Text, nullable=False)
    id = mapped_column(Integer, primary_key=True)
    creation_time = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    expiration_date = mapped_column(TIMESTAMP)

    user: Mapped['Users'] = relationship('Users', back_populates='Sessions')


class UserNote(Base):
    __tablename__ = 'User_Note'

    user_id = mapped_column(ForeignKey('Users.id'), nullable=False)
    note_id = mapped_column(ForeignKey('Notes.id'), nullable=False)
    id = mapped_column(Integer, primary_key=True)
    user_type = mapped_column(Enum('Owner', 'User'), server_default=text("'Owner'"))

    note: Mapped['Notes'] = relationship('Notes', back_populates='User_Note')
    user: Mapped['Users'] = relationship('Users', back_populates='User_Note')

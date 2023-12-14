from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, configure_mappers
from cryptography.fernet import Fernet
import base64
import hashlib

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    master_password_hash = Column(String, nullable=False)

    passwords = relationship('Password', back_populates='user')

class Password(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    website = Column(String, nullable=False)
    username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)

    user = relationship('User', back_populates='passwords')
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='passwords')
    note = relationship('Note', uselist=False, back_populates='password')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    passwords = relationship('Password', back_populates='category')

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    password_id = Column(Integer, ForeignKey('passwords.id'), nullable=False)

    password = relationship('Password', back_populates='note')

configure_mappers()

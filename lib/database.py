from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///password_manager.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    master_password_hash = Column(String)

    passwords = relationship("Password", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, index=True)
    website = Column(String, index=True)
    username = Column(String)
    encrypted_password = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="passwords")

Base.metadata.create_all(bind=engine)
session = SessionLocal()

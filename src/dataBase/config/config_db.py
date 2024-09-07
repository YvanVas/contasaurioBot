from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DateTime, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'contabot.db')

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

metadata = MetaData()

Base = declarative_base()


class TimbradosModel(Base):
    __tablename__ = 'timbrados'

    id = Column(Integer, primary_key=True)
    timbrado_number = Column(String(255), nullable=False)
    client_name = Column(String(255), nullable=False)
    numero_inicio = Column(String(255), nullable=False)
    numero_fin = Column(String(255), nullable=False)
    end_date = Column(Date, nullable=False)


class UsersModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    id_telegram = Column(Integer)
    first_name = Column(String(255))
    last_name = Column(String(255))
    full_name = Column(String(255))
    username = Column(String(255))
    is_bot = Column(String(255))

class MessagesModel(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, nullable=False)
    from_user_id = Column(Integer, nullable=False)
    text = Column(String)
    date = Column(DateTime, nullable=False)


class ContribuyenteModel(Base):
    __tablename__ = 'contribuyentes'

    id = Column(Integer, primary_key=True)
    ruc =Column(String(255))
    dv = Column(String(100))
    fullname = Column(String(255))
    status = Column(String(100))


Session = sessionmaker(bind=engine)
session = Session()

#Base.metadata.create_all(bind=engine)

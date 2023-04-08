from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DateTime, Date, Float
import datetime

engine = create_engine('sqlite:///contabot.db', echo=True)

meta = MetaData()

trackeds = Table(
    'timbrados',
    meta,
    Column('id', Integer, primary_key=True),
    Column('timbrado_number', String(255), nullable=False),
    Column('client_name', String(255), nullable=False),
    Column('numero_inicio', String(255), nullable=False),
    Column('numero_fin', String(255), nullable=False),
    Column('end_date', Date, nullable=False),
)

users = Table(
    'users',
    meta,
    Column('id', Integer, primary_key=True),
    Column('id_telegram', Integer),
    Column('first_name', String(255)),
    Column('last_name', String(255)),
    Column('full_name', String(255)),
    Column('username', String(255)),
    Column('is_bot', String(255)),
)

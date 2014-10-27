from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Property(Base):
	__tablename__ = 'property'
	id = Column(Integer, primary_key=True)
	description = Column(String)

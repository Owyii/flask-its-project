from sqlalchemy import create_engine, text, inspect
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base

from PyMovieDb import IMDB
import json

database = r'sqlite:///C:\Users\Utente\Documents\Scola\MachineLearning\Giuri\flask-its-project\MovieCollector\instance\mydb.db'

def ExecQuery(query):
    # create a SQLAlchemy engine to connect to the database file
    engine = create_engine(database)

    # create a SQLAlchemy connection to the database
    conn = engine.connect()

    # execute a SQL query to retrieve all rows and columns from the films table
    result = conn.execute(text(query))

    # print the result set
    for row in result:
        print(row)

    # close the connection
    conn.close()

def GetTabble():
    # create a SQLAlchemy engine to connect to the database file
    engine = create_engine(database)

    # create a SQLAlchemy inspector to get information about the database
    inspector = inspect(engine)

    # get a list of all the table names in the database
    table_names = inspector.get_table_names()

    # print the table names
    print(table_names)

def RemoveTable(table):
    engine = create_engine(database)
    metadata = MetaData()
    my_table = Table(table,metadata,autoload_with=engine)
    my_table.drop(engine)

def create_table():
    # create engine to connect to the database file
    engine = create_engine(database)

        # create a base class for our table model
    Base = declarative_base()

    # define the Films table
    class Films(Base):
        __tablename__ = 'Films'
        id = Column(Integer, primary_key=True)
        title = Column(String)
        director = Column(String)
        year = Column(Integer)
        description = Column(String)
        poster = Column(String)

    # create the table in the database
    Base.metadata.create_all(engine)

ExecQuery("SELECT * FROM Films")
# RemoveTable('Films')
#create_table()
GetTabble()


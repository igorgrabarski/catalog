from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities import *
import os


""" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
The following command is used to create the 'catalog' database
on PostgreSQL Server. If you use another database ,
please update them accordingly.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
os.system('createdb catalog')


"""
Connection string to the database in the following format:
'db_type://user:password@host:port/db_name'
where:
db_type - type of database (postgresql, mysql, sqlite etc.)
user - username
password - user's password
host - host on which database is running
port - port on which database is listening
db_name - the name of database
"""
DB_URL = 'postgresql:///catalog'

"""
In development, set 'echo=True' to receive messages
from SQLAlchemy environment.
In production, please change it to 'echo=False'!!!
"""
engine = create_engine(DB_URL, echo=False)

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)

session = DBSession()


"""
Below categories will be created in database.
Change them by your own here or insert others
directly into the database with 'INSERT INTO category...'
"""
categories = [
    "Java",
    "Python",
    'Hibernate',
    'Spring',
    'Flask',
    'Django',
    'Vaadin',
    'JSF',
    'TCP/IP',
    'Maven',
    'Gradle',
    'Git',
    'Perforce',
    'EasyMock',
    'JUnit',
    'PostgreSQL',
    'MySQL',
    'MongoDB',
    'Cassandra',
    'Redis']


for c in categories:
    category = Category(name=c)
    session.add(category)

session.commit()


os.system('clear')
print "*********************************************************"
print " All is ready! You can run 'python application.py' now!"
print "*********************************************************"

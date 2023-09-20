#!/usr/bin/python3
""" DBStorage module """
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models import classes

class DBStorage:
    """ Database storage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize DBStorage """
        db_user = environ.get('HBNB_MYSQL_USER')
        db_pwd = environ.get('HBNB_MYSQL_PWD')
        db_host = environ.get('HBNB_MYSQL_HOST')
        db_db = environ.get('HBNB_MYSQL_DB')
        db_env = environ.get('HBNB_ENV')

        self.__engine = create_engine(f'mysql+mysqldb://{db_user}:{db_pwd}@{db_host}/{db_db}',
                                      pool_pre_ping=True)

        if db_env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query all objects """
        session = self.__session
        objects = {}

        if cls:
            query = session.query(classes[cls]).all()
        else:
            query = []
            for cls in classes:
                query.extend(session.query(classes[cls]).all())

        for obj in query:
            key = f"{obj.__class__.__name__}.{obj.id}"
            objects[key] = obj

        return objects

    def new(self, obj):
        """ Add an object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes to the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete obj from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and create a new database session """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

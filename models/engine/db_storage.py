#!/usr/bin/python3
""" A new class for sqlAlchemy database engine """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ To create database storage engine """
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Return a dictionary of __object
        """
        my_dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                my_dic[key] = elem
        else:
            my_list = [State, City, User, Place, Review, Amenity]
            for obj in my_list:
                query = self.__session.query(obj)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    my_dic[key] = elem
        return (my_dic)

    def new(self, obj):
        """
        To add the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        To commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        To delete from the current database session 
        """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """
        To create all tables in the database and initialize a new session
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """
        To close the working SQLAlchemy session
        """
        self.__session.close()

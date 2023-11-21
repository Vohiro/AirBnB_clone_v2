#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from sqlalchemy.ext.declarative import declarative_base
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class BaseModel:
    """
    This class will defines all common attributes/methods for all other classes
    """
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """Instantiation of base model class, only kwargs to be used
        Attributes:
            id: the unique id generated
            created_at:the created date
            updated_at:the updated date
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """
        convert the instance to string
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        """
        return a string representaion of the instance
        """
        return self.__str__()


    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Method to convert instance into dictionary format
        """
        my_dic = dict(self.__dict__)
        my_dic["__class__"] = str(type(self).__name__)
        my_dic["created_at"] = self.created_at.isoformat()
        my_dic["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in my_dic.keys():
            del my_dic['_sa_instance_state']
        return my_dic

    def delete(self):
        """ 
        To delete current instance from storage
        """
        models.storage.delete(self)

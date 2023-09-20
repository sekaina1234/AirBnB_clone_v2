#!/usr/bin/python3
""" Base model module """

from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    """ Base class for all models """

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """ Initialize a new BaseModel """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    if key != "id":
                        setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            time = datetime.utcnow()
            self.created_at = time
            self.updated_at = time
        else:
            self.id = str(uuid.uuid4())
            time = datetime.utcnow()
            self.created_at = time
            self.updated_at = time

    def __str__(self):
        """ Return a string representation of the BaseModel """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """ Update the updated_at attribute and save to storage """
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """ Return a dictionary representation of the BaseModel """
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """ Delete the current instance from storage """
        from models import storage
        storage.delete(self)

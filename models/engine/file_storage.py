#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json

class FileStorage:
    # ... (existing code)

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.
        If obj is None, the method should not do anything.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def all(self, cls=None):
        """
        Returns a dictionary of objects filtered by class name (optional).
        """
        if cls is None:
            return self.__objects

        filtered_objects = {}
        for key, value in self.__objects.items():
            obj_cls = value.__class__
            if obj_cls == cls:
                filtered_objects[key] = value
        return filtered_objects

    # ... (existing code)

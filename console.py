#!/usr/bin/python3
"""
This is the console for AirBnB
"""
import cmd
import shlex
import models
from models.base_model import BaseModel
from io import StringIO
from unittest.mock import patch
import re

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel
        # Add other classes here
    }

    def do_create(self, arg):
        """Create a new instance of a class with specified parameters"""
        if not arg:
            print("** class name missing **")
            return

        args = shlex.split(arg)
        class_name = args[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        args = ' '.join(args[1:])
        args = re.split(r'(?<!\\) ', args)

        instance_dict = {}
        for arg in args:
            # Split key and value using '=' as separator
            key, value = arg.split('=')
            # Remove any escaping of double quotes
            value = value.replace('\\"', '"')
            instance_dict[key] = value

        # Create a new instance of the specified class
        new_instance = HBNBCommand.classes[class_name](**instance_dict)
        new_instance.save()
        print(new_instance.id)

if __name__ == '__main__':
    HBNBCommand().cmdloop()

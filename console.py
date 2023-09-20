#!/usr/bin/python3
""" console """

from models.base_model import BaseModel
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.place import Place
from models.state import State
import cmd
import re
from models import storage


class HBNBCommand(cmd.Cmd):
    """ HBNH console """

    prompt = '(hbnb) '
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
        }

    objs = storage.all()
    Dict_Check = 0

    def precmd(self, line):
        "analyzes the input"
        if '.' in line:
            if '{' in line or '}' in line:
                self.Dict_Check = quit
            else:
                self.Dict_Check = 0

            _delim = '.(", :){}'
            GetInput = re.split('[{}]+'.format(re.escape(_delim)), line)
            Res = GetInput[1]

            for i in range(len(GetInput) - 1):
                if i != 1:
                    Res += " " + GetInput[i].strip("'")

            return Res
        else:
            return line

    def emptyline(self):
        "Manage the blank line"
        pass

    def do_quit(self, line):
        "Terminate the program using the Quit command"
        return True

    def do_EOF(self, line):
        "Terminate the program using the EOF (ctrl+D) command"
        return True

    def do_create(self, line):
        "Instantiates a new object of a class with provided arguments, records it to
        the JSON file, and displays the associated ID.
        Usage: create <Class name> <param1=value1> <param2=value2> ..."

        if not line:
            print("** class name missing **")
            return

        args = line.split()
        class_name = args[0]

        if class_name not in self.classes.keys():
            print("** class doesn't exist **")
            return

        kwargs = {}
        for param in args[1:]:
            param_parts = param.split('=')
            if len(param_parts) == 2:
                key, value = param_parts
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                kwargs[key] = value

        new_instance = self.classes[class_name](**kwargs)
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        "Displays the textual representation of an object
        by referencing its class name and ID.
        Example: $ show BaseModel 1234-1234-1234."

        if not line:
            print("** class name missing **")
        else:
            _Args = line.split()

            if _Args[0] not in self.classes.keys():
                print("** class doesn't exist **")
            elif len(_Args) < 2:
                print("** instance id missing **")
            else:
                key = f"{_Args[0]}.{_Args[1]}"
                if key in self.objs.keys():
                    print(self.objs[key])
                else:
                    print("** no instance found **")

    def do_destroy(self, line):
        "Removes an object using its class name and ID,
        updating the JSON file accordingly.
        Example: $ destroy BaseModel 1234-1234-1234."

        if not line:
            print("** class name missing **")
        else:
            _Args = line.split()

            if _Args[0] not in self.classes.keys():
                print("** class doesn't exist **")
            elif len(_Args) < 2:
                print("** instance id missing **")
            else:
                key = f"{_Args[0]}.{_Args[1]}"
                if key in self.objs.keys():
                    del self.objs[key]
                else:
                    print("** no instance found **")

    def do_all(self, line):
        "Displays the textual representations of all objects,
        either filtered by class name or for all objects.
        Example: $ all BaseModel or $ all."

        Obj_List = []
        if not line:
            Obj_List = [obj.__str__() for obj in self.objs.values()]
            print(Obj_List)
        else:
            if line not in self.classes.keys():
                print("** class doesn't exist **")
            else:
                Obj_List = [
                        obj.__str__() for obj in self.objs.values()
                        if obj.__class__.__name__ == line
                        ]
                print(Obj_List)

    def do_update(self, line):
        "Modifies an object using its class name and ID by adding or modifying
        an attribute, and then saves the changes to the JSON file.
        Example: $ update BaseModel 1234-1234-1234 email "airbnb@mail.com"."

        _ARGS = line.split()

        if len(_ARGS) >= 4:
            if _ARGS[0] not in self.classes.keys():
                print("** class doesn't exist **")
            else:
                key = f"{_ARGS[0]}.{_ARGS[1]}"

                if key in self.objs.keys():
                    if self.Dict_Check == 1:
                        for j in range(2, len(_ARGS), 2):
                            setattr(self.objs[key], _ARGS[j], _ARGS[j + 1])
                    else:
                        _ARGS[2] = _ARGS[2].strip('"')
                        _ARGS[3] = _ARGS[3].strip('"')
                        setattr(self.objs[key], _ARGS[2], _ARGS[3])
                    self.objs[key].save()
                else:
                    print("** no instance found **")
        elif len(_ARGS) == 3:
            print("** value missing **")
        elif len(_ARGS) == 2:
            print("** attribute name missing **")
        elif len(_ARGS) == 1:
            print("** instance id missing **")
        else:
            print("** class name missing **")

        self.Dict_Check = 0

    def do_count(self, line):
        "Fetch the count of instances for a specific class."
        count = 0

        for obj in self.objs.values():
            if obj.__class__.__name__ == line:
                count += 1

        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()

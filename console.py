#!/usr/bin/python3
""" console """

def do_create(self, args):
    """Create a new instance of a class"""
    if not args:
        print("** class name missing **")
        return

    arg_list = args.split()
    class_name = arg_list[0]

    if class_name not in self.classes:
        print("** class doesn't exist **")
        return


    attr_dict = {}


    for arg in arg_list[1:]:

        key_value = arg.split('=')
        if len(key_value) != 2:
            continue
        key, value = key_value


        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('_', ' ')


        try:
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            pass


        attr_dict[key] = value

    new_instance = self.classes[class_name](**attr_dict)
    new_instance.save()
    print(new_instance.id)

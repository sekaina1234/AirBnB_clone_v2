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

    # Create a dictionary to store attribute key-value pairs
    attr_dict = {}

    # Iterate through the remaining arguments (key=value pairs)
    for arg in arg_list[1:]:
        # Split each argument into key and value
        key_value = arg.split('=')
        if len(key_value) != 2:
            continue
        key, value = key_value

        # Remove double quotes from string values and replace underscores with spaces
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('_', ' ')

        # Try to convert the value to int or float if possible
        try:
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            pass

        # Add the key-value pair to the attribute dictionary
        attr_dict[key] = value

    # Create a new instance of the class with the attribute dictionary
    new_instance = self.classes[class_name](**attr_dict)
    new_instance.save()
    print(new_instance.id)

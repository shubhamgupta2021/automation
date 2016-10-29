import sys


output_dict = {}


def dictionary_handler(name, data, parent_class, start=False):
    if start:
        class_name = parent_class
    else:
        class_name = name.title().replace("_", "")
        output_dict[parent_class] += "\t{} = {}()\n".format(name, class_name)
    if not start:
        output_dict[class_name] = """class {}(MappingSchema):\n""".format(class_name)
    for key, value in data.iteritems():
        handlers[type(value).__name__](key, value, class_name)


def string_handler(name, v, parent_class):
    output_dict[parent_class] += "\t{} = SchemaNode(String())\n".format(name)


def int_handler(name, v, parent_class):
    output_dict[parent_class] += "\t{} = SchemaNode(Integer())\n".format(name)


def list_handler(name, data, parent_class):
    if not name.endswith("s"):
        name += "s"
    class_name = name.title().replace("_", "")
    child_name = name[:-1]
    child_class_name = class_name[:-1]
    output_dict[parent_class] += "\t{} = {}()\n".format(name, class_name)
    class_data = """class {}(SequenceSchema):\n\t{} = {}()""".format(class_name, child_name, child_class_name)
    output_dict[class_name] = class_data
    output_dict[child_class_name] = """class {}(MappingSchema):\n""".format(child_class_name)
    for item in data:
        class_data = handlers[type(item).__name__](child_name, item, child_class_name )


def convert_to_colander(a):
    output_file_path = sys.argv[1]
    output_dict['Response'] = "class Response(colander):\n"
    handlers[type(a).__name__]("", a, "Response", start=True)
    f = open(output_file_path, "w")
    for d in output_dict.itervalues():
        f.write(d)
        f.write("\n\n")
    f.close()


handlers = { "dict": dictionary_handler,
             "list": list_handler,
             "str": string_handler,
             "int": int_handler,
           }

convert_to_colander(a)

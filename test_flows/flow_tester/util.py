def class_name_from_file(file_name):
    file_name = file_name.replace("_ns", "").replace(".py", "")
    name = "".join([c.capitalize() for c in file_name.split("_")])
    return name + "Flow"

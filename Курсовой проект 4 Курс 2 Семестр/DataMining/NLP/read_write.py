def write_mas(filename, data_list):
    with open(filename, 'w') as file:
        file.writelines("%s\n" % data for data in data_list)


def read_mas(filename):
    with open(filename, 'r') as file:
        result = [line.rstrip() for line in file.readlines()]
    return result

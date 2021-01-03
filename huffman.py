from collections import OrderedDict


all_freq = {}
ordered_freq = OrderedDict()

# TODO: Alters the target file directly. Add method later for copying target file.
# file_name = str(input("Input file name:"))
file_name = "test.txt"


def load_file():
    with open(file_name, mode="r") as file:
        file_contents_list = file.readlines()
        # print(file_contents_list)
        file_contents = "".join(file_contents_list)
        # print(file_contents)
        # print(len(file_contents))
        # string = file_contents.replace("\n", "")
        # print(string)
        # f = json.loads(file_contents)
        # type(f)
        return file_contents


# def count_freq():
#     global all_freq
#     string = load_file()

#     for i in string:
#         if i in all_freq:
#             all_freq[i] += 1
#         else:
#             all_freq[i] = 1
#     return all_freq


# Counts frequency of character in string and returns an ordereddict whose indices are
# priorities.
# def count_freq():
#     global ordered_freq
#     string = load_file()

#     for i in string:
#         if i in ordered_freq:
#             ordered_freq[i] += 1
#         else:
#             ordered_freq[i] = 1
#     return ordered_freq, list(ordered_freq.items())[1]


def count_freq():
    global ordered_freq
    global all_freq
    string = load_file()
    count = 1

    for i in string:
        if i in all_freq:
            all_freq[i] += 1
        else:
            all_freq[i] = 1

    for key, value in all_freq.items():
        all_freq[key] = str(value)

    while all_freq != ordered_freq:
        for key, value in all_freq.items():
            if int(value) == count:
                ordered_freq.update({f"{key}": f"{value}"})
        count += 1

    return ordered_freq


list(ordered_freq.values)

# def dict_to_list():
#     new_list = []
#     for key, value in all_freq.items():
#         new_list.append("{} {}".format(key, value))
#     return new_list


# a = OrderedDict([("a", "1"), ("c", "3"), ("b", "2")])
# b = {"a": "1", "b": "2", "c": "3"}


# print(load_file())
print(count_freq())
# print(dict_to_list())

# count = 1

# new_list = dict_to_list()
# for i in new_list:
#     if i[2] > count:
#         count += 1
#     if i[2] == count:

#     print(i[2])
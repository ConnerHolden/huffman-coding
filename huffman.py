from collections import OrderedDict
import pickle


# all_freq = {[("a", "23"), ("b", "62"), ("h", "48")]}
all_freq = {}

# ordered_freq = {[("a", "23"), ("h", "48"), ("b", "62")]}
ordered_freq = OrderedDict()

# feeder_dict = {[("ah", 71)]}
feeder_dict = OrderedDict([("", 0)])

# bit_dict = {[("a", 110), ("h", 100), ("b", 01)]}
bit_dict = OrderedDict()

# TODO: Alters the target file directly. Add method later for copying target file.
# file_name = str(input("Input file name:"))
file_name = "test.txt"


def load_file():
    with open(file_name, mode="r") as file:
        file_contents_list = file.readlines()
        file_contents = "".join(file_contents_list)
        return file_contents


def copy_file():
    copied_file = load_file()
    return copied_file


# def write_file():


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


def more_than_one(dictionary):
    try:
        return bool(list(dictionary)[1])
    except IndexError:
        return False


def check_repeating(string):
    for character in string:
        string_check = string.replace(character, "")
        if character in string_check:
            return False
        else:
            return True


def continue_building():
    try:
        if len(list(feeder_dict)[-1]) + len(list(feeder_dict)[-2]) < len(
            list(ordered_freq)
        ):
            return True
        else:
            return False
    except IndexError:
        return False


def update_feeder_dict(dict1, i1, dict2, i2):
    feeder_dict[
        f"{list(dict1)[i1]}{list(dict2)[i2]}"
    ] = f"{int(list(dict1.values())[i1]) + int(list(dict2.values())[i2])}"


def assign_new_bit_code(key, code):
    bit_dict.update({f"{key}": f"{code}"})


bit_counter = 0


def assign_bit_code(dict, i):
    counter = 0
    global bit_counter
    for character in list(dict)[i]:
        if character in bit_dict:
            bit_dict.update({f"{character}": f"{bit_counter % 2}{bit_dict[character]}"})
        else:
            assign_new_bit_code(character, bit_counter % 2)
        counter += 1
    counter = 0
    bit_counter += 1
    if bit_counter % 2 == 0:
        bit_counter = 0


def del_dict_items(dict1, i1, dict2, i2):
    del dict1[list(dict1)[i1]]
    if dict2 == dict1:
        del dict2[list(dict2)[i1]]
    else:
        del dict2[list(dict2)[i2]]


ordered_freq_counter = 0
feeder_dict_counter = 1
feeder_dict_index = 0


def feeder_counter(dict1, dict2):
    global ordered_freq_counter
    global feeder_dict_counter
    global feeder_dict_index

    if dict1 == ordered_freq:
        ordered_freq_counter += 1
        feeder_dict_index += 1
    else:
        feeder_dict_counter += 1
        feeder_dict_index += 1
    if dict2 == ordered_freq:
        ordered_freq_counter += 1
    else:
        feeder_dict_counter += 1


def feeder(dict1, i1, dict2, i2):
    update_feeder_dict(dict1, i1, dict2, i2)
    assign_bit_code(dict1, i1)
    assign_bit_code(dict2, i2)
    feeder_counter(dict1, dict2)


def huffman_tree():
    global ordered_freq_counter
    global feeder_dict_counter
    global feeder_dict_index

    for key, value in ordered_freq.items():
        if continue_building() or (len(list(feeder_dict)) == (1 or 2)):
            if len(list(feeder_dict)) == 1:
                feeder(
                    ordered_freq,
                    ordered_freq_counter,
                    ordered_freq,
                    ordered_freq_counter + 1,
                )
            else:
                if ordered_freq_counter >= 1 and ordered_freq_counter != len(
                    list(ordered_freq)
                ):
                    if int(
                        feeder_dict[list(feeder_dict)[feeder_dict_counter]]
                    ) != 0 and int(
                        feeder_dict[list(feeder_dict)[feeder_dict_counter]]
                    ) <= (
                        int(ordered_freq[list(ordered_freq)[ordered_freq_counter]])
                        or int(
                            ordered_freq[list(ordered_freq)[ordered_freq_counter + 1]]
                        )
                    ):
                        feeder(
                            feeder_dict,
                            feeder_dict_counter,
                            ordered_freq,
                            ordered_freq_counter,
                        )
                    else:
                        feeder(
                            ordered_freq,
                            ordered_freq_counter,
                            ordered_freq,
                            ordered_freq_counter + 1,
                        )
                else:
                    if ordered_freq_counter != len(list(ordered_freq)):
                        feeder(
                            feeder_dict,
                            feeder_dict_counter,
                            ordered_freq,
                            ordered_freq_counter,
                        )
                    else:
                        feeder(
                            feeder_dict,
                            feeder_dict_counter,
                            feeder_dict,
                            feeder_dict_counter + 1,
                        )
        else:
            break


def write_huffman():
    copied_file = copy_file()
    copied_file = list(copied_file)
    for index, item in enumerate(copied_file):
        for key, value in bit_dict.items():
            if item == key:
                copied_file[index] = value
    return "".join(copied_file)


def binstr_to_int():
    return int(write_huffman(), 2)


# def conversion():
#     string = load_test()
#     string = list(string)
#     for index, item in enumerate(string):
#         for key, value in bit_dict.items():
#             if item == key:
#                 string[index] = value
#     return "".join(string)


# write test.txt to new file in huffman codes, then convert to int, then write that


# print(count_freq())
# print(ordered_freq_counter + 1)
# feeder(ordered_freq, ordered_freq_counter, ordered_freq, ordered_freq_counter + 1)
# print(ordered_freq)
# print(feeder_dict)
# print(bit_dict)
# feeder(ordered_freq, ordered_freq_counter, feeder_dict, feeder_dict_counter)
# print(ordered_freq)
# print(feeder_dict)
# print(bit_dict)
# feeder(ordered_freq, ordered_freq, feeder_dict, feeder_dict_counter)
# print(ordered_freq)
# print(feeder_dict)
# print(bit_dict)


print(count_freq())
huffman_tree()
print(ordered_freq)
print(feeder_dict)
print(bit_dict)
print(write_huffman())
print(binstr_to_int())
# print(copy_file(load_file()))
pickling_on = open("test.pickle", "wb")
pickle.dump(binstr_to_int(), pickling_on)
pickling_on.close()
# def load_test():
#     with open("testcopy.txt", mode="r") as file:
#         file_contents_list = file.readlines()
#         testcopy = "".join(file_contents_list)
#         return testcopy


# print(conversion())
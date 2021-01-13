from collections import OrderedDict
import pickle
import time
from os import system
from sys import getsizeof
import timeit
import sys


# all_freq = {[("a", "23"), ("b", "62"), ("h", "48")]}
all_freq = {}

# ordered_freq = {[("a", "23"), ("h", "48"), ("b", "62")]}
ordered_freq = OrderedDict()

# feeder_dict = {[("ah", "71")]}
feeder_dict = OrderedDict([("", "0")])

# bit_dict = {[("a", "110"), ("h", "100"), ("b", "01")]}
bit_dict = OrderedDict()

bit_counter = 0
ordered_freq_counter = 0
feeder_dict_counter = 1
feeder_dict_index = 0


def load_file(target):
    with open(target, mode="r") as file:
        file_contents_list = file.readlines()
        file_contents = "".join(file_contents_list)
        return file_contents


def count_freq(target):
    string = load_file(target)
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


def freq(dict):
    if dict == feeder_dict:
        dict_counter = feeder_dict_counter
    else:
        dict_counter = ordered_freq_counter
    return int(dict[list(dict)[dict_counter]])


class Feeder:
    def __init__(self, dict1, i1, dict2, i2):
        self.update_feeder_dict(dict1, i1, dict2, i2)
        self.assign_bit_code(dict1, i1)
        self.assign_bit_code(dict2, i2)
        self.feeder_counter(dict1, dict2)

    def update_feeder_dict(self, dict1, i1, dict2, i2):
        feeder_dict[
            f"{list(dict1)[i1]}{list(dict2)[i2]}"
        ] = f"{int(list(dict1.values())[i1]) + int(list(dict2.values())[i2])}"

    def assign_bit_code(self, dict, i):
        counter = 0
        global bit_counter
        for character in list(dict)[i]:
            if character in bit_dict:
                bit_dict.update(
                    {f"{character}": f"{bit_counter % 2}{bit_dict[character]}"}
                )
            else:
                bit_dict.update({f"{character}": f"{bit_counter % 2}"})
            counter += 1
        counter = 0
        bit_counter += 1
        if bit_counter % 2 == 0:
            bit_counter = 0

    def feeder_counter(self, dict1, dict2):
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


# TODO: prefixes are not unique :(
def huffman_tree():
    for key, value in ordered_freq.items():
        feeder_len = len(list(feeder_dict))
        ordered_len = len(list(ordered_freq))
        if continue_building() or feeder_len == 1:
            if feeder_len == 1:
                Feeder(
                    ordered_freq,
                    ordered_freq_counter,
                    ordered_freq,
                    ordered_freq_counter + 1,
                )
            else:
                if ordered_freq_counter >= 1 and ordered_freq_counter != ordered_len:
                    if freq(feeder_dict) != 0 and freq(feeder_dict) <= (
                        freq(ordered_freq) or freq(ordered_freq) + 1
                    ):
                        Feeder(
                            feeder_dict,
                            feeder_dict_counter,
                            ordered_freq,
                            ordered_freq_counter,
                        )
                    else:
                        Feeder(
                            ordered_freq,
                            ordered_freq_counter,
                            ordered_freq,
                            ordered_freq_counter + 1,
                        )
                else:
                    if ordered_freq_counter != ordered_len:
                        Feeder(
                            feeder_dict,
                            feeder_dict_counter,
                            ordered_freq,
                            ordered_freq_counter,
                        )
                    else:
                        Feeder(
                            feeder_dict,
                            feeder_dict_counter,
                            feeder_dict,
                            feeder_dict_counter + 1,
                        )
        else:
            break


def return_huffman_integer(target):
    file = load_file(target)
    file = list(file)
    for index, item in enumerate(file):
        for key, value in bit_dict.items():
            if item == key:
                file[index] = value
                break
        if index % 1000 == 0:
            completion = 100 * index / len(file)
            print("{:.3f}% ({}/{})".format(completion, index, len(file)))
            time.sleep(0.001)
        # if index % 20 == 0:
        #     completion = int(20 * index / len(file))
        #     sys.stdout.write("\r[%s%s]" % ("#" * completion, " " * (20 - completion)))
        #     sys.stdout.flush()
    file = "".join(file)
    huffman_integer = int(file, 2)
    return huffman_integer


def write_bin(target="test.txt", destination="test.pickle"):
    count_freq(target)
    huffman_tree()
    pickling_on = open(destination, "wb")
    pickle.dump(return_huffman_integer(target), pickling_on)
    pickling_on.close()


write_bin()
from collections import OrderedDict
import pickle
import time
from os import system
from sys import getsizeof
from timeit import default_timer as timer
import sys


# Unordered frequency of every character in a file.
# all_freq = {[("a", "23"), ("b", "62"), ("h", "48")]}
all_freq = {}

# Ordered frequency of every character in a file.
# ordered_freq = {[("a", "23"), ("h", "48"), ("b", "62")]}
ordered_freq = OrderedDict()

# The summed freqencies of character combinations, fed to this dict from ordered_freq.
# feeder_dict = {[("ah", "71")]}
feeder_dict = OrderedDict([("", "0")])

# The bit codes associated with each character.
# bit_dict = {[("a", "110"), ("h", "100"), ("b", "01")]}
bit_dict = OrderedDict()

# All counters are indices, except <bit_counter>.
# All counters are zero-based indices except <feeder_dict_counter> (eliminates some IndexError).
bit_counter = 0
ordered_freq_counter = 0
feeder_dict_counter = 1
feeder_dict_index = 0


def load_file(target):
    """Reads file and returns its contents as a string."""
    with open(target, mode="r") as file:
        file_contents_list = file.readlines()
        file_contents = "".join(file_contents_list)
        return file_contents


def count_freq(target):
    """Counts the frequency (value) of each character (key) in <string> by adding them
    to <all_freq>.
    Orders characters by increasing frequency in <ordered_freq>.
    Returns <ordered_freq>.
    """
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
    """Determines whether all of <ordered_freq> is represented in the final two entries
    of <feeder_dict>, i.e. the huffman tree will be complete once these final two
    entries are combined.
    """
    try:
        if len(list(feeder_dict)[-1]) + len(list(feeder_dict)[-2]) < len(
            list(ordered_freq)
        ):
            return True
        else:
            return False
    except IndexError:
        return False


def freq(dict, dict_counter):
    """Returns the frequency (value) of a character (key) in an OrderedDict."""
    return int(dict[list(dict)[dict_counter]])


class Feeder:
    def __init__(self, dict1, i1, dict2, i2):
        """Abstraction of huffman tree structure into a 'dictionary-combination loop'."""
        self.update_feeder_dict(dict1, i1, dict2, i2)
        self.assign_bit_code(dict1, i1)
        self.assign_bit_code(dict2, i2)
        self.feeder_counter(dict1, dict2)

    def update_feeder_dict(self, dict1, i1, dict2, i2):
        """Adds a new entry to <feeder_dict> by combining two dict entries,

        e.g., two <ordered_freq> entries:
            {[("a", "23"), ("h", "48"), ("b", "62")]}
                -> {[("ah", "71")]}
        e.g., one <ordered_freq> and one <feeder_dict> entry:
            {[("a", "23"), ("h", "48"), ("b", "62")]} and {[("ah", "71")]}
                -> {[("ah", "71"), ("ahb", "133")]}
        e.g., two <feeder_dict> entries:
            {[("ah", "71"), ("ahb", "133"), ("tn", "290")]}
                -> {[("ah", "71"), ("ahb", "133"), ("tn", "290"), ("ahbtn", "423")]}

        Note that keys are concatenated and values are summed as integers.
        """
        feeder_dict[
            f"{list(dict1)[i1]}{list(dict2)[i2]}"
        ] = f"{int(list(dict1.values())[i1]) + int(list(dict2.values())[i2])}"

    def assign_bit_code(self, dict, i):
        """Updates bit code of a character to reflect its position in huffman tree."""
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
        """Counts position in <ordered_freq> and <feeder_dict>. I haven't been able to
        implement a simpler system in which entries are removed from their dictionary
        once they are combined into a new entry. So it's important to keep track of the
        feeder system's state.
        """
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


def huffman_tree():
    """Builds huffman tree using an overly complicated abstraction of its tree-node
    structure into this sweet loop of nested conditionals.
    """
    for key, value in ordered_freq.items():
        feeder_len = len(list(feeder_dict))
        ordered_len = len(list(ordered_freq))
        # Are we at the end of building the tree or are we at the beginning?
        if continue_building() or feeder_len == 1:
            # Are we at the beginning of building the tree?
            if feeder_len == 1:
                Feeder(
                    ordered_freq,
                    ordered_freq_counter,
                    ordered_freq,
                    ordered_freq_counter + 1,
                )
            else:
                # Have we gone through the entire <ordered_freq> dict yet?
                if ordered_freq_counter >= 1 and ordered_freq_counter != ordered_len:
                    # Is the frequency of a character ...
                    # (in <feeder_dict> at the point <feeder_dict_counter>) ...
                    # (1) greater than 0, and (2) less than or equal to that of another character ...
                    # (in <ordered_freq> at the point <ordered_freq_counter>)?
                    #
                    # i.e., would the next smallest combination be between ...
                    # a feeder_dict entry and an ordered_freq entry?
                    if freq(feeder_dict, feeder_dict_counter) != 0 and freq(
                        feeder_dict, feeder_dict_counter
                    ) <= freq(ordered_freq, ordered_freq_counter):
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
                    # Have we gone through the entire <ordered_freq> dict yet?
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
        # Since we are at the end, we should combine the final two <feeder_dict> entries.
        else:
            Feeder(
                feeder_dict,
                feeder_dict_counter,
                feeder_dict,
                feeder_dict_counter + 1,
            )
            break


def return_huffman_integer(target):
    """Compression.
    Replaces characters from a target file with their respective bit codes from <bit_dict>.
    Treats this sequence of bit codes, which is a string, as base two binary, converting it into an integer.
    """
    file = load_file(target)
    file = list(file)
    for index, item in enumerate(file):
        for key, value in bit_dict.items():
            if item == key:
                file[index] = value
                break
        if index % 1000 == 0:
            completion = int(20 * index / len(file))
            readout = "\r[%s%s]" % ("▯" * completion, " " * (20 - completion)) + " ({}/{}) {:.2f}%".format(index, len(file), 100 * index / len(file))
            sys.stdout.write(readout)
            sys.stdout.flush()
            time.sleep(0.001)
    time.sleep(0.1)
    sys.stdout.write("\r[%s%s]" % ("▯" * 20, " " * 0) + " ({}/{}) 100.00%".format(len(file), len(file)))
    sys.stdout.flush()
    file = "1" + "".join(file)
    huffman_integer = int(file, 2)
    bin_int = int(file, 2)
    bin_str = bin(bin_int)
    return huffman_integer


def write_bin(target="test.txt", destination="test.pickle"):
    """Writes <huffman_integer> and its <bit_dict> (so it can be decompressed later) to a new binary file."""
    count_freq(target)
    huffman_tree()
    pickling_on = open(destination, "wb")
    pickle.dump(return_huffman_integer(target), pickling_on)
    pickle.dump(bit_dict, pickling_on)
    pickling_on.close()


start = timer()
write_bin("test.txt")
end = timer()
print("\nruntime: {:.2f}s".format(end - start))
import pickle
from functools import reduce
import time
import sys
from timeit import default_timer as timer


def format_output(input):
    output = str(input)
    if len(output) > 50:
        return f"{output[0:25]} ... {output[-24:]} {type(input)}"
    else:
        return f"{output} {type(input)}"


def read_bin(target="test.pickle", destination="testcompare.txt"):
    pickling_on = open(target, "rb")
    huffman_integer = pickle.load(pickling_on)
    bit_dict = pickle.load(pickling_on)
    l = list(bin(huffman_integer))
    del l[0:3]

    n = []

    for index, item in enumerate(l):
        for key, value in bit_dict.items():
            if item == value:
                n.append(key)
                break
        # Major bottleneck?
        if item != value:
            l[index + 1] = f"{l[index] + l[index + 1]}"
        if index % 1000 == 0:
            completion = int(20 * index / len(l))
            readout = "\r[%s%s]" % ("▯" * completion, " " * (20 - completion)) + " ({}/{}) {:.2f}%".format(index, len(l), 100 * index / len(l))
            sys.stdout.write(readout)
            sys.stdout.flush()
            time.sleep(0.0001)
    time.sleep(0.1)
    sys.stdout.write("\r[%s%s]" % ("▯" * 20, " " * 0) + " ({}/{}) 100.00%".format(len(l), len(l)))
    sys.stdout.flush()

    file = "".join(n)
    new_file = open(destination, "w")
    new_file.write(file)
    new_file.close()
    

start = timer()
read_bin()
end = timer()
print("\nruntime: {:.2f}s".format(end - start))
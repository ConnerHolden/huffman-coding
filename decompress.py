import pickle
from functools import reduce
import time
import sys
from timeit import default_timer as timer
import getopt


def read_bin(target="test.dat", destination="testcompare.txt"):
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


def main(argv):
    target = ""
    destination = ""
    try:
        opts, args = getopt.getopt(argv,"ht:d:",["tfile=","dfile="])
    except getopt.GetoptError:
        print("compress.py -t <targetfile> -d <destinationfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("compress.py -t <targetfile> -d <destinationfile>")
            sys.exit()
        elif opt in ("-t", "--tfile"):
            targetfile = arg
        elif opt in ("-d", "--dfile"):
            destinationfile = arg
    start = timer()
    read_bin(targetfile, destinationfile)
    end = timer()
    print("\nruntime: {:.2f}s".format(end - start))


if __name__ == "__main__":
   main(sys.argv[1:])
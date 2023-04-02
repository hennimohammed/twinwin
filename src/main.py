from IO import reader
import sys
from os import listdir

if __name__ == '__main__':

    dataset = sys.argv[1]

    for instance in listdir(dataset):
        n, m, edges = reader.read_file(dataset+instance)

        print(n)
        print(m)
        print(edges)



"""Generate Random String CSV

Usage:
  generate_str_csv.py <filename> <length>
"""
from random import choice, randint
import string
from docopt import docopt
import os


def generate_str_csv(length=100000, filename='random_strs_1.csv'):
    if 'local_csv_tests' not in filename:
        path = os.path.join('local_csv_tests', filename)
    else:
        path = filename

    dirs, fname = os.path.split(path)
    if dirs and not os.path.exists(dirs):
        os.makedirs(dirs)

    with open(path, 'w+') as f:
        for i in range(length):
            if i % 10000 == 0:
                print 'wrote element {} to file {}'.format(i + 1, path)
            f.write(''.join([choice(string.digits) for _ in range(6)]) + '\n')
        print 'finished writing {} elements to file '.format(length, path)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    generate_str_csv(filename=arguments['<filename>'], length=int(arguments['<length>']))

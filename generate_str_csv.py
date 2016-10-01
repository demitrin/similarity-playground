"""Generate Random String CSV

Usage:
  generate_str_csv.py <filename> <length>
"""
from random import choice, randint
import string
from docopt import docopt
def generate_str_csv(length=100000, filename='random_strs_1.csv'):
    with open(filename, 'w+') as f:
        for i in range (length):
            if i % 10000 == 0:
                print 'wrote element {} to file {}'.format(i + 1, filename)
            f.write(''.join([choice(string.digits) for _ in range(randint(2, 8))]) + '\n')
        print 'finished writing {} elements to file '.format(length, filename)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    generate_str_csv(filename=arguments['<filename>'], length=int(arguments['<length>']))

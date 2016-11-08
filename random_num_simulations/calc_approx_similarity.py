"""Calculate Approximate Similarity

Usage:
  calc_approx_similarity.py <file1> <file2>
"""
import csv

from docopt import docopt

from datasketch import MinHash


def calc_approx_similarity(file1, file2):
    m1, m2 = MinHash(num_perm=128), MinHash(num_perm=128)

    with open(file1, 'r') as f:
        reader = csv.reader(f)
        for val in reader:
            m1.update(val[0])

    with open(file2, 'r') as f:
        reader = csv.reader(f)
        for val in reader:
            m2.update(val[0])

    print 'finished approx calc'
    return m1.jaccard(m2)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print calc_approx_similarity(file1=arguments['<file1>'], file2=arguments['<file2>'])

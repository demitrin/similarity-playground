"""Calculate Real Similarity

Usage:
  calc_exact_similarity.py <file1> <file2>
"""
import csv

from docopt import docopt


def calc_real_similarity(file1, file2):
    hashed_value_counts = {}
    with open(file1, 'r') as f:
        reader = csv.reader(f)
        data1 = list(reader)
        data1 = map(lambda arr: arr[0], data1)
        for val in data1:
            hashed_value_counts[val] = hashed_value_counts.get(val, 0) + 1

    len_intersection = 0
    with open(file2, 'r') as f:
        reader = csv.reader(f)
        data2 = list(reader)
        data2 = map(lambda arr: arr[0], data2)
        for val in data2:
            if val in hashed_value_counts:
                hashed_value_counts[val] = hashed_value_counts[val] - 1
                if hashed_value_counts[val] == 0:
                    del (hashed_value_counts[val])

                len_intersection += 1
    s1 = set(data1)
    s2 = set(data2)
    actual_jaccard = float(len(s1.intersection(s2))) / float(len(s1.union(s2)))
    return actual_jaccard


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print calc_real_similarity(file1=arguments['<file1>'], file2=arguments['<file2>'])

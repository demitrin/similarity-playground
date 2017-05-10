"""Calculate Approximate Similarity

Usage:
  calc_and_store_exact_similarities.py <directory> <storage_path>
"""

import csv
import glob
import json
from multiprocessing import Pool

import os
from docopt import docopt
from threading import Lock
import gc

mutex = Lock()


def calc_exact_similarities(set_name, sets, storage_path):
    similarities = {}
    s1 = sets[set_name]
    for sname, s2 in sets.iteritems():
        if sname != set_name:
            actual_jaccard = float(len(s1.intersection(s2))) / float(len(s1.union(s2)))
            similarities[sname] = actual_jaccard
    mutex.acquire()
    with open(storage_path, 'ab') as f:
        print 'wrote to {}'.format(set_name)
        json.dump({set_name: similarities}, f)
    mutex.release()
    gc.collect()


def async_calc_exact_similarity(set_name__sets__storage_path):
    return calc_exact_similarities(*set_name__sets__storage_path)


def calc_and_store_exact_similarities(directory, storage_path):
    filenames = glob.glob(os.path.join(directory, '*.csv'))
    sets = {}
    for filename in filenames:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            reader.next()  # skip header row
            for row in reader:
                for i in range(len(row)):
                    set_name = '{}-{}'.format(i, filename)
                    if set_name not in sets:
                        sets[set_name] = set()
                    sets[set_name].add(row[i])

    pool = Pool(4)
    args = map(lambda set_name: (set_name, sets, storage_path), sets.keys())
    pool.map(async_calc_exact_similarity, args)
    pool.close()
    pool.join()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    calc_and_store_exact_similarities(arguments['<directory>'], arguments['<storage_path>'])

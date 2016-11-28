"""Calculate Approximate Similarity

Usage:
  calc_and_store_exact_similarities.py <mitdwh_path>
"""

import csv
import glob
import json
from multiprocessing import Pool

import os
from docopt import docopt


def calc_exact_similarities(set_name, sets):
    similarities = {}
    s1 = sets[set_name]
    for sname, s2 in sets.iteritems():
        if sname != set_name:
            actual_jaccard = float(len(s1.intersection(s2))) / float(len(s1.union(s2)))
            similarities[sname] = actual_jaccard
    return set_name, similarities


def async_calc_exact_similarity(set_name__sets):
    return calc_exact_similarities(*set_name__sets)


def calc_and_store_exact_similarities(mitdwh_path):
    filenames = glob.glob(os.path.join(mitdwh_path, '*.csv'))
    sets = {}
    for filename in filenames:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                for i in range(len(row)):
                    set_name = '{}-{}'.format(i, filename)
                    if set_name not in sets:
                        sets[set_name] = set()
                    sets[set_name].add(row[i])

    pool = Pool(4)
    args = map(lambda set_name: (set_name, sets), sets.keys())
    similarities = pool.map(async_calc_exact_similarity, args)
    pool.close()
    pool.join()

    similarities_as_json = {}
    for set_name, similarity_map in similarities:
        similarities_as_json[set_name] = similarity_map

    with open('exact_mitwdwh_similarities.json', 'w+') as f:
        f.write(json.dumps(similarities_as_json))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    calc_and_store_exact_similarities(arguments['<mitdwh_path>'])

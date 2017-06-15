"""Store exact similar sets

Usage:
  calc_and_store_exact_similarities.py  
"""

import glob
import json

import os
from docopt import docopt


def calc_and_store_exact_thresholds(similarity_filename):
    with open(similarity_filename, 'r') as f:
        exact_similarities = json.load(f)
    thresholds = [.1, .3, .5, .7, .9]
    similar_sets = [set() for _ in range(len(thresholds))]
    for s1, similarities in exact_similarities.iteritems():
        for s2, similarity in similarities.iteritems():
            for i in range(len(thresholds)):
                if similarity >= thresholds[i]:
                    similar_sets[i].add(frozenset([s1, s2]))

    sets_as_lists = [[] for _ in range(len(thresholds))]
    for i in range(len(thresholds)):
        for pair in similar_sets[i]:
            sets_as_lists[i].append(list(pair))

    if '/' in similarity_filename:
        storage_path = os.path.join(*similarity_filename.split('/')[:-1])
    else:
        storage_path = ''

    for i in range(len(thresholds)):
        storage_file = os.path.join(storage_path, 'similar_sets-{}.json'.format(str(thresholds[i])))
        print 'storing to ' + storage_file
        with open(storage_file, 'w') as f:
            f.write(json.dumps(sets_as_lists[i]))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    for filename in glob.glob('exact_mitdwh_similarities.json'):
        calc_and_store_exact_thresholds(filename)

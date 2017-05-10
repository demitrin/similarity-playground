"""Calc and store precision and recall

Usage:
  calc_precision_recall.py 
"""
import gc
import glob
import json
import os

import re
from docopt import docopt


def get_as_set(data_as_arrays):
    data = set()
    for arr in data_as_arrays:
        data.add(frozenset(arr))
    return data


def calc_precision_recall(input_file, threshold):
    print 'working on file {}'.format(input_file)
    with open(input_file, 'r') as f:
        approx_set_json = json.load(f)
        approx_set = get_as_set(approx_set_json)
    with open('/Users/demitri/superurop/playground/dataset_simulations/mitdwh_exact/exact_similar_sets-{}.json'.format(
            threshold), 'r') as f:
        exact_set_json = json.load(f)
        exact_set = get_as_set(exact_set_json)

    precision = float(len(approx_set.intersection(exact_set))) / len(approx_set)
    recall = float(len(approx_set.intersection(exact_set))) / len(exact_set)
    with open('precision_recall.txt', 'a') as f:
        f.write('------------' + os.path.join(*input_file.split('/')[:-1]) + '  threshold  {}'.format(str(threshold)) + '----------------\n')
        f.write('({0:.5f}, {1:.5f})   \n'.format(precision, recall))

if __name__ == '__main__':
    arguments = docopt(__doc__)
    for filename in glob.glob('*/*/similar_sets*.json'):
        threshold = float(re.search('\d\.\d', filename).group())
        if threshold < 1:
            calc_precision_recall(filename, threshold)
            gc.collect()

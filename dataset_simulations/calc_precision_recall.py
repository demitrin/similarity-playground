"""Calc and store precision and recall

Usage:
  calc_precision_recall.py <input_folder> <output_filename>
"""

import json

import matplotlib.pyplot as plt
import numpy as np
from docopt import docopt
import os
import gc


def calc_precision_recall(input_folder, output_filename, threshold):
    print 'working on threshold {}'.format(threshold)
    approx_filename = os.path.join(input_folder, 'similar_sets-{}.json'.format(threshold))
    with open(approx_filename, 'r') as f:
        approx_set_json = json.load(f)

    with open('/Users/demitri/superurop/playground/dataset_simulations/mitdwh_exact/exact_similar_sets-{}.json'.format(threshold), 'r') as f:
        exact_set_json = json.load(f)

    json_to_store = {}
    for set_name, exact_results in exact_set_json.iteritems():
        approx_set = set(approx_set_json[set_name])
        exact_set = set(exact_results)
        if len(approx_set) == 0:
            precision = 1
        else:
            precision = float(len(approx_set.intersection(exact_set))) / len(approx_set)
        if len(exact_set) == 0:
            recall = 1
        else:
            recall = float(len(approx_set.intersection(exact_set))) / len(exact_set)
        json_to_store[set_name] = {
            'p': precision,
            'r': recall
        }

    with open(output_filename + str(threshold) + '.json', 'w+') as f:
        f.write(json.dumps(json_to_store))
    x = []
    y = []
    for p_r in json_to_store.itervalues():
        x.append(p_r['r'])
        y.append(p_r['p'])
    x = np.array(x)
    y = np.array(y)
    fig = plt.figure()
    plt.plot(x, y, 'ro')
    plt.axis([0, 1.2, 0, 1.2])
    plt.xlabel('recall')
    plt.ylabel('precision')
    fig.savefig(output_filename + str(threshold) + '.png')
    plt.close(fig)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    thresholds = [0.1, 0.3, 0.5, 0.7, 0.9]
    for threshold in thresholds:
        calc_precision_recall(arguments['<input_folder>'], arguments['<output_filename>'], threshold)
        gc.collect()

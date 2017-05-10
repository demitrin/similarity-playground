"""Calc and store precision and recall

Usage:
  calc_pr_spread.py 
"""
import gc
import glob
import json

import numpy as np
import os
import pandas as pd
import re
from docopt import docopt


def calc_pr_spread(input_folder, output_filename, pr_filename, threshold):
    with open(pr_filename, 'r') as f:
        pr_json = json.load(f)

    precision = np.array(map(lambda pr_obj: pr_obj['p'], pr_json.values()))
    recall = np.array(map(lambda pr_obj: pr_obj['r'], pr_json.values()))
    p = pd.Series(precision)
    r = pd.Series(recall)
    with open(os.path.join(input_folder, output_filename + str(threshold) + '.json'), 'w') as f:
        data = {
            'name': input_folder,
            'threshold': threshold,
            'precision': {
                'mean': p.mean(),
                'std': p.std()
            },
            'recall': {
                'mean': r.mean(),
                'std': r.std()
            }
        }
        f.write(json.dumps(data))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    for filename in glob.glob('*/*/p_r*.json'):
        input_folder = os.path.join(*filename.split('/')[:2])
        threshold_string = filename.split('/')[-1]
        threshold = float(re.search('\d.\d', threshold_string).group())
        if threshold > 1:
            print threshold_string

        calc_pr_spread(input_folder, 'pr_spread-', filename, threshold)
        gc.collect()

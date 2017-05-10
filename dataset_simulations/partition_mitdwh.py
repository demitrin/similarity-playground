"""Calculate Approximate Similarity

Usage:
  partition_mitdwh.py <mitdwh_path>
"""

import gc
import hashlib
import time

from docopt import docopt

from base_mitdwh import base_mitdwh
from datasketch import MinHashOPHR


def partition_mitdwh(mitdwh_path, filename, hash_func, k):
    base_mitdwh(mitdwh_path, MinHashOPHR, filename, hash_func, k)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    hashes = [(hashlib.sha1, 'sha1')]
    k_vals = [32, 64, 128]
    for k in k_vals:
        for i in range(len(hashes)):
            start_time = time.time()
            partition_mitdwh(arguments['<mitdwh_path>'],
                             'partition_mitdwh_10/k_{}/{}-{}-data.json'.format(k, k, hashes[i][1]),
                        hashes[i][0], k)
            with open('partition_mitdwh_10/k_{}/{}-{}-time.txt'.format(k, k, hashes[i][1]), 'w+') as f:
                f.write("--- %s seconds ---" % (time.time() - start_time))
            gc.collect()

"""Calculate Approximate Similarity

Usage:
  ophr_mitdwh.py <mitdwh_path>
"""

import gc
import hashlib
import time

from docopt import docopt

from base_mitdwh import base_mitdwh
from datasketch import MinHashOPHR


def ophr_mitdwh(mitdwh_path, filename, hash_func, k):
    base_mitdwh(mitdwh_path, MinHashOPHR, filename, hash_func, k)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    # hashes = [(hashlib.sha1, 'sha1'), (hashlib.sha256, 'sha256'), (hashlib.sha512, 'sha512'), (hashlib.md5, 'md5')]
    hashes = [(hashlib.sha1, 'sha1')]
    k_vals = [128, 256, 512]
    for k in k_vals:
        for i in range(len(hashes)):
            start_time = time.time()
            ophr_mitdwh(arguments['<mitdwh_path>'], 'ophr_minhash_mitdwh/k_{}/{}-{}-data.json'.format(k, k, hashes[i][1]),
                        hashes[i][0], k)
            with open('ophr_minhash_mitdwh/k_{}/{}-{}-time.txt'.format(k, k, hashes[i][1]), 'w+') as f:
                f.write("--- %s seconds ---" % (time.time() - start_time))
            gc.collect()

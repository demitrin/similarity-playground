"""Get similar columns using reg MinHash

Usage:
  reg_mitdwh.py <mitdwh_path>
"""

from docopt import docopt

from base_lsh_mitdwh import base_lsh_mitdwh
from datasketch import MinHash
import hashlib
import time
import gc


def reg_lsh_mitdwh(mitdwh_path, filename, hash_func, k):
    base_lsh_mitdwh(mitdwh_path, MinHash, filename, hash_func, k)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    # hashes = [(hashlib.sha1, 'sha1'), (hashlib.sha256, 'sha256'), (hashlib.sha512, 'sha512'), (hashlib.md5, 'md5')]
    hashes = [(hashlib.sha256, 'sha256')]
    k_vals = [128, 256, 512]
    for k in k_vals:
        for i in range(len(hashes)):
            start_time = time.time()
            reg_lsh_mitdwh(arguments['<mitdwh_path>'], 'reg_lsh_mitdwh/k_{}/{}-{}-data-'.format(k, k, hashes[i][1]), hashes[i][0], k)
            with open('reg_lsh_mitdwh/k_{}/{}-{}-time.txt'.format(k, k, hashes[i][1]), 'w+') as f:
                f.write("--- %s seconds ---" % (time.time() - start_time))
            gc.collect()

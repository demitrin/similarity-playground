"""Calculate Approximate Similarity

Usage:
  ophr_lash_mitdwh.py <mitdwh_path>
"""

from docopt import docopt

from base_mitdwh import base_mitdwh
from datasketch import MinHashOPHR
import hashlib
import time


def ophr_lsh_mitdwh(mitdwh_path, filename, hash_func, hashstr):
    base_mitdwh(mitdwh_path, MinHashOPHR, filename, hash_func, hashstr=hashstr)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    hashes = [(hashlib.sha1, 'sha1'), (hashlib.sha256, 'sha256'), (hashlib.sha512, 'sha512'), (hashlib.md5, 'md5')]
    for i in range(len(hashes)):
        start_time = time.time()
        ophr_lsh_mitdwh(arguments['<mitdwh_path>'], 'outputs/ophr_minhash_pt2-{}.json'.format(str(i)), *hashes[i])
        with open('outputs/ophr_minhash_pt2-time-{}.txt'.format(i), 'w+') as f:
            f.write("--- %s seconds ---" % (time.time() - start_time))

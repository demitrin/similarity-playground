"""Calculate Approximate Similarity

Usage:
  reg_lsh_mitdwh.py <mitdwh_path>
"""

from docopt import docopt

from base_mitdwh import base_mitdwh
from datasketch import MinHash
import hashlib


def reg_lsh_mitdwh(mitdwh_path, filename, hash_func):
    base_mitdwh(mitdwh_path, MinHash, filename, hash_func)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    hashes = [hashlib.sha1, hashlib.sha256, hashlib.sha512, hashlib.md5]
    for i in range(len(hashes)):
        reg_lsh_mitdwh(arguments['<mitdwh_path>'], 'outputs/reg_minhash-{}.json'.format(str(i)), hashes[i])

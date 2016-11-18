"""Calculate Approximate Similarity

Usage:
  reg_lsh_mitdwh.py <mitdwh_path>
"""

from docopt import docopt

from base_lsh_mitdwh import base_lsh_mitdwh
from datasketch import MinHash


def reg_lsh_mitdwh(mitdwh_path, filename):
    base_lsh_mitdwh(mitdwh_path, MinHash, filename)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    for i in range(10):
        reg_lsh_mitdwh(arguments['<mitdwh_path>'], 'reg_minhash-{}.json'.format(str(i)))

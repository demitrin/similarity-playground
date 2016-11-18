"""Calculate Approximate Similarity

Usage:
  ophr_lash_mitdwh.py <mitdwh_path>
"""

from docopt import docopt

from base_lsh_mitdwh import base_lsh_mitdwh
from datasketch import MinHashOPHR


def ophr_lsh_mitdwh(mitdwh_path, filename):
    base_lsh_mitdwh(mitdwh_path, MinHashOPHR, filename)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    for i in range(10):
        ophr_lsh_mitdwh(arguments['<mitdwh_path>'], 'ophr_minhash-{}.json'.format(str(i)))

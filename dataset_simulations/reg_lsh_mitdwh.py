"""Calculate Approximate Similarity

Usage:
  reg_lsh_mitdwh.py <mitdwh_path>
"""

from docopt import docopt

from base_lsh_mitdwh import base_lsh_mitdwh
from datasketch import MinHash


def ophr_lsh_mitdwh(mitdwh_path):
    base_lsh_mitdwh(mitdwh_path, MinHash)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    ophr_lsh_mitdwh(arguments['<mitdwh_path>'])

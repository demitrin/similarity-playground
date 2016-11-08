"""Calculate Approximate Similarity

Usage:
  ophr_lash_mitdwh.py <mitdwh_path>
"""
import csv
import glob
import os

from docopt import docopt

from datasketch import MinHashOPHR, MinHashLSH


def ophr_lsh_mitdwh(mitdwh_path):
    ophr_minhashes = []
    for filename in glob.glob(os.path.join(mitdwh_path, '*.csv')):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            csv_minhashes = []
            for row in reader:
                if not csv_minhashes:
                    for i in range(len(row)):
                        csv_minhashes.append(MinHashOPHR())

                for i in range(len(row)):
                    csv_minhashes[i].update(row[i])

            for minhash in csv_minhashes:
                ophr_minhashes.append(minhash)

    lsh = MinHashLSH(threshold=.3)
    for i in range(len(ophr_minhashes)):
        lsh.insert(i, ophr_minhashes[i])

    for minhash in ophr_minhashes:
        print lsh.query(minhash)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    ophr_lsh_mitdwh(arguments['<mitdwh_path>'])

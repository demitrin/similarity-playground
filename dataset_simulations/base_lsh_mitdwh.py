import csv
import glob

import os

from datasketch import MinHashLSH


def base_lsh_mitdwh(mitdwh_path, minhash_cls):
    minhashes = []
    for filename in glob.glob(os.path.join(mitdwh_path, '*.csv')):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            csv_minhashes = []
            for row in reader:
                if not csv_minhashes:
                    for i in range(len(row)):
                        csv_minhashes.append(minhash_cls())

                for i in range(len(row)):
                    csv_minhashes[i].update(row[i])

            for minhash in csv_minhashes:
                minhashes.append(minhash)

    lsh = MinHashLSH(threshold=.3)
    for i in range(len(minhashes)):
        lsh.insert(i, minhashes[i])

    for minhash in minhashes:
        print lsh.query(minhash)

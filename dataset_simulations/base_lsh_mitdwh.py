import csv
import glob
from multiprocessing import Pool

import os

from datasketch import MinHashLSH


def get_csv_minhashes(filename, minhash_cls):
    with open(filename, 'r') as f:
        print 'working on file ' + filename
        reader = csv.reader(f)
        csv_minhashes = []
        for row in reader:
            if not csv_minhashes:
                for i in range(len(row)):
                    csv_minhashes.append(minhash_cls())

            for i in range(len(row)):
                csv_minhashes[i].update(row[i])
    return csv_minhashes


def async_get_csv_minhashes(filename__minhash_cls):
    return get_csv_minhashes(*filename__minhash_cls)


def base_lsh_mitdwh(mitdwh_path, minhash_cls):
    pool = Pool(4)
    args = map(lambda filename: (filename, minhash_cls), glob.glob(os.path.join(mitdwh_path, '*.csv')))
    csv_minhashes = pool.map(async_get_csv_minhashes, args)
    minhashes = reduce(lambda csv_minhash1, csv_minhash2: csv_minhash1 + csv_minhash2, csv_minhashes, [])
    lsh = MinHashLSH(threshold=.3)
    for i in range(len(minhashes)):
        lsh.insert(i, minhashes[i])

    for minhash in minhashes:
        print lsh.query(minhash)

    pool.close()
    pool.join()

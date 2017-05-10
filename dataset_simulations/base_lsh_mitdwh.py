import csv
import glob
import json

import os

from datasketch import MinHashLSH


def get_csv_minhashes(filename, minhash_cls, hash_func, minhashes, k):
    with open(filename, 'r') as f:
        print 'working on file ' + filename
        reader = csv.reader(f)
        row = reader.next()  # skip header row
        row_len = len(row)
        for row in reader:
            for i in xrange(row_len):
                set_name = '{}-{}'.format(i, filename)
                if set_name not in minhashes:
                    minhashes[set_name] = minhash_cls(k, hashobj=hash_func)
                minhashes[set_name].update(row[i])


def query_lsh(set_name, minhash, lsh, results):
    result = lsh.query(minhash)
    result.remove(set_name)
    results[set_name] = result


def base_lsh_mitdwh(mitdwh_path, minhash_cls, json_file_name, hash_func, k):
    files = glob.glob(os.path.join(mitdwh_path, '*.csv'))

    minhashes = {}
    for filename in files:
        get_csv_minhashes(filename, minhash_cls, hash_func, minhashes, k)

    thresholds = [.1, .3, .5, .7, .9]
    for threshold in thresholds:
        lsh = MinHashLSH(threshold=threshold, num_perm=k)

        for set_name, minhash in minhashes.iteritems():
            lsh.insert(set_name, minhash)

        results = {}
        for set_name, minhash in minhashes.iteritems():
            query_lsh(set_name, minhash, lsh, results)
        with open(json_file_name + str(threshold) + '.json', 'w+') as f:
            f.write(json.dumps(results))

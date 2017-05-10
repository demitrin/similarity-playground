import csv
import glob
import json

import os


def get_csv_minhashes(filename, minhash_cls, hash_func, hashstr, minhashes, k):
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


def calc_jaccard_similarity(set_name, minhashes, similarities):
    similarities_for_set = {}
    s1_minhash = minhashes[set_name]
    for sname, minhash in minhashes.iteritems():
        if sname != set_name:
            similarities_for_set[sname] = s1_minhash.jaccard(minhash)

    similarities[set_name] = similarities_for_set


def base_mitdwh(mitdwh_path, minhash_cls, json_file_name, hash_func, k, hashstr=None):
    files = glob.glob(os.path.join(mitdwh_path, '*.csv'))
    minhashes = {}
    for filename in files:
        get_csv_minhashes(filename, minhash_cls, hash_func, hashstr, minhashes, k)

    similarities_as_json = {}
    for set_name in minhashes:
        calc_jaccard_similarity(set_name, minhashes, similarities_as_json)

    with open(json_file_name, 'w+') as f:
        f.write(json.dumps(similarities_as_json))

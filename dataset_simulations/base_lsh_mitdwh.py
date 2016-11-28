import csv
import glob
import json
from multiprocessing import Pool

import os


def get_csv_minhashes(filename, minhash_cls, hash_func, hashstr):
    with open(filename, 'r') as f:
        print 'working on file ' + filename
        reader = csv.reader(f)
        csv_minhashes = []
        for row in reader:
            if not csv_minhashes:
                for i in range(len(row)):
                    set_name = '{}-{}'.format(i, filename)
                    if hashstr:
                        csv_minhashes.append((minhash_cls(hashobj=hash_func, hashstr=hashstr), set_name))
                    else:
                        csv_minhashes.append((minhash_cls(hashobj=hash_func), set_name))

            for i in range(len(row)):
                csv_minhashes[i][0].update(row[i])
    return csv_minhashes


def async_get_csv_minhashes(filename__minhash_cls__hash_func__hashstr):
    return get_csv_minhashes(*filename__minhash_cls__hash_func__hashstr)


def calc_jaccard_similarity(set_name, minhashes):
    similarities = {}
    s1_minhash = minhashes[set_name]
    for sname, minhash in minhashes.iteritems():
        if sname != set_name:
            similarities[sname] = s1_minhash.jaccard(minhash)

    return set_name, similarities


def async_calc_jaccard_similarity(set_name__minhashes):
    return calc_jaccard_similarity(*set_name__minhashes)


def base_lsh_mitdwh(mitdwh_path, minhash_cls, json_file_name, hash_func, hashstr=None):
    pool = Pool(4)
    args = map(lambda filename: (filename, minhash_cls, hash_func, hashstr), glob.glob(os.path.join(mitdwh_path, '*.csv')))
    csv_minhashes = pool.map(async_get_csv_minhashes, args)
    minhashes_as_json = {}
    for minhashes in csv_minhashes:
        for minhash, set_name in minhashes:
            minhashes_as_json[set_name] = minhash

    args = map(lambda set_name: (set_name, minhashes_as_json), minhashes_as_json.keys())
    similarities = pool.map(async_calc_jaccard_similarity, args)
    pool.close()
    pool.join()

    similarities_as_json = {}
    for set_name, similarity_map in similarities:
        similarities_as_json[set_name] = similarity_map

    with open(json_file_name, 'w+') as f:
        f.write(json.dumps(similarities_as_json))

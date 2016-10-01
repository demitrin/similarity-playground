"""Calculate Bucketed Approximate Similarity

Usage:
  calc_bucketed_approx_similarity.py <file1> <file2> <num_buckets>
"""
import csv
from docopt import docopt
from datasketch import MinHash

def get_bucketnum_for_val(val, num_buckets):
    return hash(val) % num_buckets

def get_set_from_reader(reader):
    return set(map(lambda row: row[0], list(reader)))

def calc_bucketed_approx_similarity(file1, file2, num_buckets=3):
    minhash_buckets1 = [MinHash(num_perm=128) for _ in range(num_buckets)]
    minhash_buckets2 = [MinHash(num_perm=128) for _ in range(num_buckets)]

    file1_set_buckets_len = [0 for _ in range(num_buckets)]
    file2_set_buckets_len = [0 for _ in range(num_buckets)]
    with open(file1, 'r') as f:
        reader = csv.reader(f)
        file1_set = get_set_from_reader(reader)
        for val in file1_set:
            bucket_num = get_bucketnum_for_val(val, num_buckets)
            minhash_for_val = minhash_buckets1[bucket_num]
            minhash_for_val.update(val)
            file1_set_buckets_len[bucket_num] += 1

    with open(file2, 'r') as f:
        reader = csv.reader(f)
        file2_set = get_set_from_reader(reader)
        for val in file2_set:
            bucket_num = get_bucketnum_for_val(val, num_buckets)
            minhash_for_val = minhash_buckets2[bucket_num]
            minhash_for_val.update(val)
            file2_set_buckets_len[bucket_num] += 1
    
    unweighted_similarities = []
    weighted_similarities = []
    for i in range(num_buckets):
        unweighted_similarities.append(minhash_buckets1[i].jaccard(minhash_buckets2[i]))

        file1_weight = float(file1_set_buckets_len[i]) / float(len(file1_set))
        file2_weight = float(file2_set_buckets_len[i]) / float(len(file2_set))
        weighted_similarities.append(unweighted_similarities[i] * (file1_weight + file2_weight) / 2)
    
    # print unweighted_similarities
    # print weighted_similarities
    return sum(weighted_similarities)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print calc_bucketed_approx_similarity(
            file1=arguments['<file1>'], 
            file2=arguments['<file2>'],
            num_buckets=arguments['<num_buckets>'] or 3
            )

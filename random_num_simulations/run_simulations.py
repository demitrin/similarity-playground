"""Run Similarity Simulations

Usage:
  run_simulations.py <num_sets> <size_of_sets> <num_buckets>
"""
import datetime
from multiprocessing import Pool

import os
from docopt import docopt

from calculate_similarities import calculate_similarities
from generate_str_csv import generate_str_csv


def get_file_names(num_sets):
    return ['set{}.csv'.format(i + 1) for i in range(num_sets)]


def get_directory_name():
    return 'simulation_sets-{}'.format(
        datetime.datetime.now().strftime('%m-%d_%H-%M')
    )


def async_calc_similarities(file1_file2_num_buckets):
    print 'got call to async similarities'
    return calculate_similarities(*file1_file2_num_buckets)


def async_generate_str_csv(size_of_sets__file_name):
    return generate_str_csv(*size_of_sets__file_name)


def get_similarity_error(similarities, approx_similarity_key):
    return map(lambda similarity: abs(1 - (similarity[approx_similarity_key]
                                           / similarity['exact_similarity'])), similarities)


def run_similarity_simulations(num_sets, size_of_sets, num_buckets):
    LOCAL_CSV_TESTS = 'local_csv_tests'
    pool = Pool(4)

    # get file names
    working_dir = os.path.join(LOCAL_CSV_TESTS, get_directory_name())
    file_names = map(lambda file_name: os.path.join(working_dir, file_name), get_file_names(num_sets))
    dirs, fname = os.path.split(file_names[0])
    if dirs and not os.path.exists(dirs):
        os.makedirs(dirs)

    # create random datasets for files
    args = map(lambda file_name: (size_of_sets, file_name), file_names)
    pool.map(async_generate_str_csv, args)

    # for each pair of datasets, calculate similarities
    args = []
    for i in range(num_sets):
        for j in range(i + 1, num_sets):
            args.append((file_names[i], file_names[j], num_buckets))

    similarities = pool.map(async_calc_similarities, args)
    pool.close()
    pool.join()

    approx_similarities_errors = get_similarity_error(similarities, 'approx_similarity')
    bucketed_approx_similarities_errors = get_similarity_error(similarities, 'bucketed_approx_similarity')
    ophr_similarities_errors = get_similarity_error(similarities, 'ophr_similarity')
    approx_similarity_str = 'Average approx similarity error {}'.format(
        sum(approx_similarities_errors) / len(approx_similarities_errors))
    bucketed_approx_similarity_str = 'Average bucketed approx similarity error {}'.format(
        sum(bucketed_approx_similarities_errors) / len(bucketed_approx_similarities_errors))
    ophr_similarities_errors = 'Average OPHR similarity error {}'.format(
        sum(ophr_similarities_errors) / len(ophr_similarities_errors))

    output_filename = os.path.join(working_dir, 'output.txt')
    with open(output_filename, 'w+') as f:
        f.write(approx_similarity_str + '\n')
        f.write(bucketed_approx_similarity_str + '\n')
        f.write(ophr_similarities_errors + '\n')
        print 'wrote outputs to {}'.format(output_filename)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    num_sets = int(arguments['<num_sets>'])
    size_of_sets = int(arguments['<size_of_sets>'])
    num_buckets = int(arguments['<num_buckets>'])
    run_similarity_simulations(num_sets, size_of_sets, num_buckets)

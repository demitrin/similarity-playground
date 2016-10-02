"""Run Similarity Simulations

Usage:
  run_simulations.py <num_sets> <size_of_sets> <num_buckets>
"""
import datetime
import os
from docopt import docopt
from generate_str_csv import generate_str_csv
from calculate_similarities import calculate_similarities


def get_file_names(num_sets):
    return ['set{}.csv'.format(i + 1) for i in range(num_sets)]


def get_directory_name(num_sets, size_of_sets, num_buckets):
    return 'simulation_sets-{}_size-{}_buckets-{}_date-{}'.format(
        num_sets,
        size_of_sets,
        num_buckets,
        datetime.datetime.now().strftime('%m-%d_%H-%M')
    )


def run_similarity_simulations(num_sets, size_of_sets, num_buckets):
    LOCAL_CSV_TESTS = 'local_csv_tests'
    # get file names
    working_dir = os.path.join(LOCAL_CSV_TESTS, get_directory_name(num_sets, size_of_sets, num_buckets))
    file_names = map(lambda file_name: os.path.join(working_dir, file_name), get_file_names(num_sets))

    # create random datasets for files
    for file_name in file_names:
        generate_str_csv(size_of_sets, file_name)

    # for each pair of datasets, calculate similarities
    similarities = []
    for i in range(num_sets):
        for j in range(i + 1, num_sets):
            similarities.append(calculate_similarities(file_names[i], file_names[j], num_buckets))

    approx_similarities_errors = map(lambda similarity: abs(1 - (similarity['approx_similarity'] / similarity['exact_similarity'])), similarities)
    bucketed_approx_similarities_errors = map(lambda similarity: abs(1 - (similarity['bucketed_approx_similarity'] / similarity['exact_similarity'])), similarities)
    print 'Average approx similarity error {}'.format(sum(approx_similarities_errors) / len(approx_similarities_errors))
    print 'Average bucketed approx similarity error {}'.format(sum(bucketed_approx_similarities_errors) / len(bucketed_approx_similarities_errors))

if __name__ == '__main__':
    arguments = docopt(__doc__)
    num_sets = int(arguments['<num_sets>'])
    size_of_sets = int(arguments['<size_of_sets>'])
    num_buckets = int(arguments['<num_buckets>'])
    run_similarity_simulations(num_sets, size_of_sets, num_buckets)

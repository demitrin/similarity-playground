"""Calculate All Similarities

Usage:
  calculate_similarities.py <file1> <file2> <num_buckets>
"""
from docopt import docopt
from calc_bucketed_approx_similarity import calc_bucketed_approx_similarity
from calc_approx_similarity import calc_approx_similarity
from calc_exact_similarity import calc_real_similarity
from calc_ophr_similarity import calc_ophr_similarity


def calculate_similarities(file1, file2, num_buckets):
    # print 'Input files: {}, {}'.format(file1, file2)
    # print 'Calculating Exact, Approximate, and Approximate with {} Buckets Jaccard Similarities'.format(num_buckets)

    # print 'Calculating Exact Jaccard Similarity....'
    exact_similarity = calc_real_similarity(file1, file2)
    # print exact_similarity

    # print 'Calculating Approximate Jaccard Similarity....'
    approx_similarity = calc_approx_similarity(file1, file2)
    # print approx_similarity

    # print 'Calculating Approximate Jaccard Similarity with {} buckets....'.format(num_buckets)
    bucketed_approx_similarity = calc_bucketed_approx_similarity(file1, file2, num_buckets)
    # print bucketed_approx_similarity

    ophr_similarity = calc_ophr_similarity(file1, file2)
    return {
        'exact_similarity': exact_similarity,
        'approx_similarity': approx_similarity,
        'bucketed_approx_similarity': bucketed_approx_similarity,
        'ophr_similarity': ophr_similarity
    }


if __name__ == '__main__':
    arguments = docopt(__doc__)
    file1 = arguments['<file1>']
    file2 = arguments['<file2>']
    num_buckets = int(arguments['<num_buckets>']) or 3
    calculate_similarities(file1, file2, num_buckets)

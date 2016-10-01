
"""Calculate All Similarities

Usage:
  calculate_similarities.py <file1> <file2> <num_buckets>
"""
import csv
from docopt import docopt
from calc_bucketed_approx_similarity import calc_bucketed_approx_similarity
from calc_approx_similarity import calc_approx_similarity
from calc_exact_similarity import calc_real_similarity


if __name__ == '__main__':
    arguments = docopt(__doc__)
    file1=arguments['<file1>']
    file2=arguments['<file2>']
    num_buckets=int(arguments['<num_buckets>']) or 3
    print 'Input files: {}, {}'.format(file1, file2)
    print 'Calculating Exact, Approximate, and Approximate with {} Buckets Jaccard Similarities'.format(num_buckets) 

    print 'Calculating Exact Jaccard Similarity....'
    print calc_real_similarity(file1, file2)

    print 'Calculating Approximate Jaccard Similarity....'
    print calc_approx_similarity(file1, file2)

    print 'Calculating Approximate Jaccard Similarity with {} buckets....'.format(num_buckets)
    print calc_bucketed_approx_similarity(file1, file2, num_buckets)

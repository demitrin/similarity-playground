"""Calculate Average Error

Usage:
  calc_average_error.py <approx_glob_pattern> <exact_similarity_file>
"""
import glob
import json

from docopt import docopt


def get_similarity_error(approx_similarity, exact_similarity):
    if approx_similarity == 0 and exact_similarity == 0:
        return 0.
    if exact_similarity == 0:
        return None
    return abs(1 - float(approx_similarity) / exact_similarity)


def calc_average_error(glob_pattern, exact_filename):
    with open(exact_filename, 'r') as f:
        exact_similarity_json = json.load(f)

    for filename in glob.glob(glob_pattern):
        print 'working on file ' + filename
        with open(filename, 'r') as f:
            similarity_errors = []
            approx_similarity_json = json.load(f)
            for k1, sets in approx_similarity_json.iteritems():
                for k2, similarity in sets.iteritems():
                    similarity_errors.append(get_similarity_error(similarity, exact_similarity_json[k1][k2]))
            with open(filename.replace('json', 'txt'), 'w+') as f2:
                print 'writing error for ' + filename
                pruned_similarity_errors = filter(lambda error: error is not None, similarity_errors)
                f2.write(str(sum(pruned_similarity_errors) / len(pruned_similarity_errors)))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    calc_average_error(arguments['<approx_glob_pattern>'], arguments['<exact_similarity_file>'])

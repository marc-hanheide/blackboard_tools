import argparse
import numpy as np
from glob import glob
from difflib import unified_diff
from pprint import pprint

# def levenshteinDistance(s1, s2):
#     if len(s1) > len(s2):
#         s1, s2 = s2, s1

#     distances = range(len(s1) + 1)
#     for i2, c2 in enumerate(s2):
#         distances_ = [i2+1]
#         for i1, c1 in enumerate(s1):
#             if c1 == c2:
#                 distances_.append(distances[i1])
#             else:
#                 distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
#         distances = distances_
#     return distances[-1]

def levenshtein(source, target):
    if len(source) < len(target):
        return levenshtein(target, source)

    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)

    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + 1

        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s))

        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1)

        previous_row = current_row

    return previous_row[-1]

parser = argparse.ArgumentParser(description='compute similarity')
parser.add_argument('glob',
                    help='path glob pattern')

args = parser.parse_args()

files = glob(args.glob)

distances = np.zeros((len(files), len(files))) + 1

c1 = 0
for fn1 in files:
    c2 = 0
    for fn2 in files:
        if not fn1 == fn2:
            with file(fn1, 'r') as f1, file(fn2, 'r') as f2:
                t1 = f1.readlines()
                t2 = f2.readlines()
                diff = unified_diff(t1, t2, n=0)
                diff = list(diff)
                #    print "  %s <->  %s = %d" % (fn1, fn2, len(d))
                #pprint(diff)
                distances[c1, c2] = (float(len(diff)) /
                                     (len(t1) + len(t2)))
                # distances[c1, c2] = 1.0 - (float(levenshtein(t1, t2)) /
                #                            np.max([len(t1), len(t2)]))
        c2 += 1
    m = np.min(distances[c1, :])
    n = np.argmin(distances[c1, :])
    print "%s => %s %f" % (fn1, files[n], m)
    c1 += 1


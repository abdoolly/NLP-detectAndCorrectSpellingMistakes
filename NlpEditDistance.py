from __future__ import division
from __future__ import print_function

from nltk import*

def _edit_dist_init(len1, len2):
    lev = []
    for i in range(len1):
        lev.append([0] * len2)  # initialize 2D array to zero
    for i in range(len1):
        lev[i][0] = i           # column 0: 0,1,2,3,4,...
    for j in range(len2):
        lev[0][j] = j           # row 0: 0,1,2,3,4,...
    return lev


def _edit_dist_step(lev, i, j, s1, s2, substitution_cost=1, transpositions=False):
    c1 = s1[i - 1]
    c2 = s2[j - 1]

    # skipping a character in s1
    a = lev[i - 1][j] + 1
    # skipping a character in s2
    b = lev[i][j - 1] + 1
    # substitution
    c = lev[i - 1][j - 1] + (substitution_cost if c1 != c2 else 0)

    # transposition
    d = c + 1  # never picked by default
    if transpositions and i > 1 and j > 1:
        if s1[i - 2] == c2 and s2[j - 2] == c1:
            d = lev[i - 2][j - 2] + 1

    # pick the cheapest
    lev[i][j] = min(a, b, c, d)


def edit_distance(s1, s2, substitution_cost=1, transpositions=False):
    # set up a 2-D array
    len1 = len(s1)
    len2 = len(s2)
    lev = _edit_dist_init(len1 + 1, len2 + 1)

    # iterate over the array
    for i in range(len1):
        for j in range(len2):
            _edit_dist_step(lev, i + 1, j + 1, s1, s2,
                            substitution_cost=substitution_cost, transpositions=transpositions)
    return lev[len1][len2]


def demo():

    # we'll use our dataset instead .
    edit_distance_examples = [
        ("rain", "shine"), ("abcdef", "acbdef"), ("language", "lnaguaeg"),
        ("language", "lnaugage"), ("language", "lngauage")]
    for s1, s2 in edit_distance_examples:
        print("Edit distance between '%s' and '%s':" % (s1, s2), edit_distance(s1, s2))
    for s1, s2 in edit_distance_examples:
        print("Edit distance with transpositions between '%s' and '%s':" % (s1, s2), edit_distance(s1, s2, transpositions=True))

    s1 = set([1, 2, 3, 4])
    s2 = set([3, 4, 5])
    print("s1:", s1)
    print("s2:", s2)


if __name__ == '__main__':
    demo()
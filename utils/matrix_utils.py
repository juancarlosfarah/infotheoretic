__author__ = 'juancarlosfarah'

import numpy as np


def reduce(base, data):
    """
    Reduce a 2D matrix to an array given its base.
    :param base: Base of original data.
    :param data: 2D matrix with original data.
    :return: Reduced array.
    """
    rows = len(data)
    columns = len(data[0])
    combined_values = []
    for r in range(rows):
        combined_row_value = 0
        multiplier = 1
        for c in range(columns - 1, -1, -1):
            # Add in the contribution from each row.
            combined_row_value += data[r][c] * multiplier
            multiplier *= base
        combined_values.append(combined_row_value)

    return combined_values


def test_reduce():
    d0 = np.array([[0, 0, 0, 0, 0, 1, 1, 0],
                   [1, 1, 1, 0, 0, 1, 1, 0],
                   [1, 1, 1, 0, 0, 1, 1, 0],
                   [0, 0, 1, 0, 1, 1, 1, 0],
                   [1, 1, 1, 0, 1, 0, 1, 1],
                   [0, 0, 1, 0, 1, 1, 1, 0]])

    d1 = [[0, 0, 0, 0, 0, 1, 1, 0],
          [1, 1, 1, 0, 0, 1, 1, 0],
          [1, 1, 1, 0, 0, 1, 1, 0],
          [0, 0, 1, 0, 1, 1, 1, 0],
          [1, 1, 1, 0, 1, 0, 1, 1],
          [0, 0, 1, 0, 1, 1, 1, 0]]

    # Should print out [26, 26, 31, 0, 7, 61, 63, 2]
    print reduce(2, d0.T)

    d1 = np.array(d1).T
    d1 = d1.tolist()
    d1_reduced = reduce(2, d1)
    zipped = zip(d1_reduced, d1)
    zipped.sort(key=lambda k: k[0])
    d1 = [v[1] for v in zipped]
    print np.array(d1)
    print d1_reduced
    print d1
from itertools import chain

ini_list = [[1, 2, 3],
            [3, 6, 7],
            [7, 5, 4]]

flattened_list = list(chain.from_iterable(ini_list))

print(2 in flattened_list)
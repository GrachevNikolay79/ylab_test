import itertools


def bananas(s):
    result = set()

    for comb in itertools.combinations(range(len(s)), len(s) - 6):
        arr = list(s)
        for i in comb:
            arr[i] = '-'
        candidate = ''.join(arr)

        if candidate.replace('-', '') == 'banana':
            result.add(candidate)

    return result

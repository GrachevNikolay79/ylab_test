from functools import reduce


def count_find_num(primes_l: list, limit: int) -> list:
    base_num = reduce((lambda a, b: a * b), primes_l, 1)
    if base_num > limit:
        return []

    nums = [base_num]
    for i in primes_l:
        for n in nums:
            num = n * i
            while (num <= limit) and (num not in nums):
                nums.append(num)
                num *= i

    return [len(nums), max(nums)]

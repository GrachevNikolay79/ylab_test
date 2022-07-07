from ex_01 import simple_cache, simple_cache_all_arg
from ex_02 import decorator
'''
@simple_cache фактически годится только для этой (или такой же функции) 
'''


@simple_cache
def multiplier(number: int):
    print('i\'m a multiplier!', end=' ')
    return number * 2


'''
@simple_cache_all_arg годится для разных функций,с разным количеством и разными аргументами,
но построение ключа может убить всю выгоду от кэширования, к тому же если в параметрах передать 
одни и теже значения, но по разному то будут разные ключи и будут промахи кэша
'''


@simple_cache_all_arg
def multiplier_all_arg(number: int, add: int = 1):
    print('i\'m a multiplier!', end=' ')
    return number * 2 + add


@decorator(call_count=10, start_sleep_time=1, factor=2, border_sleep_time=5)
def fn_ex_02(n):
    return n*2


if __name__ == '__main__':
    print('\n --== Задание 1 ==-- ')
    print('\n\t@simple_cache:')
    for i in range(5):
        print("first call: ", i, ' -> ', multiplier(i))

    for i in range(5):
        print("second call: ", i, ' -> ', multiplier(i))

    print('\n\n\t@simple_cache_all_arg:')
    print("по сути одни и те же данные передаются, но кэширование не всегда возможно")
    for i in range(3):
        print("first call (add=5, number=i): ", i, ' -> ', multiplier_all_arg(add=5, number=i))

    for i in range(3):
        print("second call (i, 5): ", i, ' -> ', multiplier_all_arg(i, 5))

    for i in range(3):
        print("third call (i, add=5): ", i, ' -> ', multiplier_all_arg(i, add=5))

    for i in range(3):
        print("fourth call (number=i, add=5): ", i, ' -> ', multiplier_all_arg(number=i, add=5))

    print('\n\n --== Задание 2 ==-- \n')
    fn_ex_02(5)

def simple_cache(func):
    cache = {}

    def wrapper(number: int):
        if number not in cache:
            cache[number] = func(number)
        return cache[number]

    return wrapper


def simple_cache_all_arg(func):
    cache = {}

    def wrapper(*args, **kwargs):
        #нужен уникальный ключ, лучшего как-то не придумалось
        #получилось не оптимально, т.к. f(1) и f(number=1) это два разных ключа,
        #зато более универсально
        number = ' '.join((str(i) for i in args))
        number = number + ' '.join((str(i) for k, i in kwargs.items()))
        if number not in cache:
            cache[number] = func(*args, **kwargs)
        return cache[number]

    return wrapper


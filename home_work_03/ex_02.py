from time import sleep


def decorator(call_count=5, start_sleep_time=1, factor=2, border_sleep_time=10):
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            print('Кол-во запусков =', call_count)
            print('Начало работы')
            t = start_sleep_time
            for num_start in range(1, call_count+1):
                print('Запуск номер ', num_start, ' Ожидание: ', t, ' секунд.', end=' ')
                sleep(t)
                print('Результат декорируемой функций = ', func(*args, **kwargs))
                if t < border_sleep_time:
                    t = min(start_sleep_time * factor**num_start, border_sleep_time)

        return wrapper2
    return wrapper1

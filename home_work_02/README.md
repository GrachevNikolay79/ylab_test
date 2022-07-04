## Задание 1:
пример запуска:

        import random as rd
        import datetime as dt
        from ex_01 import salesman
        
        p = [(rd.randint(0, 50), rd.randint(0, 50)) for _ in range(15)]
        t1 = dt.datetime.now()
        
        salesman(p)
        
        t2 = dt.datetime.now()
        print("Elapsed time:{}".format(t2-t1))

## Задание 2
        python3 ./ex_02/main.py
        
                
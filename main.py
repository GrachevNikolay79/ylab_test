from ex_01 import domain_name
from ex_02 import int32_to_ip
from ex_03 import zeros
from ex_04 import bananas
from ex_05 import count_find_num


def check_exercises():
    assert domain_name("http://github.com/carbonfive/raygun") == "github"
    assert domain_name("http://www.zombie-bites.com") == "zombie-bites"
    assert domain_name("https://www.cnet.com") == "cnet"
    assert domain_name("http://google.com") == "google"
    assert domain_name("http://google.co.jp") == "google"
    assert domain_name("www.xakep.ru") == "xakep"
    assert domain_name("https://youtube.com") == "youtube"
    print("exercise 1: OK")

    assert int32_to_ip(2154959208) == "128.114.17.104"
    assert int32_to_ip(0) == "0.0.0.0"
    assert int32_to_ip(2149583361) == "128.32.10.1"
    print("exercise 2: OK")

    assert zeros(0) == 0
    assert zeros(6) == 1
    assert zeros(25) == 6
    assert zeros(30) == 7
    assert zeros(50) == 12
    print("exercise 3: OK")

    assert bananas("banann") == set()
    assert bananas("banana") == {"banana"}
    assert bananas("bbananana") == {"b-an--ana", "-banana--", "-b--anana", "b-a--nana", "-banan--a",
                                    "b-ana--na", "b---anana", "-bana--na", "-ba--nana", "b-anan--a",
                                    "-ban--ana", "b-anana--"}
    assert bananas("bananaaa") == {"banan-a-", "banana--", "banan--a"}
    assert bananas("bananana") == {"ban--ana", "ba--nana", "bana--na", "b--anana", "banana--", "banan--a"}
    print("exercise 4: OK")

    assert count_find_num([2, 3], 200) == [13, 192]
    assert count_find_num([2, 5], 200) == [8, 200]
    assert count_find_num([2, 3, 5], 500) == [12, 480]
    assert count_find_num([2, 3, 5], 1000) == [19, 960]
    assert count_find_num([2, 3, 47], 200) == []
    print("exercise 5: OK")


if __name__ == "__main__":
    check_exercises()

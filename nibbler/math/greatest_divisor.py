from typing import Iterable


def greatestDivisor(target: int, iterator: Iterable[int]):

    gd = 1
    
    for item in iterator:
        if target%item == 0:
            if item > gd:
                gd = item

    return gd

if __name__ == "__main__":

    items = [2, 5, 20, 50, 1000]

    target = 10

    print(greatestDivisor(target, items))

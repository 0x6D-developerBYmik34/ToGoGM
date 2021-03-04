from numbers import Number
from operator import sub
from typing import Iterable, Generator, Any


def diff_bet_adj(seq: Iterable[Number]) -> Generator[Number, Any, None]:
    buff = []
    for i in seq:
        buff.append(i)
        if len(buff) == 2:
            yield sub(*buff)
            buff.pop(0)


def num_sub_dif_bet_adj(num: Number, seq: Iterable[Number]):
    yield num
    for diff in diff_bet_adj(seq):
        num -= diff
        yield num


if __name__ == '__main__':
    test_lst = '''100 90 89 90 95 104 118 118 117 129 128 116 117 130 132 148 157 167 171 173 176 178 181 176 186 
    189 191 193 196 199 202 206 210 210 200 190179 165 155 146 137 125 129 114 108 104 98 94'''
    test_lst = [int(x) for x in test_lst.split(' ') if x.isdigit()]
    print(test_lst)
    print(list(diff_bet_adj(test_lst)))
    print(list(num_sub_dif_bet_adj(test_lst[0], test_lst)))
    print(list(num_sub_dif_bet_adj(44, test_lst)))

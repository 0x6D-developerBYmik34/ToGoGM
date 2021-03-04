from functools import partial
from numbers import Number
from typing import Iterable, Sequence, Tuple


def average_among_adj_args(seq: Iterable[Number], len_buff: int, extra_point_index: int):
    buff = []
    extra_point = None
    ep_index_null = extra_point_index == 0
    for n, i in enumerate(seq):

        if not ep_index_null and n >= extra_point_index and n % extra_point_index == 0:
            extra_point = i
        else:
            buff.append(i)

        if len(buff) == len_buff:
            if extra_point is not None:
                buff.append(extra_point)
                extra_point = None

            yield sum(buff) / len(buff)
            buff.clear()


def to_25(points: Sequence[Tuple[Number, Number]]):
    raw_points = points[1:-1]
    len_raw = (len(points) - 2)

    len_buff = len_raw // 23
    mod = len_raw % 23
    extra_p_index = len_raw // mod if mod else 0

    print(f'{len_buff=}, {mod=}, {extra_p_index=}, {len(points) - 2}')

    union_func_points = partial(average_among_adj_args, len_buff=len_buff, extra_point_index=extra_p_index)

    x_unit = union_func_points(i[0] for i in raw_points)
    y_unit = union_func_points(i[1] for i in raw_points)

    yield points[0]
    yield from zip(x_unit, y_unit)
    yield points[-1]

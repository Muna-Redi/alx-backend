#!/usr/bin/env python3
""" Pagination """

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ returns a tuple of start and end page """
    return ((page-1) * page_size, page_size * page)

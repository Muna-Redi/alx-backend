#!/usr/bin/env python3
""" Hypermedia del-resilient pagination """

import csv
import math
from typing import List, Dict


class Server:
    """
       Defining a Server class to paginate a
       database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """ Cached dataset """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """ returns an index sorted Dataset """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                x: dataset[x] for x in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None,
                        page_size: int = 10) -> Dict:

        if index is None:
            index = 0

        assert isinstance(index, int)
        assert 0 <= index < len(self.indexed_dataset())
        assert isinstance(page_size, int) and page_size > 0

        data = []
        nxt_index = index + page_size

        for content in range(index, nxt_index):
            if self.indexed_dataset().get(content):
                data.append(self.indexed_dataset()[content])
            else:
                content += 1
                nxt_index += 1

        return {
            'index': index,
            'data': data,
            'page_size': page_size,
            'next_index': nxt_index
        }

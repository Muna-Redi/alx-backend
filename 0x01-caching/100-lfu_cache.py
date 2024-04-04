#!/usr/bin/env python3
"""LFU Caching
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """A cache class implementing Least Frequency Used caching policy
    """
    order = {}

    def put(self, key, item):
        """Insert an item in the cache
        """
        if key is None or item is None:
            return

        if (len(self.cache_data) >= BaseCaching.MAX_ITEMS and
                key not in self.cache_data):
            discarded = self.remove()
            print("DISCARD: {}".format(discarded[0]))

        self.cache_data[key] = item
        self.update_count(key)

    def remove(self):
        """Evicts the Least Frequency used key and item
        """
        min_used = None

        # obtaining least ued item
        for key, val in self.order.items():
            if not min_used:
                min_used = key
                continue

            if val < self.order[min_used]:
                min_used = key

        # deleting first inserted item which is the least used
        for key, val in self.order.items():
            if val == self.cache_data[min_used]:
                min_used = key
                break

        item = self.cache_data.pop(min_used)

        self.order.pop(min_used)

        return min_used, item

    def update_count(self, key):
        """use-count update for a key
        """
        if key not in self.order:
            self.order[key] = 1
            return

        self.order[key] = self.order[key] + 1

    def get(self, key):
        """Fetching data from the cache
        """
        if key is None or key not in self.cache_data:
            return None

        self.update_count(key)
        return self.cache_data[key]

#!/usr/bin/env python3
""" Creates a class MRUCache that inherits
   from BaseCaching system:
"""


BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """_summary_
    """

    def __init__(self):
        """_summary_
        """
        super().__init__()
        self.keys_used = []

    def put(self, key, item):
        """_summary_

        Args:
                        key (_type_): _description_
                        item (_type_): _description_
        """
        if key is not None and item is not None:
            self.cache_data[key] = item
            if key not in self.keys_used:
                self.keys_used.append(key)
            else:
                self.keys_used.append(
                    self.keys_used.pop(self.keys_used.index(key)))
            if len(self.keys_used) > BaseCaching.MAX_ITEMS:
                discard = self.keys_used.pop(-2)
                del self.cache_data[discard]
                print('DISCARD: {:s}'.format(discard))

    def get(self, key):
        """return the value in self.cache_data linked to key

        Args:
                        key (_type_): _description_
        """
        if key is not None and key in self.cache_data.keys():
            self.keys_used.append(self.keys_used.pop(self.keys_used.index(key)))
            return self.cache_data.get(key)
        return None

# app/extractor/cache.py
from cachetools import LRUCache

class SessionCache:
    """
    Cache simples em memória (LRU) para respostas de PDFs.
    """
    def __init__(self, maxsize=256):
        self.cache = LRUCache(maxsize=maxsize)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def exists(self, key) -> bool:
        return key in self.cache

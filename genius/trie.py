#encoding:utf-8
from __future__ import unicode_literals


class TreeNode(object):

    def __init__(self):
        self.key = None
        self.value = None
        self.children = {}


class TrieTree(object):

    def __init__(self):
        self.root = TreeNode()

    def __setitem__(self, key, value):
        self.add(key, value)

    def __getitem__(self, key):
        cache = self.search(key)
        return cache[key]

    def get(self, key):
        cache = self.search(key)
        return cache.get(key)

    def add(self, key, value):
        node = self.root
        for char in key:
            if char not in node.children:
                child = TreeNode()
                child.key = key
                child.value = value
                node.children[char] = child
                node = child
            else:
                node = node.children[char]
        node.value = value

    def search(self, key):
        '''return all partially matched strings with the input key'''
        node = self.root
        matches = {}
        for char in key:
            if char not in node.children:
                break
            node = node.children[char]
            matches[node.key] = node.value
        return matches

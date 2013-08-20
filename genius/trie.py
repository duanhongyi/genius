#encoding:utf-8
from __future__ import unicode_literals
from .tools import StringHelper


class Word(object):

    def __init__(self, text, **kwargs):
        self.text = text
        self.freq = kwargs.get('freq', 0)
        self.tagging = kwargs.get('tagging', 'unknow')
        self.weight = kwargs.get('weight', 0)
        self.source = kwargs.get('source', 'system')
        self.marker = StringHelper.mark(text)

    def __repr__(self):
        return "u'%s'" % self.text.encode('unicode_escape')

    def __len__(self):
        return len(self.text)

    def __hash__(self):
        return self.text.__hash__()

    def __eq__(self, obj):
        if isinstance(obj, Word):
            return self.text == obj.text
        return obj == self.text


class TrieTree(object):

    class TreeNode(object):

        def __init__(self):
            self.value = None
            self.children = {}

    def __init__(self):
        self.root = self.TreeNode()

    def add(self, word):
        node = self.root
        key = word.text
        for char in key:
            if char not in node.children:
                child = self.TreeNode()
                child.value = word
                node.children[char] = child
                node = child
            else:
                node = node.children[char]
        node.value = word

    def search(self, key):
        '''return all partially matched strings with the input key'''
        node = self.root
        matches = set()
        for char in key:
            if char not in node.children:
                break
            node = node.children[char]
            if node.value:
                matches.add(node.value)
        return matches

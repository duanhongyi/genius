#encode:utf-8

from __future__ import unicode_literals

import os
from wapiti import Model
from genius.trie import TrieTree
from genius.word import Word

here = os.path.abspath(os.path.dirname(__file__))
library_path = os.path.join(here, 'library')


class ResourceLoader(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(
                ResourceLoader, cls).__new__(cls, *args, **kwargs)
            cls._instance._trie_tree = None
            cls._instance._crf_seg_model = None
            cls._instance._crf_pos_model = None
            cls._instance._break_table = None
        return cls._instance

    def load_crf_seg_model(self, path=None, **options):
        if not self._crf_seg_model:
            if path:
                options['model'] = path
            else:
                options['model'] = os.path.join(
                    library_path, "crf_seg_model.txt")
            if os.path.exists(options['model']):
                _crf_seg_model = Model(**options)
            else:
                e = IOError()
                e.errno = 2
                e.filename = options['model']
                e.strerror = "No such file or directory"
                raise e
            self._crf_seg_model = _crf_seg_model
        return self._crf_seg_model

    def load_crf_pos_model(self, path=None, **options):
        if not self._crf_pos_model:
            if path:
                options['model'] = path
            else:
                options['model'] = os.path.join(
                    library_path, "crf_pos_model.txt")
            if os.path.exists(options['model']):
                _crf_pos_model = Model(**options)
            else:
                e = IOError()
                e.errno = 2
                e.filename = options['model']
                e.strerror = "No such file or directory"
                raise e
            self._crf_pos_model = _crf_pos_model
        return self._crf_pos_model

    def load_trie_tree(self, path=None):
        if not self._trie_tree:
            trie_tree = TrieTree()
            if not path:
                path = library_path
            for node_path in os.listdir(path):
                if not node_path.endswith('.dic'):
                    continue
                node_path = os.sep.join([path, node_path])
                with open(node_path) as f:
                    for line in f:
                        word, tagging, freq = line.decode(
                            'utf-8').strip().split('\t')
                        trie_tree.add(word, Word(
                            word,
                            freq=freq,
                            tagging=tagging,
                        ))
            self._trie_tree = trie_tree
        return self._trie_tree

    def load_break_table(self, path=None):
        if not self._break_table:
            if not path:
                break_idx = os.path.join(library_path, "break.txt")
            else:
                break_idx = path
            tree = {}
            if not os.path.exists(break_idx):
                return
            with open(break_idx) as break_file:
                for line in break_file:
                    label = unicode(line, "utf-8").strip().split('\t')
                    tree[label[0]] = label[1:]
            self._break_table = tree
        return self._break_table

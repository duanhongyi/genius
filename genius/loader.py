#encode:utf-8

from __future__ import unicode_literals

import re
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
            cls._instance._idf_table=None
            cls._instance._break_table = None
            cls._instance._break_regex_method = None
            cls._instance._combine_regex_method = None
        return cls._instance

    def load_crf_seg_model(self, path=None, force=False):
        if not self._crf_seg_model or force:
            options = {}
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

    def load_crf_pos_model(self, path=None, force=False):
        if not self._crf_pos_model or force:
            options = {}
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

    def load_trie_tree(self, path=None, force=False):
        if not self._trie_tree or force:
            trie_tree = TrieTree()
            if not path:
                path = library_path
            for node_path in os.listdir(path):
                if not node_path.endswith('.dic'):
                    continue
                node_path = os.sep.join([path, node_path])
                with open(node_path, 'rb') as f:
                    for line in f:
                        word, tagging, freq = line.decode(
                            'utf8').strip().split('\t')
                        trie_tree.add(word, Word(
                            word,
                            freq=freq,
                            tagging=tagging,
                            source='dic',
                        ))
            self._trie_tree = trie_tree
        return self._trie_tree

    def load_idf_table(self, path=None, force=False):
        if not self._idf_table or force:
            if not path:
                idf_path = os.path.join(library_path, "idf.txt")
            else:
                idf_path = path 
            tree = {}
            if not os.path.exists(idf_path):
                return
            with open(idf_path, 'rb') as idf_file:
                for line in idf_file:
                    label = line.decode("utf8").strip().split('\t')
                    tree[label[0]] = float(label[1])
            self._idf_table = tree
        return self._idf_table

    def load_break_table(self, path=None, force=False):
        if not self._break_table or force:
            if not path:
                break_idx = os.path.join(library_path, "break.txt")
            else:
                break_idx = path
            tree = {}
            if not os.path.exists(break_idx):
                return
            with open(break_idx, 'rb') as break_file:
                for line in break_file:
                    label = line.decode("utf8").strip().split('\t')
                    tree[label[0]] = label[1:]
            self._break_table = tree
        return self._break_table

    def load_break_regex_method(self, path=None, force=False):
        if not self._break_regex_method or force:
            _break_regex_list = []
            if not path:
                break_regex_path = os.path.join(library_path, "break.regex")
            else:
                break_regex_path = path
            with open(break_regex_path, 'rb') as break_regex_file:
                for line in break_regex_file:
                    regex = line.decode('unicode-escape').strip()
                    if not regex or regex.startswith('#'):
                        continue
                    _break_regex_list.append(regex)
            pattern = u'|'.join(
                [u'[%s]+[*?]*' % regex for regex in _break_regex_list])
            pattern += u'|[^%s]+[*?]*' % u''.join(_break_regex_list)
            self._break_regex_method = re.compile(
                pattern,
                re.UNICODE,
            ).findall
        return self._break_regex_method

    def load_combine_regex_method(self, path=None, force=False):
        if not self._combine_regex_method or force:
            _combine_regex_list = []
            if not path:
                combine_regex_path = os.path.join(
                    library_path, "combine.regex")
            else:
                combine_regex_path = path
            with open(combine_regex_path, 'rb') as combine_regex_file:
                for line in combine_regex_file:
                    regex = line.decode('unicode-escape').strip()
                    if not regex or regex.startswith('#'):
                        continue
                    _combine_regex_list.append(regex)
            """
            fix '^a$' regex can match 'a\n'
            """
            def _combine_regex_method(text):
                m = re.compile(
                    '|'.join(_combine_regex_list), re.UNICODE
                ).match(text)
                if m and m.group() == text:
                    return True
                else:
                    return False
            self._combine_regex_method = _combine_regex_method
        return self._combine_regex_method

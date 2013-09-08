#encoding:utf-8
from .trie import TrieTree
from .loader import ResourceLoader
from .tools import StringHelper
from .word import Word
from .digital import is_chinese_number, chinese_to_number


class MarkerSegmentProcess(object):

    def __init__(self):
        self.string_helper = StringHelper()

    @classmethod
    def merge(cls, word, groups):
        length = len(groups)
        offset = word.offset
        words = []
        for index in range(length):
            group = groups[index]
            word = Word(group, offset=offset)
            offset += len(group)
            words.append(word)
        return words

    def process(self, word):
        """
        将文本切割成以marker为单位的词
        仅保留（字符、数字、标点、中文）
        """
        groups = self.string_helper.group_marker(word.text)
        return self.merge(word, groups)


class SimpleSegmentProcess(MarkerSegmentProcess):

    def __init__(self):
        MarkerSegmentProcess.__init__(self)
        self.loader = ResourceLoader()
        self.seg_model = self.loader.load_crf_seg_model()

    def process(self, word):
        words = MarkerSegmentProcess.process(self, word)
        pre_words = []
        for word in words:
            if word.marker == 'CN':
                label = self.label_sequence(word.text)
                groups = self.segment(label)
                pre_words.extend(self.merge(word, groups))
            else:
                pre_words.append(word)
        return pre_words

    def label_sequence(self, text, nbest=1):
        if self.seg_model.options.nbest != nbest:
            self.seg_model.options.nbest = nbest
        label = self.seg_model.label_sequence(
            '\n'.join(text), True).decode('utf-8')
        return label

    @classmethod
    def segment(cls, label):
        result_words = []
        prev_words = []
        for word_label in filter(lambda x: x.strip('\n'), label.split('\n')):
            word, label = word_label.split('\t')
            if 'S' in label:
                if prev_words:  # 这是一种错误的概率
                    return word.text
                result_words.append(word)
            elif 'E' in label:
                prev_words.append(word)
                result_words.append(u''.join(prev_words))
                prev_words = []
            else:
                prev_words.append(word)
        result_words.extend(prev_words)
        return result_words


class KeywordsSegmentProcess(SimpleSegmentProcess):

    def __init__(self):
        SimpleSegmentProcess.__init__(self)
        self.trie = self.loader.load_trie_tree()

    def process(self, word):
        length = len(word.text)
        if length <= 3:
            return self.crf_keywords(word, nbest=1)
        else:
            return self.crf_keywords(word, 2)

    def crf_keywords(self, word, nbest=2):
        words = MarkerSegmentProcess.process(self, word)
        pre_words = []
        for word in words:
            if word.marker == 'CN':
                labels = self.label_sequence(word.text, nbest).split('\n\n')
                words_list = filter(
                    lambda x: x,
                    [self.merge(word, self.segment(label)) for label in labels]
                )
                pre_words.extend(self.merge_keywords(word.text, words_list))
            else:
                pre_words.append(word)
        return pre_words

    @classmethod
    def merge_keywords(cls, text, words_list):
        trie = TrieTree()
        for words in words_list:
            for word in words:
                trie[word.text] = word
        pos, length = 0, len(text)
        pre_words = []
        while pos < length:
            dic = trie.search(text[pos:])
            for i in range(pos + 1, length + 1):
                word = text[pos:i]
                if word in dic:
                    pre_words.append(dic[word])
            pos += 1
        return pre_words


class PinyinSegmentProcess(MarkerSegmentProcess):

    def __init__(self):
        MarkerSegmentProcess.__init__(self)
        self.loader = ResourceLoader()
        self.trie = self.loader.load_trie_tree()

    def process(self, words):
        pre_words = []
        for word in words:
            if word.marker == 'LETTER':
                pinyins = self.segment(word.text)
                if pinyins:
                    pre_words.extend(self.merge(word, pinyins))
                else:
                    pre_words.append(word)
            else:
                pre_words.append(word)
        return pre_words

    def segment(self, text):
        length = len(text)
        pos = 0
        pre_words = []
        while pos < length:
            dic = self.trie.search(text[pos:length])
            max_matching_pos = 0
            for i in range(pos + 1, length + 1):
                if text[pos:i] in dic:
                    max_matching_pos = i
            if max_matching_pos == 0:
                return None
            else:
                pinyin = text[pos:max_matching_pos]
                pre_words.append(pinyin)
            pos = max_matching_pos
        return pre_words


class BreakProcess(MarkerSegmentProcess):

    def __init__(self):
        MarkerSegmentProcess.__init__(self)
        self.loader = ResourceLoader()
        self.tree = self.loader.load_break_table()

    def process(self, words):
        break_word_result = []
        for word in words:
            if word.text in self.tree:
                break_word_result.extend(
                    self.merge(word, self.tree[word.text]))
            else:
                break_word_result.append(word)
        return break_word_result


class CombineProcess(object):

    def __init__(self):
        self.loader = ResourceLoader()
        self.trie = self.loader.load_trie_tree()

    def process(self, words):
        pos = 0
        length = len(words)
        pre_words = []
        while pos < length:
            max_matching_pos = 0
            dic = self.trie.search(''.join(
                map(lambda x: x.text, words[pos:length])))
            for i in range(pos + 1, length + 1):
                text = ''.join(map(lambda x: x.text, words[pos:i]))
                if text in dic:
                    max_matching_pos = i
                elif is_chinese_number(text) and chinese_to_number(text):
                    max_matching_pos = i
            if max_matching_pos == 0:
                max_matching_pos = pos + 1
            text = ''.join(map(lambda x: x.text, words[pos:max_matching_pos]))
            if text in dic:
                word = dic[text]
            else:
                word = Word(text)
            word.offset = pos
            pre_words.append(word)
            pos = max_matching_pos
        return pre_words


class TaggingProcess(object):

    def __init__(self):
        self.loader = ResourceLoader()
        self.tagging_model = self.loader.load_crf_pos_model()

    def label_sequence(self, words):
        if self.tagging_model.options.nbest != 1:
            self.tagging_model.options.nbest = 1
        label_text = self.tagging_model.label_sequence(
            ''.join([(
                '%s\t%s\n' % (word.text, word.marker)) for word in words
            ]),
            include_input=False,
        )
        return label_text

    def process(self, words):
        label = self.label_sequence([
            word for word in words if word.marker != 'WHITESPACE'])
        taggings = self.tagging(label)
        tagging_pos = 0
        for word in words:
            if word.marker == 'WHITESPACE':
                word.tagging = 'x'
                tagging_pos -= 1
            elif word.marker == 'NUM':
                word.tagging = 'm'
            elif word.marker == 'LETTER':
                word.tagging = 'en'
            elif word.marker in ['HPUNC', 'FPUNC']:
                word.tagging = 'w'
            elif word.marker == 'CN':
                word.tagging = taggings[tagging_pos]
            else:
                word.tagging = 'x'
            tagging_pos += 1
        return words

    @classmethod
    def tagging(cls, label):
        taggings = []
        for word_label in filter(lambda x: x, label.split('\n')):
            tagging = word_label.decode('utf-8')
            taggings.append(tagging)
        return taggings


processes = {
    'default': SimpleSegmentProcess,
    'break': BreakProcess,
    'combine': CombineProcess,
    'tagging': TaggingProcess,
    'pinyin_segment': PinyinSegmentProcess,
    'segment_keywords': KeywordsSegmentProcess,
}

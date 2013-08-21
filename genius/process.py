#encoding:utf-8
from .loader import ResourceLoader
from .tools import StringHelper
from .digital import is_chinese_number, chinese_to_number


class SimpleSegmentProcess(object):

    def __init__(self):
        self.loader = ResourceLoader()
        self.seg_model = self.loader.load_crf_seg_model()

    def process(self, text):
        groups = StringHelper.group_ascii_cjk(text)
        pre_words = []
        for group in groups:
            mark = StringHelper.mark(group)
            if mark == 'ASCII':
                pre_words.append(group)
            elif mark == 'PUNC':
                pre_words.append(group)
            else:
                label = self.label_sequence(group)
                words = self.segment(label)
                if words:
                    pre_words.extend(words)
                else:
                    pre_words.extend(group)
        return pre_words

    def label_sequence(self, words, nbest=1):
        self.seg_model.options.nbest = nbest
        label = self.seg_model.label_sequence(
            '\n'.join(words), include_input=True).decode('utf-8')
        return label

    @classmethod
    def segment(cls, label):
        result_words = []
        prev_words = []
        for word_label in filter(lambda x: x.strip('\n'), label.split('\n')):
            word, label = word_label.split('\t')
            if 'S' in label:
                if prev_words:  # 这是一种错误的概率
                    return []
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

    def process(self, text):
        length = len(text)
        if length <= 3:
            return self.crf_keywords(text, nbest=1)
        else:
            return self.crf_keywords(text, 2)

    def crf_keywords(self, text, nbest=2):
        groups = StringHelper.group_ascii_cjk(text)
        pre_words = []
        for group in groups:
            mark = StringHelper.mark(group)
            if mark == 'ASCII':
                pre_words.append(group)
            elif mark == 'PUNC':
                pre_words.append(group)
            else:
                labels = self.label_sequence(group, nbest)
                for label in labels.split('\n\n'):
                    words = self.segment(label)
                    if words:
                        pre_words.extend(words)
                    else:
                        pre_words.extend(group)
        return pre_words

    def dict_keywords(self, text):
        pos, length = 0, len(text)
        pre_words = set()
        while pos < length:
            dic = self.trie.search(''.join(text[pos:length]))
            for i in range(pos + 1, length + 1):
                pre_word = text[pos:i]
                if pre_word in dic and len(pre_word) > 1:
                    pre_words.add(pre_word)
            pos += 1
        return pre_words


class PinyinSegmentProcess(object):

    def __init__(self):
        self.loader = ResourceLoader()
        self.trie = self.loader.load_trie_tree()

    def process(self, words):
        pre_words = []
        for word in words:
            marker = StringHelper.mark(word)
            if marker == 'ASCII':
                pinyins = self.segment(word)
                if pinyins:
                    pre_words.extend(pinyins)
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
                return text
            else:
                pinyin = text[pos:max_matching_pos]
                pre_words.append(pinyin)
            pos = max_matching_pos
        return pre_words


class BreakProcess(object):

    def __init__(self):
        self.loader = ResourceLoader()
        self.tree = self.loader.load_break_table()

    def process(self, word):
        break_word_result = []
        for term in word:
            if term in self.tree:
                break_word_result.extend(self.tree[term])
            else:
                break_word_result.append(term)
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
            word = words[pos]
            max_matching_pos = 0
            dic = self.trie.search(''.join(words[pos:length]))
            for i in range(pos + 1, length + 1):
                word = ''.join(words[pos:i])
                if word in dic:
                    max_matching_pos = i
                elif is_chinese_number(word) and chinese_to_number(word):
                    max_matching_pos = i
            if max_matching_pos == 0:
                max_matching_pos = pos + 1
            pre_words.append(''.join(words[pos:max_matching_pos]))
            pos = max_matching_pos
        return pre_words


class TaggingProcess(object):

    def __init__(self):
        self.loader = ResourceLoader()
        self.tagging_model = self.loader.load_crf_pos_model()

    def label_sequence(self, words, nbest=1):
        self.seg_model.options.nbest = nbest
        label_text = self.tagging_model.label_sequence(
            ''.join([(
                '%s\t%s\n' % (word, StringHelper.mark(word))) for word in words
            ]),
            include_input=True,
        )
        return label_text

    def process(self, words):
        label = self.label_sequence(words, nbest=1)
        return self.tagging(label)

    @classmethod
    def tagging(cls, label):
        result_words = []
        for word_label in filter(lambda x: x, label.split('\n')):
            text, marker, tagging = word_label.decode('utf-8').split('\t')
            if StringHelper.is_number(text):
                result_words.append('\t'.join((text, 'm')))
            elif StringHelper.is_letter(text):
                result_words.append('\t'.join((text, 'en')))
            elif marker == 'PUNC':
                result_words.append('\t'.join((text, 'w')))
            else:
                result_words.append('\t'.join((text, tagging)))
        return result_words


processes = {
    'default': SimpleSegmentProcess,
    'break': BreakProcess,
    'combine': CombineProcess,
    'tagging': TaggingProcess,
    'pinyin_segment': PinyinSegmentProcess,
    'segment_keywords': KeywordsSegmentProcess,
}

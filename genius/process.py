#encoding:utf-8
import re
import copy
from .loader import ResourceLoader
from .tools import StringHelper
from .word import Word
from .digital import is_chinese_number, chinese_to_number


class BaseSegmentProcess(object):

    group_marker = re.compile(
        '|'.join([
            '%s{1,}?' % StringHelper.cjk_pattern,
            '%s+[*?]*' % StringHelper.digit_pattern,
            '%s+[*?]*' % StringHelper.alpha_pattern,
            '%s+[*?]*' % StringHelper.whitespace_pattern,
            '%s+[*?]*' % StringHelper.punctuation_pattern,
        ]),
        re.UNICODE
    ).findall

    def __init__(self, **kwargs):
        self.string_helper = StringHelper()
        self.segment_type = 'marker'

    def split_by_text_groups(self, word, text_groups):
        length = len(text_groups)
        offset = word.offset
        words = []
        for index in range(length):
            group = text_groups[index]
            word = Word(group, offset=offset, source=self.segment_type)
            offset += len(group)
            words.append(word)
        return words

    def process(self, word):
        """
        将文本切割成以marker为单位的词
        """
        groups = self.group_marker(word.text)
        return self.split_by_text_groups(word, groups)


class SimpleSegmentProcess(BaseSegmentProcess):

    def __init__(self, **kwargs):
        BaseSegmentProcess.__init__(self, **kwargs)
        self.loader = ResourceLoader()
        self.seg_model = self.loader.load_crf_seg_model()
        self.segment_type = 'crf'

    def process(self, word):
        base_words = BaseSegmentProcess.process(self, word)
        result_words = []
        pre_label_words = []
        for word in base_words:
            if word.marker != 'WHITESPACE':
                pre_label_words.append(word)
            else:
                label = self.label_sequence(pre_label_words)
                result_words.extend(self.segment(label, pre_label_words))
                pre_label_words = []
                result_words.append(word)
        if pre_label_words:
            label = self.label_sequence(pre_label_words)
            result_words.extend(self.segment(label, pre_label_words))
        return result_words

    def label_sequence(self, words, nbest=1):
        if self.seg_model.options.nbest != nbest:
            self.seg_model.options.nbest = nbest
        label = self.seg_model.label_sequence(
            '\n'.join(['%s\t%s' % (word.text, word.marker) for word in words]),
            False,
        ).decode('utf-8')
        return label.strip(self.string_helper.whitespace_range)

    def segment(self, label, pre_label_words):
        result_words = []
        offset = 0
        for index, label in enumerate(label.split('\n')):
            if 'S' == label:
                if index - offset > 1:
                    pre_word = copy.copy(pre_label_words[offset])
                    pre_word.text = u''.join(
                        [word.text for word in pre_label_words[offset:index]]
                    )
                    pre_word.source = self.segment_type
                    result_words.append(pre_word)
                result_words.append(pre_label_words[index])
                offset = index + 1
            elif 'E' == label:
                pre_word = copy.copy(pre_label_words[offset])
                pre_word.text = u''.join(
                    [word.text for word in pre_label_words[offset:index + 1]]
                )
                pre_word.source = self.segment_type
                result_words.append(pre_word)
                offset = index + 1
        if offset < len(pre_label_words):
            pre_word = copy.copy(pre_label_words[offset])
            pre_word.text = u''.join(
                [word.text for word in pre_label_words[offset:]]
            )
            pre_word.source = self.segment_type
            result_words.append(pre_word)
        return result_words


class KeywordsSegmentProcess(SimpleSegmentProcess):

    def __init__(self, **kwargs):
        SimpleSegmentProcess.__init__(self, **kwargs)

    def process(self, word):
        length = len(word.text)
        if length <= 3:
            return self.crf_keywords(word, nbest=1)
        else:
            return self.crf_keywords(word, 2)

    def crf_keywords(self, word, nbest=2):
        base_words = BaseSegmentProcess.process(self, word)
        result_words = []
        pre_label_words = []
        for word in base_words:
            if word.marker != 'WHITESPACE':
                pre_label_words.append(word)
            else:
                labels = self.label_sequence(
                    pre_label_words, nbest).split('\n\n')
                result_words.extend(self.segment(labels, pre_label_words))
                pre_label_words = []
                result_words.append(word)
        if pre_label_words:
            labels = self.label_sequence(pre_label_words, nbest).split('\n\n')
            result_words.extend(self.segment(labels, pre_label_words))
        return result_words

    def segment(self, labels, pre_label_words):
        words_list = []
        for label in labels:
            if label:
                words_list.extend(
                    SimpleSegmentProcess.segment(
                        self, label, pre_label_words))
        return self.combine_by_words_list(pre_label_words, set(words_list))

    @classmethod
    def combine_by_words_list(cls, pre_label_words, words_list):
        pos, length = 0, len(pre_label_words)
        result_words = []
        while pos < length:
            for i in range(pos + 1, length + 1):
                text = u''.join([word.text for word in pre_label_words[pos:i]])
                word = copy.copy(pre_label_words[pos])
                word.text = text
                word.source = 'crf'
                if word in words_list:
                    result_words.append(word)
            pos += 1
        return result_words


class PinyinSegmentProcess(BaseSegmentProcess):

    def __init__(self, **kwargs):
        BaseSegmentProcess.__init__(self, **kwargs)
        self.loader = ResourceLoader()
        self.trie = self.loader.load_trie_tree()
        self.segment_type = 'pinyin'

    def process(self, words):
        result_words = []
        for word in words:
            if word.marker == 'ALPHA':
                pinyins = self.segment(word.text)
                if pinyins:
                    result_words.extend(self.split_by_text_groups(
                        word, pinyins))
                else:
                    result_words.append(word)
            else:
                result_words.append(word)
        return result_words

    def segment(self, text):
        length = len(text)
        pos = 0
        result_words = []
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
                result_words.append(pinyin)
            pos = max_matching_pos
        return result_words


class BreakSegmentProcess(BaseSegmentProcess):

    def __init__(self, **kwargs):
        BaseSegmentProcess.__init__(self, **kwargs)
        self.loader = ResourceLoader()
        self.tree = self.loader.load_break_table()
        self.break_regex_method = self.loader.load_break_regex_method()
        self.segment_type = 'break'

    def process(self, words):
        break_word_result = []
        for word in words:
            if word.text in self.tree:
                break_word_result.extend(
                    self.split_by_text_groups(word, self.tree[word.text]))
            else:
                text_groups = self.break_regex_method(word.text)
                if len(text_groups) > 1:
                    break_word_result.extend(
                        self.split_by_text_groups(word, text_groups))
                else:
                    break_word_result.append(word)
        return break_word_result


class CombineSegmentProcess(BaseSegmentProcess):

    def __init__(self, **kwargs):
        BaseSegmentProcess.__init__(self, **kwargs)
        self.loader = ResourceLoader()
        self.trie = self.loader.load_trie_tree()
        self.combine_regex_method = self.loader.load_combine_regex_method()

    def process(self, words):
        pos = 0
        length = len(words)
        result_words = []
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
                elif self.combine_regex_method(text):
                    max_matching_pos = i
            if max_matching_pos == 0:
                max_matching_pos = pos + 1
            text = ''.join(map(lambda x: x.text, words[pos:max_matching_pos]))
            word = words[pos]
            if text in dic:
                pre_word = copy.copy(dic[text])
                pre_word.offset = word.offset
                word = pre_word
            elif max_matching_pos == pos + 1:  # 无匹配
                word = words[pos]
            else:
                word = Word(text)
                word.offset = word.offset
            result_words.append(word)
            pos = max_matching_pos
        return result_words


class TaggingProcess(object):

    def __init__(self, **kwargs):
        self.string_helper = StringHelper()
        self.loader = ResourceLoader()
        self.tagging_model = self.loader.load_crf_pos_model()

    def label_tagging(self, words):
        if self.tagging_model.options.nbest != 1:
            self.tagging_model.options.nbest = 1
        label_sequence_texts = []
        unlabel_sequence_indexes = []
        for index, word in enumerate(words):
            if word.marker == 'WHITESPACE':
                unlabel_sequence_indexes.append(index)
            else:
                label_sequence_texts.append(
                    u'%s\t%s' % (word.text, word.marker))
        label_text = self.tagging_model.label_sequence(
            '\n'.join(label_sequence_texts),
            include_input=False,
        ).decode('utf8').strip(self.string_helper.whitespace_range)
        taggings = label_text.split('\n')
        map(lambda x: taggings.insert(x, 'x'), unlabel_sequence_indexes)
        return taggings

    def process(self, words):
        taggings = self.label_tagging(words)
        for index, word in enumerate(words):
            if word.marker == 'DIGIT':
                word.tagging = 'm'
            elif word.marker == 'ALPHA':
                word.tagging = 'en'
            elif word.marker == 'PUNC':
                word.tagging = 'w'
            else:
                word.tagging = taggings[index]
        return words

    @classmethod
    def tagging(cls, label):
        taggings = []
        for word_label in filter(lambda x: x, label.split('\n')):
            tagging = word_label.decode('utf-8')
            taggings.append(tagging)
        return taggings


class TagExtractProcess(object):

    def __init__(self, **kwargs):
        self.string_helper = StringHelper()
        self.loader = ResourceLoader()
        self.idf_table = self.loader.load_idf_table()
        self.default_idf = sorted(
            self.idf_table.values()
        )[int(len(self.idf_table)/2)]
        self.ntop = kwargs.get('ntop', 20)

    def process(self, words):
        idf_table = {}
        for word in words:
            if len(word) > 1:
                idf_table[word.text] = idf_table.get(word.text, 0.0) + 1.0
        total = sum(idf_table.values())
        idf_table = [(text, idf/total) for text, idf in idf_table.items()]
        tf_idf_list = sorted([(
            idf * self.idf_table.get(text, self.default_idf),
            text,
        ) for text, idf in idf_table], reverse=True)[:self.ntop]
        return [tf_idf[1] for tf_idf in tf_idf_list]

processes = {
    'default': SimpleSegmentProcess,
    'break': BreakSegmentProcess,
    'combine': CombineSegmentProcess,
    'pinyin_segment': PinyinSegmentProcess,
    'segment_keywords': KeywordsSegmentProcess,
    'tagging': TaggingProcess,
    'tag_extract': TagExtractProcess,
}

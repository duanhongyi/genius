#encoding:utf-8
import six
from genius.tools import StringHelper


class Word(object):
    string_helper = StringHelper()

    def __init__(self, text, **kwargs):
        self.text = text  # 词
        self.freq = kwargs.get('freq', 0)  # 词频
        self.tagging = kwargs.get('tagging', 'unknown')  # 词性
        # dic:字典,crf:crf生成,break:打断字典,pinyin拼音分词
        self.source = kwargs.get('source', 'unknown')
        self.offset = kwargs.get('offset', 0)  # 在文本中的位置

    @property
    def marker(self):
        """
        see string_helper.mark_text method
        """
        return self.string_helper.mark_text(self.text)

    def __str__(self):
        if six.PY2:
            return self.text.encode('utf8')
        return self.text

    def __len__(self):
        return len(self.text)

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, obj):
        if isinstance(obj, type(self)):
            return (
                obj.text == self.text and 
                obj.freq == self.freq and
                obj.tagging == self.tagging and
                obj.source == self.source and
                obj.offset == self.offset
            )
        return False


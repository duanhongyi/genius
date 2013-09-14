#encoding:utf-8
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
        return self.text.encode('utf8')

    def __len__(self):
        return len(self.text)

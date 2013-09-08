#encoding:utf-8
from genius.tools import StringHelper


class Word(object):
    string_helper = StringHelper()

    def __init__(self, text, **kwargs):
        self.text = text  # 词
        self.freq = kwargs.get('freq', 0)  # 词频
        self.tagging = kwargs.get('tagging', 'unknown')  # 词性
        self.source = kwargs.get('source', 'unknown')  # dic:字典,crf:crf生成,brk:打断字典
        self.offset = kwargs.get('offset', 0)  # 在文本中的位置
        #标记（NUM、LETTER、CN、HWPUNC、FWPUNC、UNKNOW）
        self.marker = kwargs.get(
            'marker', self.string_helper.marker_text(self.text))

    def __repr__(self):
        return "u'%s'" % self.text.encode('unicode_escape')

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)

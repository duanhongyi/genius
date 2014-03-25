#encoding:utf-8
import os
import io
import zipfile
from contextlib import closing
from .process import processes
from .word import Word

here = os.path.abspath(os.path.dirname(__file__))


def seg_text(text, **kwargs):
    """
    text: 必须是unicode
    use_break: boolean类型，代表是否进行打断处理
    use_combine: boolean类型，代表是否使用FFM最大正向匹配合并词
    use_tagging: boolean类型，是否进行词性标注
    use_parse_pinyin: boolean类型，是否对拼音进行分词
    """
    word = Word(text)
    pre_words = processes['default'](**kwargs).process(word)
    if kwargs.get('use_break', True):  # 对分词结构进行打断
        pre_words = processes['break'](**kwargs).process(pre_words)
    if kwargs.get('use_combine', False):  # 合并分词结果
        pre_words = processes['combine'](**kwargs).process(pre_words)
    if kwargs.get('use_pinyin_segment', False):  # 是否对pinyin分词
        pre_words = processes['pinyin_segment'](**kwargs).process(pre_words)
    if kwargs.get('use_tagging', False):  # 是否进行词性标注
        pre_words = processes['tagging'](**kwargs).process(pre_words)
    return pre_words


def seg_keywords(text, **kwargs):
    """
    text: 必须是unicode
    use_break: boolean类型，代表是否进行打断处理
    use_tagging: boolean类型，是否进行词性标注
    use_parse_pinyin: boolean类型，是否对拼音进行分词
    """
    word = Word(text)
    pre_words = processes['segment_keywords'](**kwargs).process(word)
    if kwargs.get('use_break', True):  # 对分词结构进行打断
        pre_words = processes['break'](**kwargs).process(pre_words)
    if kwargs.get('use_pinyin_segment', False):  # 是否对pinyin分词
        pre_words = processes['pinyin_segment'](**kwargs).process(pre_words)
    if kwargs.get('use_tagging', False):  # 是否进行词性标注
        pre_words = processes['tagging'](**kwargs).process(pre_words)
    return pre_words

def extract_tag(text, **kwargs):
    """
    text: 必须是unicode
    ntop: 提取前n个关键字
    use_break: boolean类型，代表是否进行打断处理
    use_combine: boolean类型，代表是否使用FFM最大正向匹配合并词
    use_parse_pinyin: boolean类型，是否对拼音进行分词
    """
    kwargs['use_tagging'] = False  # 忽略use_tagging参数
    pre_words = seg_text(text, **kwargs)
    return processes['tag_extract'](**kwargs).process(pre_words)

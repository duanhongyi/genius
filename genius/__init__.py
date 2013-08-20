#encoding:utf-8

from .process import processes


def seg_text(text, **kwargs):
    """
    text: 必须是unicode
    use_break: boolean类型，代表是否进行打断处理
    use_combine: boolean类型，代表是否使用FFM最大正向匹配合并词
    use_tagging: boolean类型，是否进行词性标注
    use_parse_pinyin: boolean类型，是否对拼音进行分词
    """
    pre_words = processes['default']().process(text)
    if kwargs.get('use_break', False):  # 对分词结构进行打断
        pre_words = processes['use_break']().process(pre_words)
    if kwargs.get('use_combine', False):  # 合并分词结果
        pre_words = processes['use_combine']().process(pre_words)
    if kwargs.get('use_pinyin_segment', False):  # 是否对pinyin分词
        pre_words = processes['use_pinyin_segment']().process(pre_words)
    if kwargs.get('use_tagging', False):  # 是否进行词性标注
        pre_words = processes['use_tagging']().process(pre_words)
    return pre_words

#encoding:utf-8
import re
#from genius.word import Word


class StringHelper(object):

    #range
    num_range = u'0-9'
    letter_range = u'a-zA-Z'
    cjk_range = u'\u4e00-\u9fff\u3400-\u4ddf\u9000-\ufaff'
    cjk_range += u'\u3040-\u309f\uac00-\ud7af\uff10-\uff19'
    whitespace_range = u'\t\n\x0b\x0c\r '
    half_width_punctuation_range = u'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    full_width_punctuation_range = u'！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～'

    num_pattern = u'[%s]' % num_range
    letter_pattern = u'[%s]' % letter_range
    cjk_pattern = u'[%s]' % cjk_range
    whitespace_pattern = u'[%s]' % whitespace_range
    half_width_punctuation_pattern = u'[%s]' % half_width_punctuation_range
    full_width_punctuation_pattern = u'[%s]' % full_width_punctuation_range
    unknown_pattern = u'[^%s]' % (
        ''.join([
            num_range,
            letter_range,
            cjk_range,
            whitespace_range,
            half_width_punctuation_range,
            full_width_punctuation_range,
        ])
    )

    group_marker = re.compile(
        '|'.join(map(lambda x:'%s+[*?]*' % x, [
            num_pattern,
            letter_pattern,
            cjk_pattern,
            whitespace_pattern,
            half_width_punctuation_pattern,
            full_width_punctuation_pattern,
            unknown_pattern,
        ]))
    ).findall

    #单词分类标记
    @classmethod
    def mark_text(cls, word):
        marker = None
        if re.match('^%s+[*?]*$' % cls.num_pattern, word):  # 数字
            marker = 'NUM'
        elif re.match('^%s+[*?]*$' % cls.letter_pattern, word):  # 字母
            marker = 'LETTER'
        elif re.match('^%s+[*?]*$' % cls.cjk_pattern, word):  # 中文
            marker = 'CN'
        elif re.match('^%s+[*?]*$' % cls.whitespace_pattern, word):  # 空格字符
            marker = 'WHITESPACE'
        elif re.match(
                '^%s+[*?]*$' % cls.half_width_punctuation_pattern, word):  # 半角符号
            marker = 'HPUNC'
        elif re.match(
                '^%s+[*?]*$' % cls.full_width_punctuation_pattern, word):  # 全角符号
            marker = 'FPUNC'
        else:
            marker = 'UNKNOWN'  # 未知标记
        return marker

    @classmethod
    def halfwidth_to_fullwidth(cls, word):
        rstring = ""
        for uchar in word:
            inside_code = ord(uchar)
            if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
                rstring += uchar
                continue
            if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
                inside_code = 0x3000
            else:
                inside_code += 0xfee0
            rstring += unichr(inside_code)
        return rstring

    @classmethod
    def fullwidth_to_halfwidth(cls, word):
        rstring = ""
        for uchar in word:
            inside_code = ord(uchar)
            if inside_code == 0x3000:
                inside_code = 0x0020
            else:
                inside_code -= 0xfee0
            if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
                rstring += uchar
            else:
                rstring += unichr(inside_code)
        return rstring

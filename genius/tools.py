#encoding:utf-8
import re


class StringHelper(object):

    #range
    digit_range = u'0-9'
    alpha_range = u'a-zA-Z'
    whitespace_range = u'\t\n\x0b\x0c\r '
    halfwidth_punctuation_range = u'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    fullwidth_punctuation_range = u'！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？'
    fullwidth_punctuation_range += u'＠［＼］＾＿｀｛｜｝～。、《》•”“'
    punctuation_range = ''.join([
        halfwidth_punctuation_range,
        fullwidth_punctuation_range,
    ])

    digit_pattern = u'[%s]' % digit_range
    alpha_pattern = u'[%s]' % alpha_range
    whitespace_pattern = u'[%s]' % whitespace_range
    halfwidth_punctuation_pattern = u'[%s]' % halfwidth_punctuation_range
    punctuation_pattern = u'[%s]' % punctuation_range
    cjk_pattern = u'[^%s]' % ''.join([
        digit_range,
        alpha_range,
        whitespace_range,
        punctuation_range,
    ])

    #单词分类标记
    @classmethod
    def mark_text(cls, text):
        marker = None
        if re.match(
                '^%s+[*?]*$' % cls.digit_pattern,
                text, re.UNICODE):  # 数字
            marker = 'DIGIT'
        elif re.match(
                '^%s+[*?]*$' % cls.alpha_pattern,
                text, re.UNICODE):  # 字母
            marker = 'ALPHA'
        elif re.match(
                '^%s+[*?]*$' % cls.whitespace_pattern,
                text, re.UNICODE):  # 空格字符
            marker = 'WHITESPACE'
        elif re.match(
<<<<<<< HEAD
                '^%s+[*?]*$' % cls.punctuation_pattern, text):  # 标点符号
=======
                '^%s+[*?]*$' % cls.punctuation_pattern,
                text, re.UNICODE):  # 半角符号
>>>>>>> 4125bdf1ffbe4beca70e4e9afed33a9d97d78ffd
            marker = 'PUNC'
        else:
            marker = 'CJK'  # 中日韩
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

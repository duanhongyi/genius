#encoding:utf-8
import re
import string


class StringHelper(object):

    cjk_pattern = u'[\u4e00-\u9fff\u3400-\u4ddf\u9000-\ufaff\u3040-\u309f\uac00-\ud7af\uff10-\uff19]+[*?]*'
    ascii_pattern = u'[a-zA-Z]+[*?]*|[0-9]+[*?]*'
    punctuation_pattern = (
        u'[%s！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～]+[*?]*' % string.punctuation
    )
    whitespace_pattern = u"[%s]+[*?]*" % string.whitespace
    group_ascii_cjk_pattern = u'|'.join(
        [ascii_pattern, punctuation_pattern, cjk_pattern])
    group_ascii_cjk = re.compile(group_ascii_cjk_pattern, re.UNICODE).findall
    is_whitespace_string = re.compile("^%s$" % whitespace_pattern).match
    is_number = re.compile('^[0-9]+[*?]*$').match
    is_letter = re.compile('^[a-zA-Z]+[*?]*$').match

    #判断字符是否是cjk字符
    @staticmethod
    def is_cjk_char(charater):
        c = ord(charater)
        return 0x4E00 <= c <= 0x9FFF or \
            0x3400 <= c <= 0x4dbf or \
            0xf900 <= c <= 0xfaff or \
            0x3040 <= c <= 0x309f or \
            0xac00 <= c <= 0xd7af or \
            0xFF10 <= c <= 0xFF19

    #判断是否是ASCII码
    @staticmethod
    def is_latin_char(ch):
        if ch in string.whitespace:
            return False
        if ch in string.punctuation:
            return False
        return ch in string.printable

    @staticmethod
    def halfwidth_to_fullwidth(word):
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

    @staticmethod
    def fullwidth_to_halfwidth(word):
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

    #单词分类标记
    @staticmethod
    def mark(word):
        if re.match('^%s$' % StringHelper.ascii_pattern, word):
            return 'ASCII'
        elif re.match('^%s$' % StringHelper.cjk_pattern, word):
            return 'CN'
        else:
            return 'PUNC'

# encoding:utf-8
import re

CN_NUM = {
    u'〇': 0,
    u'一': 1,
    u'二': 2,
    u'三': 3,
    u'四': 4,
    u'五': 5,
    u'六': 6,
    u'七': 7,
    u'八': 8,
    u'九': 9,

    u'零': 0,
    u'壹': 1,
    u'贰': 2,
    u'叁': 3,
    u'肆': 4,
    u'伍': 5,
    u'陆': 6,
    u'柒': 7,
    u'捌': 8,
    u'玖': 9,

    u'貮': 2,
    u'两': 2,
}
CN_UNIT = {
    u'十': 10,
    u'拾': 10,
    u'百': 100,
    u'佰': 100,
    u'千': 1000,
    u'仟': 1000,
    u'万': 10000,
    u'萬': 10000,
    u'亿': 100000000,
    u'億': 100000000,
    u'兆': 1000000000000,
}


cn_unit_match = re.compile(
    '^[%s]+$' % u''.join(CN_UNIT.keys()),
    re.UNICODE
).match

cn_number_match = re.compile(
    '^[%s]+$' % u''.join(CN_NUM.keys()),
    re.UNICODE
).match

cn_number_unit_match = re.compile(
    '^[%s]+$' % u''.join((list(CN_NUM.keys()) + list(CN_UNIT.keys()))),
    re.UNICODE
).match


def is_chinese_number(text):
    if cn_number_unit_match(text):
        if text[0] not in CN_UNIT or CN_UNIT[text[0]] == 10:
            try:
                chinese_to_number(text)
                return True
            except ValueError:
                return False
    return False


def chinese_to_number(text):
    if cn_number_match(text):
        return int(''.join([str(CN_NUM[c]) for c in text]))
    words = list(text)
    num, unit, result = 0, 0, 0
    for word in words:
        if word in CN_UNIT:
            unit = CN_UNIT[word]
            if unit in (10000, 100000000, 1000000000000):
                result = (result + num) * unit
            else:
                if num == 0 and unit == 10:
                    result += unit
                elif num != 0:
                    result += num * unit
                else:
                    raise ValueError
            num = 0
        else:
            if num != 0:
                raise ValueError
            num = CN_NUM[word]
            if num == 0:
                unit = 10
    return result + (unit/10 * num)

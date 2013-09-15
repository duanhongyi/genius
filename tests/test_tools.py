#encoding:utf-8
from genius.tools import StringHelper

def test_string_helper():
    helper = StringHelper()
    s1 = helper.halfwidth_to_fullwidth('1')
    s2 = helper.fullwidth_to_halfwidth(s1)
    assert s1 != s2
    assert s1 != u'1'
    assert s2 == u'1'
    assert helper.mark_text(s1) == 'DIGIT'
    assert helper.mark_text(s2) == 'DIGIT'
    assert helper.mark_text(u"1中国") == 'CJK'
    assert helper.mark_text(u'SourceInsight') == 'ALPHA'

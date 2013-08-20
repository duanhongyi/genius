#encoding:utf-8
from scseg.tools import *

def test_string_helper():
    s1 = StringHelper.halfwidth_to_fullwidth('1')
    s2 = StringHelper.fullwidth_to_halfwidth(s1)
    assert s1 != s2
    assert s1 !=u'1'
    assert s2 == u'1'
    assert StringHelper.mark(s1) == 'ASCII'
    assert StringHelper.mark(s2) == 'ASCII'
    assert StringHelper.mark(u"1中国") == 'CN'
    assert StringHelper.mark(u'SourceInsight') == 'ASCII'

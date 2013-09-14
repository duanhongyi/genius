import genius

def test_seg_text():
    words = genius.seg_text(u"南京市长江大桥\n12、english123pinyin")
    word = words[0]
    assert word.text == u'南京市'
    assert word.offset == 0

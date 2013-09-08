genius
========
genius中文分词，是基于crf条件随机场的分组件


Feature
========

* 支持pinyin分词
* 支持用户自定义break
* 支持用户自定义词典
* 支持词性标注

Install
==========
* 安装git: 1) ubuntu or debian `apt-get install git` 2) fedora or redhat `yum install git`
* 升级setuptools: `pip install easy_install --upgrade`
* 升级pip: `pip install pip --upgrade`
* `pip install genius`
* 通过`import genius`来引用


Algorithm
==========
* 采用trie树进行词典查找
* 基于wapiti实现条件随机场分词
* 可以通过genius.loader.ResourceLoader来重载默认的字典

功能 1)：分词`genius.seg_text`方法
==============

* `genius.seg_text`函数接受5个参数: 
* `text`第一个参数为需要分词的字符 
* `use_break`代表对分词结构进行打断处理 
* `use_combine`代表是否使用字典进行词合并
* `use_tagging`代表是否进行词性标注
* `use_pinyin_segment`代表是否对拼音进行分词处理

代码示例( 全功能分词 )

    #encoding=utf-8
    import genius

    seg_list = genius.seg_text(
        u'中国人民站起来了pinyin',
        use_combine=True,
        use_pinyin_segment=True,
        use_tagging=True)
    print '\n'.join(['%s\t%s' % (word.text, word.tagging) for word in seg_list])

功能 2)：面向索引分词
==============
* `genius.seg_keywords`方法专门为搜索引擎索引准备，保留歧义分割。
* `text`第一个参数为需要分词的字符 
* `use_break`代表对分词结构进行打断处理 
* `use_tagging`代表是否进行词性标注
* `use_pinyin_segment`代表是否对拼音进行分词处理
* 由于合并操作与此方法有意义上的冲突，此方法并不提供合并功能；并且如果采用此方法做索引时候，检索时不推荐`genius.seg_text`使用`use_combine=True`参数。

代码示例

    #encoding=utf-8
    import genius

    seg_list = genius.seg_keywords(u'中国人民站起来了pinyin')
    print '\n'.join([word.text for word in seg_list])

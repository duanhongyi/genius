Genius
========
Genius是一个开源的python中文分词组件，采用 CRF(Conditional Random Field)条件随机场算法。

Feature
========

* 支持python2.x、python3.x以及pypy2.x。
* 支持简单的pinyin分词
* 支持用户自定义break
* 支持用户自定义合并词典
* 支持词性标注

Source Install
==========
* 安装git: 1) ubuntu or debian `apt-get install git` 2) fedora or redhat `yum install git`
* 下载代码：`git clone https://github.com/duanhongyi/genius.git`
* 安装代码：`python setup.py install`

Pypi Install
============
* 执行命令：`easy_install genius`或者`pip install genius`


Algorithm
==========
* 采用trie树进行合并词典查找
* 基于wapiti实现条件随机场分词
* 可以通过genius.loader.ResourceLoader来重载默认的字典

功能 1)：分词`genius.seg_text`方法
==============

* `genius.seg_text`函数接受5个参数，其中text是必填参数: 
* `text`第一个参数为需要分词的字符
* `use_break`代表对分词结构进行打断处理，默认值`True`
* `use_combine`代表是否使用字典进行词合并，默认值`False`
* `use_tagging`代表是否进行词性标注，默认值`True`
* `use_pinyin_segment`代表是否对拼音进行分词处理，默认值`True`

代码示例( 全功能分词 )

    #encoding=utf-8
    import genius
    text = u"""昨天,我和施瓦布先生一起与部分企业家进行了交流,大家对中国经济当前、未来发展的态势、走势都十分关心。"""
    seg_list = genius.seg_text(
        text,
        use_combine=True,
        use_pinyin_segment=True,
        use_tagging=True,
        use_break=True
    )
    print('\n'.join(['%s\t%s' % (word.text, word.tagging) for word in seg_list]))

功能 2)：面向索引分词
==============
* `genius.seg_keywords`方法专门为搜索引擎索引准备，保留歧义分割，其中text是必填参数。
* `text`第一个参数为需要分词的字符 
* `use_break`代表对分词结构进行打断处理，默认值`True`
* `use_tagging`代表是否进行词性标注，默认值`False`
* `use_pinyin_segment`代表是否对拼音进行分词处理，默认值`False`
* 由于合并操作与此方法有意义上的冲突，此方法并不提供合并功能；并且如果采用此方法做索引时候，检索时不推荐`genius.seg_text`使用`use_combine=True`参数。

代码示例

    #encoding=utf-8
    import genius

    seg_list = genius.seg_keywords(u'南京市长江大桥')
    print('\n'.join([word.text for word in seg_list]))

功能 3)：关键词提取
==============
* `genius.tag_extract`方法专门为提取tag关键字准备，其中text是必填参数。
* `text`第一个参数为需要分词的字符 
* `use_break`代表对分词结构进行打断处理，默认值`True`
* `use_combine`代表是否使用字典进行词合并，默认值`False`
* `use_pinyin_segment`代表是否对拼音进行分词处理，默认值`False`

代码示例

    #encoding=utf-8
    import genius

    tag_list = genius.tag_extract(u'南京市长江大桥')
    print('\n'.join(tag_list))

其他说明 4)：
=================
* 目前分词语料出自人民日报1998年1月份，所以对于新闻类文章分词较为准确。
* CRF分词效果很大程度上依赖于训练语料的类别以及覆盖度，若解决语料问题分词和标注效果还有很大的提升空间。

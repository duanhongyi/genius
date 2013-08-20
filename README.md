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
* 升级pip和setuptools执行命令: `pip install easy_install` 和 `pip install pip --upgrade`
* pip install https://github.com/duanhongyi/genius/archive/master.zip
* 通过import genius来引用


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
    print '\n'.join(seg_list)

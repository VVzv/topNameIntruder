# !/usr/bin/python
# -*- coding:utf-8 -*-
# __Author__: VVzv

import pypinyin

name_dict = open('./top500_name_dict.txt', 'r').readlines()

# 中文名字拼音化
def namePinyin(word):
    name_pinyin = ''
    for w in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        name_pinyin += ''.join(w)
    return name_pinyin

pinyin_list = []
for w in name_dict:
    pinyin_list.append(namePinyin(w))
# print(pinyin_list)
with open('top500_name_pinyin_dict.txt', 'w', encoding='utf-8') as f:
    f.writelines(pinyin_list)


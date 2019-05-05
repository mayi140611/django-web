#!/usr/bin/python
# encoding: utf-8

"""
@author: Ian
@file: utils.py
@time: 2019-04-30 15:42
"""
import pandas as pd
import re
from mayiutils.db.pymysql_wrapper import PyMysqlWrapper
from mayiutils.pickle_wrapper import PickleWrapper as picklew
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os
import shutil
import jieba
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from django_rest_web.settings import BASE_DIR
import os


projname = 'dicproj'


def standardize(s):
    """
    字符串标准化
        去除所有空格
        去掉末尾最后一个 的
        小写转大写
        中文字符替换： （），【】：“”’‘；
    :param s:
    :return:
    """

    s = re.sub(r'\s+', '', s)
    s = re.sub(r'的$', '', s)  # 去掉末尾最后一个 的
    s = re.sub(r',未特指场所$', '', s)
    s = s.upper()
    s = re.sub(r'（', '(', s)
    s = re.sub(r'）', ')', s)
    s = re.sub(r'，', ',', s)
    s = re.sub(r'：', ':', s)
    s = re.sub(r'【', '[', s)
    s = re.sub(r'】', ']', s)
    s = re.sub(r'“|”|’|‘', '"', s)
    s = re.sub(r'】', ']', s)
    s = re.sub(r'；', ';', s)
    return s


def cal_similarity_by_tfidf(name, threshold=0.9):
    """
    tfidf + cosine distance
    :param name:
    :param threshold:
    :return:
    """
    t = tfidf.transform([tokenizer(name)])
    r = cosine_similarity(t, tfidf_features)
    r = pd.Series(r[0]).sort_values(ascending=False)
    return r


def cal_similarity_by_editdistance(name, threshold):
    """
    计算name的相似度
    :param name:
    :return:
    """
    name = standardize(name)
    length = len(name)
    size = int(length * (1 - threshold))
    namelist = list(dis_name_code_dict.keys())
    fnamelist = list(filter(lambda x: length - size <= len(x) <= length + size, namelist))


def match(code1, name1, threshold=0.9):
    """

    :param code1:
    :param name1:
    :return:
    """
    try:
        name = standardize(name1)
        code = standardize(code1)
    except Exception as e:
        print(f'{code1}, {name1} 格式有误，未处理！')
        print(e)
        return
    if name in dis_name_code_dict:
        """
        如果匹配上的话，返回(状态码, 原始code, 原始name, 匹配的字典code, 匹配的name, 匹配标记)

        匹配标记
            0：表示系统匹配成功
            -1：表示系统未匹配成功，待人工校核
            1：表示系统未匹配成功，已人工校核
        """
        if code in dis_name_code_dict[name]:
            return 10, code, name, code, name, 0
        else:
            return 11, code, name, dis_name_code_dict[name], name, 0
    r = cal_similarity_by_tfidf(name)
    r1 = r[r > threshold]
    rlist = []
    if not r1.empty:
        for i, v in r1.items():
            print(i, v)
            rlist.append((12, code, name, df.iloc[i, 0], df.iloc[i, 1], -1))
    else:
        """
        如果未能匹配，返回 相同的code对应的name，及达到匹配度的前三个name对应的code
        [
            (状态码, 原始code, 原始name, 原始code, 原始code对应的name, -1),
            (状态码, 原始code, 原始name, 匹配的字典code1, 匹配的name1, -1),
            (状态码, 原始code, 原始name, 匹配的字典code2, 匹配的name2, -1),
            (状态码, 原始code, 原始name, 匹配的字典code3, 匹配的name3, -1),
        ]
        """
        if code in dis_code_name_dict:
            rlist.append((2, code, name, code, dis_code_name_dict[code], -1))

        r1 = r[:5]
        for i, v in r1.items():
            print(i, v)
            rlist.append((2, code, name, df.iloc[i, 0], df.iloc[i, 1], -1))
        if len(rlist) == 0:
            rlist.append((2, code, name, -1, -1, -1))
    return 2, rlist


def update_dic(dft):
    """
    更新标注字典库
    :param dft:
    :return:
    """
    dft = dft[dft.iloc[:, -1].apply(int) == 1]# 1表示已经经过业务专家确认过的
    flag = 0
    count1, count2 = 0, 0
    for line in dft.itertuples():
        if line[3] not in dis_name_code_dict:
            dis_name_code_dict[line[3]] = [line[4]]
            print('新增dis_name_code_dict：{}:{}'.format(line[3], [line[4]]))
            flag = 1
            count1 += 1
        if line[4] not in dis_code_name_dict and line[5]:
            dis_code_name_dict[line[4]] = line[5]
            print('新增dis_code_name_dict：{}:{}'.format(line[4], line[5]))
            flag = 1
            count2 += 1
    if flag == 1:
        data_dir = os.path.join(BASE_DIR, projname, 'data')
        backups_dir = os.path.join(data_dir, 'backups')
        if not os.path.exists(backups_dir):
            os.mkdir(backups_dir)
            print(f'新建备份目录： {backups_dir}')

        if os.path.exists(os.path.join(data_dir, 'dis_name_code_dict.pkl')) and os.path.exists(os.path.join(data_dir, 'dis_code_name_dict.pkl')):
            now = datetime.now()
            nowstr = now.strftime('%Y%m%d%H%M%S')
            d1 = os.path.join(backups_dir, 'dis_name_code_dict_{}.pkl'.format(nowstr))
            d2 = os.path.join(backups_dir, 'dis_code_name_dict_{}.pkl'.format(nowstr))
            shutil.move(os.path.join(data_dir, 'dis_name_code_dict.pkl'), d1)
            shutil.move(os.path.join(data_dir, 'dis_code_name_dict.pkl'), d2)
            print('备份字典：{}'.format(d1))
            print('备份字典：{}'.format(d2))
        picklew.dump2File(dis_name_code_dict, os.path.join(data_dir, 'dis_name_code_dict.pkl'))
        picklew.dump2File(dis_code_name_dict, os.path.join(data_dir, 'dis_code_name_dict.pkl'))
    print(f'finished！dis_name_code_dict新增 {count1} 条记录！ dis_code_name_dict新增 {count2} 条记录！')


def tokenizer(x):
    """
    分词
    :param x:
    :return:
    """
    x = re.sub(r'[a-zA-Zαβγδ]+', 'alphabet', x)
    x = re.sub(r'[0-9]+', 'num', x)  # 把数字替换为num
    return ' '.join(jieba.lcut(x))


df = pd.read_csv('/Users/luoyonggui/Documents/work/dataset/1/icd10_leapstack.csv')
# 3bitcode
# df3 = pd.read_excel('/Users/luoyonggui/Documents/work/dataset/1/3bitcode.xls', skiprows=[0])
# df4 = pd.read_excel('/Users/luoyonggui/Documents/work/dataset/1/4bitcode.xls', skiprows=[0]).iloc[:, 1:]
dis_name_code_dict = picklew.loadFromFile(os.path.join(BASE_DIR, 'dicproj/data/dis_name_code_dict.pkl'))
dis_code_name_dict = picklew.loadFromFile(os.path.join(BASE_DIR, 'dicproj/data/dis_code_name_dict.pkl'))





df['diag_name_'] = df['diag_name'].apply(tokenizer)
# df['diag_name_'] = df['diag_name'].apply(lambda x: ' '.join(jieba.lcut(x)))
x_test = df['diag_name_']
print('load stopwords')
with open(os.path.join(BASE_DIR, 'dicproj/data/stopwords_zh.dic'), encoding='utf8') as f:
    stopwords = [s.strip() for s in f.readlines()]
print('building tfidf array')
tfidf = TfidfVectorizer(stop_words=stopwords, token_pattern=r"(?u)\b\w+\b")
tfidf.fit(x_test)
tfidf_features = tfidf.transform(x_test).toarray()
print('building tfidf array completed')
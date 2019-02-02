# coding: utf-8

import sys
from collections import Counter
from docx import Document
import os
import docx
import subprocess
import shutil
import random
import string
from itertools import chain
import time
from zipfile import ZipFile
from bs4 import BeautifulSoup

import numpy as np
import tensorflow.contrib.keras as kr



if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False


def native_word(word, encoding='utf-8'):
    """如果在python2下面使用python3训练的模型，可考虑调用此函数转化一下字符编码"""
    if not is_py3:
        return word.encode(encoding)
    else:
        return word


def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content

def open_file(filename, mode='r'):
    """
    常用文件操作，可在python2和python3间切换.
    mode: 'r' or 'w' for read or write
    """
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)



#def word_file(word_Data):
#    """根据data源的位置产生并列出word_file's trainSet"""
#    for dirname in os.listdir(word_Data):
#        if not os.path.exists(trainSet_path+'/'+dirname):
#            os.makedirs(trainSet_path+'/'+dirname)
#        else:
#            continue
##            shutil.rmtree(trainSet_path+'/'+dirname)
#        try:
#            file_type = os.listdir(word_Data+'/'+dirname)
#            for dirs in file_type:
#                files = os.listdir(word_Data+'/'+dirname+'/'+dirs)
#                for doc_type in files:
#                    random_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
#                    new_file_name = random_str+'.docx'
#                    if doc_type.endswith('.doc'):
#                        subprocess.check_output(['soffice', '--headless', '--convert-to', 'docx', word_Data+'/'+dirname+'/'+dirs+'/'+doc_type])
#                        convert_file = doc_type+'x'
#                        shutil.move(convert_file,trainSet_path+'/'+dirname+'/'+new_file_name)
#    
#                    elif doc_type.endswith('.docx'):
#                        shutil.copy(word_Data+'/'+dirname+'/'+dirs+'/'+doc_type,trainSet_path+'/'+dirname+'/'+new_file_name)
#        except:
#            pass
#        try:
#            files = os.listdir(word_Data+'/'+dirname)
#            for doc_type in files:
#                time.sleep(0.5)
#                random_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
#                new_file_name = random_str+'.docx'
#                if doc_type.endswith('.doc'):
#                    subprocess.check_output(['soffice', '--headless', '--convert-to', 'docx', word_Data+'/'+dirname+'/'+doc_type])
#                    convert_file = doc_type+'x'
#                    shutil.move(convert_file,trainSet_path+'/'+dirname+'/'+new_file_name)    
#                elif doc_type.endswith('.docx'):
#                    shutil.copy(word_Data+'/'+dirname+'/'+doc_type,trainSet_path+'/'+dirname+'/'+new_file_name)
#        except:
#            pass 
#

def list_word(dataSet_dir):
    """读取word_file's trainSet的数据，使之成为list_word"""
#    word_file(word_Data)
    words_collect = []
    for dirname in os.listdir(dataSet_dir):
        for types in os.listdir(dataSet_dir+'/'+dirname):
            for _file in os.listdir(dataSet_dir+'/'+dirname+'/'+types):
                word_collect = []
                try:
    #                docx_file = docx.Document(dataSet_dir+'/'+dirname+'/'+_file[:-4]+"docx")
                    document=ZipFile(dataSet_dir+'/'+dirname+'/'+types+'/'+_file[:-4]+"docx")
                    xml = document.read('word/document.xml')
                    wordObj=BeautifulSoup(xml.decode("utf-8"), "lxml")
                    texts=wordObj.findAll("w:t")                
                except:
    #                os.remove(dataSet_dir+'/'+dirname+'/'+_file[:-4]+"docx")
                    pass
    #            for para in docx_file.paragraphs:
    #                word_collect.append(para.text.split('\t')[0].split('\n'))
    #                word_collect.append(para.text.split('\n')[0])
                for text in texts:
                    word_collect.append(text.text.split('\t')[0].split('\n'))
                word_ = list(chain.from_iterable(word_collect))
                word_.insert(0, 'labels_and_content_split_point')
                word_.insert(0, dirname)
                word_content = ''.join(word_)
                words_collect.append(word_content)
    return words_collect

def write_word_to_file(word_Data, Word_dir):
    """写word的数据进file"""
    word_list_change = []
    word_list_end = []
    word_list_all = []
    word_list = list_word(word_Data)
    for num in range(len(word_list)):
        word_list_change.append(list(native_content(word_list[num])))
    for n in range(len(word_list_change)):    
        for empty in range(word_list_change[n].count(' ')):
            word_list_change[n].remove(' ')
        word_list_end.append(''.join(word_list_change[n]))
#        for empty in word_list_change[n]:
#            if empty is None or empty is ' ':
#                continue
#            else:
#                word_list_end.append(empty)
#        word_list_all.append(''.join(word_list_end))
    for line in word_list_end:
#        print (line)
        with open(Word_dir, 'a') as fp:
            fp.write(line+'\n')


def read_word(filename):
    """读取write_word_to_file生成的文本数据"""
#    word_list = open(word_Data)
    contents, labels = [], []
    with open_file(filename) as fp:
        for line in fp:
            try:
                label, content = line.strip().split('labels_and_content_split_point')
                if content:
                    contents.append(list(native_content(content)))
                    labels.append(native_content(label))
            except:
                pass
#    for num in range(len(contents)):
#        for empty in range(contents[num].count(' ')):
#            contents[num].remove(' ')
    return contents, labels


def build_vocab(trainWord_dir, vocab_dir, vocab_size=5000):
    """根据训练集构建词汇表，存储"""
    data_train, _ = read_word(trainWord_dir)

    all_data = []
    for content in data_train:
        all_data.extend(content)

    counter = Counter(all_data)
    counter_len = len(counter)
    count_pairs = counter.most_common(counter_len - 1)
    words, _ = list(zip(*count_pairs))
    # 添加一个 <PAD> 来将所有文本pad为同一长度
    words = ['<PAD>'] + list(words)
    open_file(vocab_dir, mode='w').write('\n'.join(words) + '\n')


def read_vocab(vocab_dir):
    """读取词汇表"""
    # words = open_file(vocab_dir).read().strip().split('\n')
    with open_file(vocab_dir) as fp:
        # 如果是py2 则每个值都转化为unicode
        words = [native_content(_.strip()) for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def read_category(trainSet_path):
    """读取分类目录，固定"""
#    categories = ["外包","运维","代理"] 
    categories = []
    for dirname in os.listdir(trainSet_path):
        categories.append(dirname)
    
#    categories = ['运维', '体育']

    categories = [native_content(x) for x in categories]

    cat_to_id = dict(zip(categories, range(len(categories))))

    return categories, cat_to_id


def to_words(content, words):
    """将id表示的内容转换为文字"""
    return ''.join(words[x] for x in content)


def process_file(filename, word_to_id, cat_to_id, max_length=5000):
    """将文件转换为id表示"""
    contents, labels = read_word(filename)
    print (max_length)

    data_id, label_id = [], []
    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])
        label_id.append(cat_to_id[labels[i]])

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    y_pad = kr.utils.to_categorical(label_id)  # 将标签转换为one-hot表示

    return x_pad, y_pad


def batch_iter(x, y, batch_size=64):
    """生成批次数据"""
    data_len = len(x)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = x[indices]
    y_shuffle = y[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]

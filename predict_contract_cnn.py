# coding: utf-8

from __future__ import print_function

import sys
import os
import tensorflow as tf
import tensorflow.contrib.keras as kr
from itertools import chain

from zipfile import ZipFile
from bs4 import BeautifulSoup
from contract_recognition.cnn_contract_model import TCNNConfig, TextCNN
from contract_recognition.data_processing.contract_loader import read_category, read_vocab


try:
    bool(type(unicode))
except NameError:
    unicode = str

base_dir = 'cnn_model/contract'
trainSet_dir = "cnn_model/contract/trainSet"
vocab_dir = os.path.join(base_dir, 'contract.vocab.txt')

save_dir = 'cnn_model/checkpoints/contract_cnn'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径

if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False

def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content

def docx_url(filename):
    word_collect = []
    document=ZipFile(filename)
    xml = document.read('word/document.xml')
    wordObj=BeautifulSoup(xml.decode("utf-8"), "lxml")
    texts=wordObj.findAll("w:t")
    for text in texts:
        word_collect.append(text.text.split('\t')[0].split('\n'))
    word_ = list(chain.from_iterable(word_collect))
    content = ''.join(word_)
    return content

def read_text(filename):
    with open(filename, 'r') as rp:
        content = rp.read()
    return content

def file_read(way,filename):
    word_collect = []
    if way == "docx":
        content = docx_url(filename)
    elif way == "txt":
        content = read_text(filename)
    return content

def content_message(way,filename):
    file_content = []
    file_content_end = []
    read_content = file_read(way,filename)
    for num in range(len(read_content)):
        file_content.append(list(native_content(read_content[num])))
    for n in range(len(file_content)):
        for empty in file_content[n]:
            if empty is None or empty is ' ':
                continue
            else:
                file_content_end.append(empty)
    return (''.join(file_content_end))

class CnnModel:
    def __init__(self):

        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category(trainSet_dir)
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
#        self.config.seq_length = 1
#        print (self.categories, self.cat_to_id)
#        print (self.words, self.word_to_id)
#        print (self.config.vocab_size)
        self.model = TextCNN(self.config)
#
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
#        self.this = saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self,way,filename):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        message = content_message(way,filename) 
        content = unicode(message)
        
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]





if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("""usage: python %s [doc/txt/...or other content file""" % sys.argv[0])
    filename = sys.argv[1]  
    way = filename.split(".")[-1]
    cnn_contract_model = CnnModel()
    
#    test_demo = ['三星ST550以全新的拍摄方式超越了以往任何一款数码相机',
#                 '热火vs骑士前瞻：皇帝回乡二番战 东部次席唾手可得新浪体育讯北京时间3月30日7:00',
#		 '小米手机研发了人脸识别，以及空中隐形飞行蜜蜂',
#                 '今天的天气是雨天']
                   
#不过由于篮球场地被一家时装秀给订包了，于是该场地举办了时装秀展示各种划时代风格的衣服或裤子等']
#    for i in test_demo:
    print(cnn_contract_model.predict(way, filename))

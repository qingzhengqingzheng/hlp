# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 12:05:42 2020

@author: 彭康
"""

import os
from utils import wav_to_mfcc,text_to_int_sequence
import tensorflow as tf
import random
import config

def data_process(
    data_path,
    batch_size,
    if_train_or_test, #train和test的返回数据不一样
    n_mfcc = config.configs_other["n_mfcc"]
    ):
    files = os.listdir(data_path) #得到文件夹下的所有文件名称
    #除去最后一个文本txt的所有音频文件
    audio_nums = len(files)-1
    if batch_size>audio_nums:
        batch_size=audio_nums
    #构建一个batch_size长度的随机整数list,且无序(防止测试数据重复)
    file_list_num = random.sample(range(audio_nums),batch_size)
    #对应数据文件夹下的文本list
    text_index = len(files)-1
    text_list=open(data_path+'/'+files[text_index],"r").readlines()

    mfccs_list = []
    labels_str_list = []

    for i in file_list_num:
        filepath = data_path +'/'+files[i]
        mfcc = wav_to_mfcc(n_mfcc=n_mfcc,wav_path=filepath)
        mfccs_list.append(mfcc)
        str=text_list[i][12:len(text_list[i])-1].lower()
        labels_str_list.append(str)
    mfccs_numpy = tf.keras.preprocessing.sequence.pad_sequences(mfccs_list,padding='post',dtype='float32')
    inputs = tf.convert_to_tensor(mfccs_numpy)
    if if_train_or_test == 'test':
        return inputs,labels_str_list
    else:
        labels_list=[]
        label_length_list=[]
        for i in range(len(labels_str_list)):
            labels_list.append(text_to_int_sequence(labels_str_list[i]))
            label_length_list.append(len(labels_str_list[i]))
        labels_numpy = tf.keras.preprocessing.sequence.pad_sequences(labels_list,padding='post')
        labels = tf.convert_to_tensor(labels_numpy)
        label_length=tf.convert_to_tensor(label_length_list)
        return inputs,labels,label_length


if __name__=="__main__":
    pass
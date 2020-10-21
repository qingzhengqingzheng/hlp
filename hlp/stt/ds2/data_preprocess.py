import io
import os
import re
import tensorflow as tf
import librosa
import numpy as np
from model import DS2
import json
from utils import get_all_data_path,create_dataset,tokenize,get_audio_feature,text_row_process,get_config,set_config


def get_text_number(data_path):
    files = os.listdir(data_path)
    with open(data_path + "/data.txt","a") as f:
        for path in files:
            f.write(path[0] + "\n")


#基于数据文件夹来进行加载数据(可以是一个文件夹列表也可以是单个文件夹)
def load_dataset_train(data_path, num_examples=None):
    if isinstance(data_path,str):
        #单个数据文件夹
        #number语料的文本文件构建
        if not os.path.exists(data_path+"/data.txt"):
            get_text_number(data_path)
        text_data_path,audio_data_path_list = get_all_data_path(data_path)
        mfccs_list,sentences_list = create_dataset(
            data_path,
            text_data_path,
            audio_data_path_list,
            num_examples
            )
        mfccs_numpy = tf.keras.preprocessing.sequence.pad_sequences(
            mfccs_list,
            padding='post',
            dtype='float32'
            )
        input_tensor = tf.convert_to_tensor(mfccs_numpy)
        target_sequence,sentences_length_list,target_tokenizer = tokenize(sentences_list)
        target_tensor = tf.convert_to_tensor(target_sequence)
        target_length = tf.convert_to_tensor(sentences_length_list)
        #保存index_word到json文件
        configs = get_config()
        index_word_json_path = configs["other"]["index_word_json_path"]
        with open(index_word_json_path,'w',encoding="utf-8") as f:
            json.dump(target_tokenizer.index_word, f, ensure_ascii=False,indent=4)
        set_config("preprocess","max_inputs_len",input_tensor.shape[1])
        set_config("model","dense_units",len(target_tokenizer.index_word)+2)
        return input_tensor,target_tensor,target_length
    else:
        #若data_path是多个数据文件夹路径组成的list
        mfccs_lists=[]
        sentences_lists=[]
        for path in data_path:
            text_data_path,audio_data_path_list = get_all_data_path(path)
            mfccs_list,sentences_list = create_dataset(path,text_data_path,audio_data_path_list,None)
            mfccs_lists.extend(mfccs_list)
            sentences_lists.extend(sentences_list)
        mfccs_lists=mfccs_lists[:num_examples]
        sentences_lists=sentences_lists[:num_examples]
        mfccs_numpy = tf.keras.preprocessing.sequence.pad_sequences(mfccs_lists,padding='post',dtype='float32')
        input_tensor = tf.convert_to_tensor(mfccs_numpy)
        target_sequence,sentences_length_list,target_tokenizer = tokenize(sentences_lists)
        target_tensor = tf.convert_to_tensor(target_sequence)
        target_length = tf.convert_to_tensor(sentences_length_list)
        #保存index_word到json文件
        configs = get_config()
        index_word_json_path = configs["other"]["index_word_json_path"]
        with open(index_word_json_path,'w',encoding="utf-8") as f:
            json.dump(target_tokenizer.index_word, f, ensure_ascii=False,indent=4)
        set_config("preprocess","max_inputs_len",input_tensor.shape[1])
        set_config("model","dense_units",len(target_tokenizer.index_word)+2)
        return input_tensor,target_tensor,target_length

def load_dataset_test(data_path, num_examples=None):
    if not os.path.exists(data_path+"/data.txt"):
        get_text_number(data_path)
    configs = get_config()
    text_data_path,audio_data_path_list = get_all_data_path(data_path)
    mfccs_list = get_audio_feature(data_path,audio_data_path_list,num_examples)
    labels_list = []
    with open(data_path+"/"+text_data_path,"r") as f:
        sen_list = f.readlines()
    for sentence in sen_list[:num_examples]:
        labels_list.append(text_row_process(sentence))
    mfccs_list = mfccs_list[:num_examples]
    labels_list = labels_list[:num_examples]
    mfccs_numpy = tf.keras.preprocessing.sequence.pad_sequences(
            mfccs_list,
            maxlen=configs["preprocess"]["max_inputs_len"],
            padding='post',
            dtype='float32'
            )
    input_tensor = tf.convert_to_tensor(mfccs_numpy)
    return input_tensor,labels_list
    
    

if __name__ == '__main__':
    pass
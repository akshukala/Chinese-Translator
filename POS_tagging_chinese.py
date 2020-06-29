# -*- coding: utf-8 -*-
"""
Created on Fri Jan  10 10:34:28 2020

@author: akshay.kale
"""

import re
import pandas as pd
from emoji import UNICODE_EMOJI
import jieba.posseg as pseg
from googletrans import Translator
 

translator = Translator()

'''Data Cleaning: Removing the unwanted data from the data.'''
def get_replace_list(raw, lang_type):
    date_strings_with_brackets = re.findall(r'\(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d*\)', raw)
    date_strings = re.findall(r'Chat Started: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d*', raw)
    visitor_string = re.findall(r'Visitor \d+:', raw)
    join_string = re.findall(r'\*\*\* Visitor \d+ joined the chat \*\*\*', raw)
    left_string = re.findall(r'\*\*\* Visitor \d+ left the chat \*\*\*', raw)
    bot_string = re.findall(r'bot_proactive:', raw)
    emojis = [i for i in raw.split() if i in UNICODE_EMOJI]
    if lang_type == 1:
        chinese_name = re.findall(r'客服：\d+: ', raw)
        customer_join_string = re.findall(r'\*\*\* 客服：\d+ joined the chat \*\*\*', raw)
    else:
        chinese_name = re.findall(r'Customer Service: \d+: ', raw)
        customer_join_string = re.findall(r'\*\*\* Customer Service: \d+ joined the chat \*\*\*', raw)
    '''Searching all possible unwanted data and then removing from the data'''
    final_list = list(set(date_strings_with_brackets)) + list(set(date_strings)) + list(set(visitor_string)) \
            + list(set(join_string)) + list(set(left_string)) + list(set(chinese_name)) \
            + list(set(customer_join_string)) + list(set(bot_string)) + list(set(emojis))
    for i in final_list:
        raw = raw.replace(i, "")
        raw = raw.replace('\n','').replace('\r','')
    return raw     

def pos_tagging_replacement(raw):
    replace_words = []
    '''Getting POS for each word and if it is noun or proper noun replace it with some different word'''
    words = pseg.cut(raw)
    cnt = 65
    for word, flag in words:
        if flag.startswith('n'):
            if flag.startswith('nr'):
                continue
            else:
                if cnt == 90:
                    cnt = cnt + 7
                replace_words.append((word,"N"+ str(cnt) + chr(cnt)))
                cnt = cnt + 1    
    for i,word in enumerate(replace_words):
        raw = raw.replace(word[0], word[1])
    return (raw, replace_words)


def translating_POS_tags(data):
    ''' Translating the text to English with removal of all the Nouns '''
    result = []
    for d in data:
        result.append((translator.translate(d[0]).text, d[1]))                
    return result

def back_to_original_text(data, tags):
    '''Replacing the tags which we had given to the nouns, so that we get original data'''
    text = data
    mapping = tags
    for word in mapping:
        text = re.sub(word[1], word[0], text)
    return text

''' Reading the data'''
raw = pd.read_excel("ChineseTestData.xlsx")

result = []

'''Iterating for multiple rows and creating the output excel'''
for index, row in raw.iterrows():
    temp_result = []
    print(index + 1)
    data = row[0]
    temp_result.append(data)
    final_data = get_replace_list(data, 1)
    print (final_data)
    temp_result.append(final_data)
    temp_result.append(translator.translate(final_data).text)
    replace_data = pos_tagging_replacement(final_data)
    temp_result.append(replace_data[1])
    temp_result.append(replace_data[0])
    replace_translated = translator.translate(replace_data[0]).text 
    temp_result.append(replace_translated)
    
    pos_translate = translating_POS_tags(replace_data[1])
    print (pos_translate)
        
    #print("-------------------------------------------------------------")
    back_to_original = back_to_original_text(replace_translated, pos_translate)
    temp_result.append(pos_translate)
    temp_result.append(back_to_original)
    #temp_result.append(translator.translate(back_to_original).text)
    #print (back_to_original)
    result.append(temp_result)
df = pd.DataFrame(result)
df.columns = ["Original Text", "Chinese Text", "Translated to English", "POS Tags", "Text With Tags", "Translated to English",
              "POS Tags Translation", "Replaced POS With Original"]

df.to_excel("POS_Tagging_chinese.xlsx")





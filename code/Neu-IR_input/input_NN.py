#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import numpy as np
from sklearn.cross_validation import train_test_split
import xml.dom.minidom
from xml.dom.minidom import parse
import sys
import string
reload(sys)
sys.setdefaultencoding('utf-8')


def CreateDicFromXml(filename):
    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement
    queries = collection.getElementsByTagName("query")
    
    dic = {}
    for query in queries:
        dic[query.getAttribute("id")]=query
    return dic


def GetQuery(dic, id_num):
    key = str(id_num)
    if not dic.has_key(key):
        return 'The query: '+key+' is not exist!'
    
    query = dic[key]
    title = query.getElementsByTagName('title')[0]
    res = title.childNodes[0].data
    description = query.getElementsByTagName('description')[0]
    if description.hasChildNodes():
        paras = description.getElementsByTagName('paragraph')
        for para in paras:
            res += ' '+para.childNodes[0].data
    return res


def GetAnswer(train_answer_id):
    filename = r'1xml/'+train_answer_id+'.xml'
    f = open(filename,'rb')
    html = f.read().decode('utf-8')
    f.close()
    html = html.replace('\r\n', '\n')
    train_answer_title = re.findall('<title>(.*?)</title>',html,flags=re.S)[0]   
    train_answer_title = train_answer_title.replace('\n', '')
    train_answer_transcript = re.findall('<transcript>(.*?)</transcript>',html,flags=re.S)[0]
    train_answer_transcript = train_answer_transcript.replace('\n', '')
    flag = 0
    if train_answer_transcript.find(',') >=0:
        flag = 1
    train_answer_transcripts = train_answer_transcript.split('||')
    transcript = []
    i = 0
    for train_answer_transcript in train_answer_transcripts:
        i = i+1
        if (i!=1) and (i!=2):
            transcript.append(train_answer_transcript)
    if flag == 0:
        train_answer_transcript = '. '.join(transcript)
    else:
        train_answer_transcript = ' '.join(transcript)
    train_answer = train_answer_title+' '+train_answer_transcript
    return train_answer.encode('utf-8') 


def Padding(string):
    string = string.lower()
    #string = string.replace(',',' ').replace('.',' ').replace('?',' ').replace('-',' ').replace('(',' ').replace(')',' ').replace('!',' ').replace('"',' ').replace(';',' ')
    #string = string.replace(',',' , ').replace('.',' . ').replace('?',' ? ').replace('-',' - ').replace('(',' ( ').replace(')',' ) ').replace('!',' ! ').replace('"',' " ').replace(';',' ; ')
    string = string.replace('...','.').replace(',',' , ').replace('.',' . ').replace('?',' ? ').replace('-',' ').replace('(',' ').replace(')',' ').replace('!',' ! ').replace('"',' ').replace(';',' ; ').replace('--',' ').replace(':',' : ').replace('“',' ').replace('”',' ')
    words = string.split(' ')    
    while '' in words:
        words.remove('')
    if len(words)< 200:
        wordLIst = words
        for i in range(len(words),200):
            wordLIst.append('<a>')
    else:
        wordLIst = []
        for i in range(0,200):
            wordLIst.append(words[i])
    string_norm = '_'.join(wordLIst)
    string_norm = string_norm+'_'
    return string_norm.encode('utf-8') 


def DicCriterion():
    file_evalData = open('evalData.txt','r')
    lines = file_evalData.read().split('\n')
    file_evalData.close()
    while '' in lines:
        lines.remove('')    
    dic = {}
    query_ids = []
    for line in lines:
        terms = line.split(' ')
        query_id = terms[0]
        answer_id = terms[2]
        if query_id not in query_ids:
            query_ids.append(query_id)
            dic[query_id] = answer_id   
        else:
            dic[query_id] = dic[query_id]+','+answer_id    
    return dic


def DicSimilar(dic_criterion):
    file_IRresult = open('4SeaResCombine.txt','r')
    lines = file_IRresult.read().split('\n')
    file_IRresult.close()
    while '' in lines:
        lines.remove('')       
    query_ids = []
    dic = {}
    for line in lines:
        terms = line.split(' ')
        query_id = terms[0]
        answer_id = terms[2]
        train_answer_ids = dic_criterion.get(str(query_id))
        train_answer_ids = train_answer_ids.split(',')            
        if answer_id not in train_answer_ids:
            if query_id not in query_ids:
                query_ids.append(query_id)
                dic[query_id] = answer_id
            else:
                dic[query_id] = dic[query_id]+','+answer_id     
    return dic

def DicEval():
    file_IRresult = open('4SeaResCombine.txt','r')
    lines = file_IRresult.read().split('\n')
    file_IRresult.close()
    while '' in lines:
        lines.remove('')       
    query_ids = []
    dic = {}
    for line in lines:
        terms = line.split(' ')
        query_id = terms[0]
        answer_id = terms[2]
        if query_id not in query_ids:
            query_ids.append(query_id)
            dic[query_id] = answer_id
        else:
            dic[query_id] = dic[query_id]+','+answer_id   
    return dic


if __name__ == '__main__':
    #queries---train_id;test_id
    train_data = []
    for i in range(1,674):
        train_data.append(i)
    train_target = np.ones(len(train_data))           
    train_query_ids, test_query_ids, y_train, y_test = train_test_split(train_data, train_target, test_size=225, random_state=0)
   
    filename = r'__AllQueriesMultiLine0131.xml'
    #dic_query_xml[query_id] = query
    dic_query_xml = CreateDicFromXml(filename)  
    #dic_criterion[query_id] = positive_answer_id_s
    dic_criterion = DicCriterion()
    #dic_similar[query_id] = negative_answer_id_s
    dic_similar = DicSimilar(dic_criterion)
    #dic_eval[query_id] = galago_retrieval_answer_id_s
    dic_eval = DicEval()

    """    
    # generate file_train
    file_train = open('NN_input/train','w+') 
    total = 0
    i = 0
    for train_query_id in train_query_ids:
        i = i+1
        train_query = GetQuery(dic_query_xml, train_query_id)
        train_query_norm = Padding(train_query)
        train_answer_ids = dic_criterion.get(str(train_query_id))
        train_answer_ids = train_answer_ids.split(',')             
        for train_answer_id in train_answer_ids:
            total = total+1
            train_answer = GetAnswer(train_answer_id)           
            train_answer_norm = Padding(train_answer)            
            file_train.write('1'+' '+'qid:%s'%train_query_id+' '+train_query_norm+' '+train_answer_norm+'\n')
            file_train.flush() 
            train_sim_answer_ids = dic_similar.get(str(train_query_id))
            train_sim_answer_ids = train_sim_answer_ids.split(',')
            answer_num = 0 
            for train_sim_answer_id in train_sim_answer_ids:
                train_sim_answer = GetAnswer(train_sim_answer_id)
                train_sim_answer_norm = Padding(train_sim_answer)            
                file_train.write('0'+' '+'qid:%s'%train_query_id+' '+train_query_norm+' '+train_sim_answer_norm+'\n')
                file_train.flush()
                answer_num = answer_num+1              
                if answer_num == 99:
                    break            
           
    file_train.close() 
    print 'train_file done!'
    print 'train_num:'+ str(i)
    print 'train_num_all:'+ str(total)
    """

    query_no_answer_ids = []
    file_test_no_answer = open('100_no_answer_queryids.txt','r')    
    ids = file_test_no_answer.readlines()
    file_test_no_answer.close()
    for term in ids:
        term = term.replace('\r\n','')
        query_no_answer_ids.append(term)
 
    #file_test = open('NN_input/test1.sample','w+')
    file_test = open('NN_input/test1','w+')
    total = 0
    append_num = 0
    a = 0
    for test_query_id in test_query_ids:
        total = total+1
        #test_query:title+description
        test_query = GetQuery(dic_query_xml, test_query_id)
        #Fixed sentence length is 200
        test_query_norm = Padding(test_query)        
        test_answer_ids = dic_eval.get(str(test_query_id))
        #test_answer_ids: galago 1000 answer_id_s
        test_answer_ids = test_answer_ids.split(',')
        i = 0
        for test_answer_id in test_answer_ids:           
            test_answer = GetAnswer(test_answer_id)
            #Fixed sentence length is 200
            test_answer_norm = Padding(test_answer) 
            file_test.write(test_answer_id+' '+'qid:%s'%test_query_id+' '+test_query_norm+' '+test_answer_norm+'\n')
            i = i+1              
            if i == 100:
                break        
        if str(test_query_id) in query_no_answer_ids:
            append_num = append_num +1
            test_answer_ids = dic_criterion.get(str(test_query_id))
            test_answer_ids = test_answer_ids.split(',')
            for test_answer_id in test_answer_ids:
                a = a+1
                test_answer = GetAnswer(test_answer_id)
                test_answer_norm = Padding(test_answer) 
                file_test.write(test_answer_id+' '+'qid:%s'%test_query_id+' '+test_query_norm+' '+test_answer_norm+'\n')    
    file_test.close()    
    print 'test_file done!'
    print 'test_num:'+ str(total)
    print 'no answer query num: '+str(append_num)
    print 'no answer query answer num: '+str(a)
     
            
   
    
        
    
    
 

	

    

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import hw2_corpus_tool
from hw2_corpus_tool import get_data
from collections import defaultdict
import pycrfsuite
import sys
import time


# In[2]:


data_directory = sys.argv[1]
test_directory = sys.argv[2]
output_file = sys.argv[3]


# In[3]:


data = list(get_data(data_directory))
test = list(get_data(test_directory))


# In[4]:


feature_set = []
tag_set = []
for d in data:
    feature_d = []
    tag_d = []
    current_speaker = d[0].speaker
    for du_i in range(len(d)):
        du = d[du_i]
        feature_du = []
        if du_i == 0:
            feature_du.append('first_utterance')
        else:
            feature_du.append('not_first_utterance')
        if du.speaker != current_speaker:
            feature_du.append('speaker_changed')
            current_speaker = du.speaker
        else:
            feature_du.append('speaker_not_changed')
        if du.pos:
            posdict = defaultdict(int)
            i = 0
            j = 0
            for po in du.pos:
                if(po.pos):
                    if i == 0:
                        p = 'first_pos_'+po.pos
                        feature_du.append(p)
                    if i == len(du.pos)-1:
                        p = 'last_pos_'+po.pos
                        feature_du.append(p)
                    posdict[po.pos] += 1
                    p = 'pos_'+po.pos
                    feature_du.append(p)
                    i += 1;
                if(po.token):
                    if j == 0:
                        t = 'first_token_'+po.token
                        feature_du.append(t)
                    if j == len(du.pos)-1:
                        t = 'last_token_'+po.token
                        feature_du.append(t)
                    t = 'token_'+po.token
                    feature_du.append(t)
                    j += 1;
            for postag in posdict.keys():
                feature = postag+'_'+str(posdict[postag])
                feature_du.append(feature)
        else:
            feature_du.append('no_pos')
            feature_du.append('no_token')
        txt = du.text.split()
        for tx in range(len(txt)-1):
            feature_du.append(txt[tx])
            if len(txt) > 1:
                x = 'bigram_'+txt[tx]+'_'+txt[tx+1]
                feature_du.append(x)
        if len(txt) > 1:
            feature_du.append(txt[-1])
        lf = 'text_length_'+str(len(txt))
        feature_du.append(lf)
        feature_d.append(feature_du)
        tag_d.append(du.act_tag)
    feature_set.append(feature_d)
    tag_set.append(tag_d)


# In[5]:


feature_test = []
for d in test:
    feature_d = []
    tag_d = []
    current_speaker = d[0].speaker
    for du_i in range(len(d)):
        du = d[du_i]
        feature_du = []
        if du_i == 0:
            feature_du.append('first_utterance')
        else:
            feature_du.append('not_first_utterance')
        if du.speaker != current_speaker:
            feature_du.append('speaker_changed')
            current_speaker = du.speaker
        else:
            feature_du.append('speaker_not_changed')
        if du.pos:
            posdict = defaultdict(int)
            i = 0
            j = 0
            for po in du.pos:
                if(po.pos):
                    if i == 0:
                        p = 'first_pos_'+po.pos
                        feature_du.append(p)
                    if i == len(du.pos)-1:
                        p = 'last_pos_'+po.pos
                        feature_du.append(p)
                    posdict[po.pos] += 1
                    p = 'pos_'+po.pos
                    feature_du.append(p)
                    i += 1;
                if(po.token):
                    if j == 0:
                        t = 'first_token_'+po.token
                        feature_du.append(t)
                    if j == len(du.pos)-1:
                        t = 'last_token_'+po.token
                        feature_du.append(t)
                    t = 'token_'+po.token
                    feature_du.append(t)
                    j += 1;
            for postag in posdict.keys():
                feature = postag+'_'+str(posdict[postag])
                feature_du.append(feature)
        else:
            feature_du.append('no_pos')
            feature_du.append('no_token')
        txt = du.text.split()
        for tx in range(len(txt)-1):
            feature_du.append(txt[tx])
            if len(txt) > 1:
                x = 'bigram_'+txt[tx]+'_'+txt[tx+1]
                feature_du.append(x)
        if len(txt) > 1:
            feature_du.append(txt[-1])
        lf = 'text_length_'+str(len(txt))
        feature_du.append(lf)
        feature_d.append(feature_du)
    feature_test.append(feature_d)


# In[6]:


trainer = pycrfsuite.Trainer(verbose=False)
for x_seq, y_seq in zip(feature_set, tag_set):
    trainer.append(x_seq, y_seq)


# In[7]:


trainer.set_params({
    'c1': 1.0,
    'c2': 1e-3,
    'max_iterations': 50,
    'feature.possible_transitions': True
})


# In[8]:


trainer.train('model.crfsuite')


# In[9]:


tagger = pycrfsuite.Tagger()


# In[10]:


tagger.open('model.crfsuite')


# In[11]:


tag_pred = [tagger.tag(x_seq) for x_seq in feature_test]


# In[12]:


outfile = open(output_file, 'w')
for tag in tag_pred:
    for t in tag:
        outfile.write(str(t))
        outfile.write('\n')
    outfile.write('\n')


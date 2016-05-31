#!/usr/bin/python
#
# created by ray on 2016-05-30
#

import pickle
from sklearn import svm
from nltk.corpus import wordnet as wn
from nltk.tag.perceptron import PerceptronTagger
from nltk import word_tokenize
from configs.global_para import DATA_PATH, MODEL_PATH

CONFIDENCE_THRESHOLD = 0.3

class ActionDetection(object):
    def __init__(self, train=False):
        self.tagger = PerceptronTagger()
        self.model = None
        # BOW: triangle, rectangle, circle, hand
        # verbs: draw, wave, rotate
        self.BOW = ['draw', 'wave', 'rotate', 'triangle', 'rectangle', 'circle', 'hand']
        self.VERBS = [wn.synset('draw.v.01'), wn.synset('wave.v.01'), wn.synset('rotate.v.01')]
        self.n_bow, self.n_verbs = len(self.BOW), len(self.VERBS)
        if train: self.train_svm()
        else: self.load_model()
        return

    def save_model(self):
        f = open(MODEL_PATH + 'action_detection.model', 'wb')
        pickle.dump(self.model, f)
        f.close()
        return

    def train_svm(self):
        with open(DATA_PATH+'action_detection_training_set.txt') as f:
            data = f.readlines()
        X, y = [],[]
        for line in data:
            line = line.strip()
            if not line: continue
            line = line.split(' ',1)
            X.append(self.extract_feature(line[1]))
            y.append(int(line[0]))
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X, y)
        self.model = lin_clf
        self.save_model()
        return

    def load_model(self):
        f = open(MODEL_PATH + 'action_detection.model', 'rb')
        self.model = pickle.load(f)
        f.close()
        return

    def extract_feature(self, sent):
        feature = [0] * (self.n_bow+self.n_verbs)
        verbs = [ w for w,pos in self.tagger.tag(word_tokenize(sent)) if pos=='VB' ]
        words = set(sent.split())
        for i in xrange(self.n_bow):
            feature[i] = 1 if self.BOW[i] in words else 0
        for i in xrange(self.n_verbs):
            if not verbs:
                feature[self.n_bow+i] = 0
            else:
                similarities = [ wn.path_similarity(self.VERBS[i],wn.synset(v+'.v.01')) for v in verbs ]
                feature[self.n_bow+i] = max(similarities)
        return feature

    def predict(self, sent):
        # classes: 0(rectangle), 1(circle), 2(triangle), 3(wave), 4(rotate)
        feature = self.extract_feature(sent)
        idx = self.model.predict([feature])[0]
        probs = self.model._predict_proba_lr([feature])[0]
        # return value: 0(none), 1-5(classes+1)
        if probs[idx]>CONFIDENCE_THRESHOLD: return idx+1
        else: return 0

if __name__ == '__main__':
    ad = ActionDetection(True)
    sents = ['give me five',
            'bring me some water please',
            'move yourself forward',
            'please draw a rectangle',
            'draw a circle to me',
            'draw a triangle please',
            'wave you hand to me',
            'rotate your hand']
    for sent in sents:
        ad.predict(sent)


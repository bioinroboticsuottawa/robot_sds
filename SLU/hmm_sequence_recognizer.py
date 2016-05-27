#!/usr/bin/python
#
# created by ray on 2016-04-09
#

import pickle
from nltk import word_tokenize
from nltk.tag.perceptron import PerceptronTagger
from hmm_model import HmmModel


class HmmSeqRecognizer(object):
  def __init__(self):
    self.hmm_models = []
    self.n_hmm = 0
    self.hmm2idx = {}
    self.idx2hmm = {}
    self.tagger = PerceptronTagger()
    return

  def batch_test(self, samples, label):
    tp,ns = 0,len(samples)
    for i in xrange(ns):
      idx = self.predict_sample(samples[i])
      if idx==label: tp+=1
    return tp,float(tp)/ns

  def predict_sample(self, sample):
    sample = [sample]
    probs = [ model.test(sample) for model in self.hmm_models ]
    return probs.index(max(probs))

  def predict_sentence(self, sentence):
    sample =  [[ tag for _,tag in self.tagger.tag(word_tokenize(sentence)) ]]
    probs = [ model.test(sample) for model in self.hmm_models ]
    return probs.index(max(probs))

  def add_model(self, name, model):
    self.hmm_models.append(model)
    self.hmm2idx[name] = self.n_hmm
    self.idx2hmm[self.n_hmm] = name
    self.n_hmm += 1

  def new_hmm(self, name, datapath, nhs, ne):
    print '=> adding HMM model \'%s\'...' % name
    hmm_model = HmmModel(nhs)
    hmm_model.train(datapath,ne)
    self.add_model(name, hmm_model)
    print '|  done'
    return

  def save_hmm(self, name, hmm_path):
    print '=> saving HMM model \'%s\'...' % name
    f = open(hmm_path, 'wb')
    pickle.dump(self.hmm_models[self.hmm2idx[name]], f)
    f.close()
    print '|  done'
    return

  def load_hmm(self, name, hmm_path):
    # print '=> adding HMM model \'%s\'...' % name
    f = open(hmm_path, 'rb')
    hmm_model = pickle.load(f)
    f.close()
    self.add_model(name, hmm_model)
    # print '|  done'
    return




# testing random sentences
def random_test():
  print 'number of hmm: %d' % hmm_recognizer.n_hmm
  test_set = ['what day is it today',
              'i have an apple',
              'please raise up your hand']
  for sentence in test_set:
    idx = hmm_recognizer.predict_sentence(sentence)
    name = hmm_recognizer.idx2hmm[idx]
    print 'predicting: %s' % sentence
    print 'result: %s(%d)' % (name, idx)

# this is another quick and dirty implementation (not really a cross validation)
# i will re-implement it later to do the real work
# currently it's just testing the accuracy of training set itself...
def cross_validation():
  tp_all,n_all = 0,0
  classes = ['declarative', 'imperative', 'interrogative']
  data_path = '../data/'
  for cls in classes:
    print '=> testing \'%s\' samples...' % cls
    datafile = data_path + 'training_' + cls + '.txt'
    idx = hmm_recognizer.hmm2idx[cls]
    model = hmm_recognizer.hmm_models[idx]
    samples = model.load_samples(datafile, False)
    n_all += len(samples)
    tp,acc = hmm_recognizer.batch_test(samples,idx)
    tp_all += tp
    print '|  true positives: %s, accuracy: %g' % (tp,acc)
  print '=> done (overall accuracy:%g)' % (float(tp_all)/n_all)
  return

def predefined_hmm(model_path, train_flag=False):
  # print '=> initializing recognizer...'
  recognizer = HmmSeqRecognizer()
  # configuration
  ne, nhs = 1, 5
  classes = ['declarative', 'imperative', 'interrogative']
  data_path = 'data/'
  # training new model or loading existing model
  for cls in classes:
    # get model file path as configured
    model_file = model_path + cls + '_%dhs%depoch.model' % (nhs, ne)
    if train_flag:
      # training new HMM models and then save to files
      data_file = data_path + 'training_' + cls + '.txt'
      recognizer.new_hmm(cls, data_file, nhs, ne)
      recognizer.save_hmm(cls, model_file)
    else:
      # loading HMM models from files
      recognizer.load_hmm(cls, model_file)
  # return the recognizer
  return recognizer

if __name__ == '__main__':
  # train or load hmm recognizer
  hmm_recognizer = predefined_hmm('data/models/', False)
  # testing the recognizer
  random_test()
  cross_validation()

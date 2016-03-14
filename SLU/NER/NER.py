__author__ = 'ray'

import os
from StanfordTagger_Revised import StanfordNERTagger
from NLTK import StanfordNERTagger
StanfordNERTagger.tag()

classpath = os.path.abspath('./stanford-ner.jar')+':'+os.path.abspath('./lib/*')
classifier = os.path.abspath('./classifiers/english.muc.7class.distsim.crf.ser.gz')

if 'CLASSPATH' in os.environ: os.environ['CLASSPATH'] = os.environ['CLASSPATH']+':'+classpath
else: os.environ['CLASSPATH'] = classpath
print 'CLASSPATH: ', os.environ['CLASSPATH']


st = StanfordNERTagger(classifier)
# st = StanfordNERTagger('/Users/Ray/Documents/Dev/stanford-ner/classifiers/english.conll.4class.distsim.crf.ser.gz')
# st = StanfordNERTagger('/Users/Ray/Documents/Dev/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz')
# ret = st.tag('Rami Eid is studying at Stony Brook University in New York'.split())
ret = st.tag('Ray bought 300 shares of Acme Corp. in 2006.'.split())
for r in ret: print r, type(r), type(r[0])

# who is the us president
# i visited London last summer
# I went to Ottawa from Toronto.
# Dr. Inkpen is a very nice professor.
# Ray bought 300 shares of Acme Corp. in 2006.


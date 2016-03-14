Named Entity Recognition (NER) modeul is implemented based on Stanford NER, which can be found from:
http://nlp.stanford.edu/software/CRF-NER.shtml

The tool provides is implemented in Java and several jars need to be included in java CLASSPATH in order to run the tool, also several pre-trained classifiers with different number of recognizable classes are provided along with the downloadable. In this directory, they are put separately under the 'classifiers' and 'lib' sub-directory.

There is a small bug in the original code in 'StanfordTagger.py' that it does not take the current system env CLASSPATH to run the main stanford-ner program, I modified the program to fix this. That's why there is a 'StanfordTagger_Revised.py' file in this directory.


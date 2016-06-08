# Spoken Dialog System for Robots
This repository contains the codes and documentation of a spoken dialog system for robots. The system allows humane-robot interaction through speech, and the core problem is to determine user's speech intents. User's intent can be either asking a question and expect answer from the robot, or giving a command and expect the robot to perform some action, or anything else.

The main program is a dialog manager which maintains a process pool of four sub-modules: ASR (automatic speech recognition), SLU (spoken language understanding), ACT(action) and TTS(text-to-speech). ASR is the input module that set up connections with a microphone and receive audio signals, the actual decoding is done by Google speech recognizer. SLU serves as a processing module which takes the text transcription from ASR as input, performs intent recognition and provide either action command or speech answer as output. ACT and TTS are the two output rendering module, ACT sends action commands to the robot, TTS submit text to online speech synthesis service and playback the returned audio.

## Controller Program
The "contrller.py" program communicate with the system using named pipe. The controller is supposed to be run as a separate process independent from the system, and the purpose is to enable dynamic control over the system, such as suspend/resume the system, or suspend/resume a specific module. It is particularly useful during debugging.

**available commands and syntax**

```
# start/exit all the modules
start
exit
```

```
# start/exit a specific module
<module_name>:start
<module_name>:exit
```

```
# sending message to a specific module
<module_name>:msg:<contents>
```

## System States
A finite state machine logic is being imposed on system states, the system at any time can be in one of these four states: CLOSED, WAITING, ACTIONING and ANSWERING. The initial state is at CLOSED because it's configured that no modules are running when the system starts. Start modules using the controller program and the system goes to the WAITING state, where some/all modules are working and waiting for input to process. When the ACT or the TTS module receives input, the robot start to perform action or speak to the user, these two states are called ACTIONING and ANSWERING, where incoming inputs will not be processed until the current action is done and the system returns to WAITING state.

## Speech Intent Recognition
Speech intent recognition is considered as a sequence classification problem, because the input is a text string of words and the length of string is variable. User intents are determined based on sentence grammar, interrogative sentences are considered as questions, imperative sentences are considerred as commands and declarative sentences for any other intent in a dialog between user and robot. Thus it comes down to solve a three-class classification problem.

In a general domain dialog system, the vocabulary is very large and thus it's not very feasible to use bag-of-words as feature. Another approach is to use part-of-speech tags as feature, which has a finite set. To allow inputs of variable lengths (number of words) as well as taking sequential relation into consideration, a hidden Markov model (HMM) is trained for each class.

In this project, we manually collected 450 sentences as training data, 150 sentences for each class. The training step is done by first pre-process the training sentences to remove punctuations and convert each word in the sentence into POS tag. Then by considering the number of hidden states as a hyperparameter to be fit, a HMM for each class can be trained using the Baum-Welch algorithm.

To test a new sentence, first transform it into a sequence of POS tags; then with the three trained HMMs we can calculate the probability of each class using the Viterbi algorithm; finally a softmax function is applied to normalize the three probabilities, and the class with highest probability the prediction result.


## Action Detection
Action detection is also a classification problem and it's only performed when the intent recognizer determines a user utterance as command. A support vector machine (SVM) classifier is trained for this problem. Training data are example commands to the robot. The features for SVM comsist of two parts, the first part is a bag-of-words (BOW) vector of all keywords in the training data, and the second part is a verb relevence vector. For each test sample, form BOW vector by checking if the keyword exist in the sample, form the verb relevance vector by calculating WordNet similarity between verbs in the vector and verbs in the sample.

## Usage
1. run the controller program<>

  ```
  ./controller.py
  ```
2. run the main program, system in state 'CLOSED'

  ```
  ./robot_sds.py
  ```
3. send command 'start' from the controller program to activate all the sub-modules, system in state 'WAITING'
4. speak to the microphone, depending on the speech contents, system in state 'ACTIONING' or 'ANSWERING'

- to start or suspend or resume a specific module

  ```
  <module_name>:start
  <module_name>:exit
  ```
- to send message to a specific module

  ```
  <module_name>:msg:<contents>
  ```

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
In a general domain dialog system, the vocabulary is very large and thus it's not very feasible to use bag-of-words as feature. A more is to use part-of-speech tagging. In order for the classifier to accept variable length input, and be able to classify based on the order of inputs

-- to be continued


## Action Detection


## Usage



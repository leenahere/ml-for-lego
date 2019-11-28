# ml-for-lego

This repository is part of my master's thesis. It contains all Python scripts for the LEGO MINDSTORMS EV3 that are necessary to perform the machine learning tasks I describe in my thesis.

It makes sense to solve these tasks with **µanthánō**, the visual programming environment, I built in the scope of my master thesis. The repository can be found [here](https://github.com/leenahere/manthano). In the following, I will only describe the workflow with **µanthánō**.

## Prerequisites

[ev3dev](https://www.ev3dev.org) has to be run on the EV3 to use these scripts.

Additionally, some python packages should be installed on the EV3. This can be done through ssh-ing onto the EV3 and pasting the following command:

```
sudo apt-get install python3-numpy python3-matplotlib python3-scipy python3-pandas python3-sklearn
```

Once you cloned the repository on your EV3, to run the scripts from the EV3 controls, you need to make the Python scripts you wish to use executable.

```
chmod +x ml-for-lego/record_scripts/record_digits.py
```

Currently the classifying scripts only send new data to the **µanthánō** server that performs the acutal classification task (mainly because it takes forever on the EV3). Therefore, you need to adjust the ip address in the `digit_classifier.py` and `shapes_classifier.py` to the ip address of the **µanthánō** server you probably run on your local machine. The ip address can be set in the constant `ENDPOINT_ADDRESS`.

## Digits and Shapes Classifier

This classifier task works as follows:

You need to tape the digits or shapes you wish to classify onto a light desk (tape should be dark). To collect training and test data, you need to use the `record_digits.py` or `record_shapes.py` script. Place the robot on the tape and follow the instructions on the screen. The data will automatically be saved to the *digits.csv* or *shapes.csv*.

When all the data is collected, you can connect the robot to **µanthánō**, preprocess the data and build a machine learning model. You can send the trained model to your EV3 and use `digit_classifier.py` or `shapes_classifier.py` to classify a digit or shape. Before running one of these scripts, you need to place your EV3 on the tape of the digit or shape that it is supposed to classify.

## Remote Control

This repository also includes remote control scripts to control the EV3. This could be used for future machine learning tasks on the EV3.

To use the remote control scripts, the script `client_web.py` has to be executed on a machine with a browser and a keyboard. On the same machine, the `index.html` has to be opened in a browser. On the EV3, the script `remote_drive.py` has to be executed. The EV3 can then be controlled with the `w`, `a`, `s` and `d` keys.

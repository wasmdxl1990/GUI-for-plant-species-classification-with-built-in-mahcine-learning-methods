#  GUI for plant species classification with built-in machine learning methods 

The objective of this project is to use machine learning algorithms to effciently classify 99 plant species by
using their binary leaf images including shape, margin & texture and pixel level information. This problem
also provides a valuable opportunity to directly implement programming tools to tackle unsolved engineering
problems. Furthermore, the methods this work is based on can be applied to various engineering domains
due to the applicability nature of machine learning.


<img src="./resultexamples/ab.png" width="400"> | <img src="./resultexamples/cd.png" width="400">

<img src="./resultexamples/GUI1.png" width="400"> | <img src="./resultexamples/GUI2.png" width="400">

# Contents
* Source code for GUI (/code)
* Raw leaf samples (/samples)
* GUI interface and preprocessing results (/resultexamples)


# Requirements
* Ubuntu / macOS / Windows
* Python3
* Scikit-Learn and PyQt5


# Usage
* clone this repository
> git clone https://github.com/wasmdxl1990/GUI-for-plant-species-classification-with-built-in-mahcine-learning-methods.git

* go to the code folder and setup the input path and output path

* run main script to run GUI of loading the image and predicting the species
> python GUI_addpic.py

* run main script to run GUI of taking the image with the webcam and predicting the species
> python GUI_ALLFeatures_Livedemo.py

* result has been saved in the output path

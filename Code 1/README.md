How to run our web site
=================
## Introduction
Our website is developed through many tools and library including HTML, Javascript, Arcgis Pro, Flask, and Python. Arcgis Pro comes with the user-friendly implementation on the map engine in our website which server as the primary function and platform for our development. Flask is a  web framework written in Python that helps us processed the data in Python and transport the analysis result into Javascript then into HTML format. Python is a simple programming language that equiped extensive libraries that helps us pre-process our data and do neccessary data retrival when requried.

## Step by Step guide line

### 1 Clone our repository or download our repository as zip file

### 2 Simply go into /Code/templates/ and clicks on main.html
It opens up our website where our data is visualized in the map. However, the data interpretion and calculation is no ready when you directly open up our website as the data is not ready in your folder.

### 3 If you wish to perform data analysis and calculation
Since GitHub limits the size of file we can upload into our repository. We are not able to store our data file in Git and thus, our data file is store at Google doc: https://drive.google.com/drive/folders/1mtH_evyiBC0kgZiA23ROwWvUPP2KmC6z?usp=sharing <br/>
Download **"Australia wind.tif"** and **"GHI.tif"**, save them into **/Code/data/**
However, if you are not interested in doing analysis on the data and only want to have a look at the color map, you can stop here. Notes that the initial loading and visualizing could take sometimes.

### 4 Start the website from Flask
Navigate your terminal into /Code/ and run the Python file **"start.py"**
If you are working in a Windows system.It is possible that you are missing some libarary to run the Python file. Here are some tips in installing some libararies.
**No module name "gdal"**: We found that installing of GDAL are often troublesome when using Pip install. Therefore, we advised to install using the wheel we provided in /Code/ folder named "GDAL-2.4.1-cp37-cp37m-win_amd64.whl", you can then run **"pip install GDAL-2.4.1-cp37-cp37m-win_amd64.whl"** in /Code/ folder if you are using Python version 3.7. Or if you are working on different python version, you should find yourself a installation package here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

### 5 Wait until the data is loaded and pre-processed
The data you downloaded will be processed in the python and then it will opens up the websites with the ability to do data analysis in the side bar.

### 6 Navigate to url http://localhost:5000/

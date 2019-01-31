# Fuzzy Car Simulator

[![Requirements Status](https://requires.io/github/seanwu1105/fuzzy-car/requirements.svg?branch=develop)](https://requires.io/github/seanwu1105/fuzzy-car/requirements/?branch=develop)

A sandbox practice for the fuzzy system.

![preview](https://i.imgur.com/C8xARC6.gif)

## Installation

Download this project

``` bash
git clone https://gitlab.com/seanwu1105/fuzzy-car.git
```

Change directory to the root of the project

``` bash
cd fuzzy-car/
```

Run with Python interpreter

``` bash
python3 main.py
```

## Add Customized Map Cases

### The data location

The data location is `/data`. The application will load every files with `*.txt` extension automatically after the execution.

### Example Format

``` python
0,0,90  # the starting position and angle of car (x, y, degree)
18,40   # the top-left coordinate of the ending area
30,37   # the bottom-right coordinate of the ending area
-6,-3   # the first point for the wall in map
-6,22
18,22
18,50
30,50
30,10
6,10
6,-6
-6,-3   # the last point for the wall in map
```

Every coordinates between the fourth and last line are the corner point of the walls in map.

## Save Data

### `train4D.txt`

``` python
# Front_Distance Right_Distance Left_Distance Wheel_Angle

22.0000000 8.4852814 8.4852814 -16.0709664
21.1292288 9.3920089 7.7989045 -14.7971418
20.3973643 24.4555821 7.2000902 16.2304876
19.1995799 25.0357595 7.5129743 16.0825385
18.1744869 42.5622911 8.0705896 15.5075777
```

### `train6D.txt`

``` python
# X Y Front_Distance Right_Distance Left_Distance Wheel_Angle

0.0000000 0.0000000 22.0000000 8.4852814 8.4852814 -16.0709664
0.0000000 0.9609196 21.1292288 9.3920089 7.7989045 -14.7971418
-0.0892157 1.9236307 20.3973643 24.4555821 7.2000902 16.2304876
-0.2588831 2.8686659 19.1995799 25.0357595 7.5129743 16.0825385
-0.3398267 3.8261141 18.1744869 42.5622911 8.0705896 15.5075777
-0.3319909 4.7896773 17.2922349 8.1967401 8.9258102 -14.6592172
```

## Dependencies

* [numpy](http://www.numpy.org/)

``` bash
pip3 install numpy
```

* [matplotlib](https://matplotlib.org/)

``` bash
pip3 install matplotlib
```

* [PySide2](http://wiki.qt.io/Qt_for_Python)

``` bash
pip3 install pyside2
```

## Further Details

https://is.gd/RmH2J3

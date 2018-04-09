# Fuzzy Car Simulator

A sandbox practice for the fuzzy system.

## Installation

1. Download this project

```
git clone https://gitlab.com/GLaDOS1105/fuzzy-car.git
```

2. Change directory to the root of the project

3. Running with Python interpreter

```
python3 main.py
```

## Add Customized Map Cases

### The data location

The data location is `/data`. The application will load every files with `*.txt` extension automatically after the execution.

### Example Format

```
0,0,90  // the starting position and angle of car (x, y, degree)
18,40   // the top-left coordinate of the ending area
30,37   // the bottom-right coordinate of the ending area
-6,-3   // the first point for the wall in map
-6,22
18,22
18,50
30,50
30,10
6,10
6,-6
-6,-3   // the last point for the wall in map
```

Every coordinates between the fourth and last line are the corner point of the walls in map.

## Third-Party Packages

* [numpy](http://www.numpy.org/)

```
pip3 install numpy
```

* [matplotlib](https://matplotlib.org/)

```
pip3 install matplotlib
```

* [PyQt5](https://riverbankcomputing.com/software/pyqt/intro)

```
pip3 install pyqt5
```

* [PyQtChart5](https://www.riverbankcomputing.com/software/pyqtchart/intro)

```
pip3 install PyQtChart
```
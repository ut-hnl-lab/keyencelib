【[日本語](https://github.com/ut-hnl-lab/keyencelib/blob/main/README-ja.md)】

# KeyenceLib
A tool to handle Keyence laser profiler in python.

## Description
Connect the LJ-V7000 series profiler, and you can easily do the following things with your python programs:
* Measurement data acquisition in the form of the numpy array
* CSV output of the data
* Real-time plotting of the data (Not yet implemented)

## Demo
▼Observation of the surface of an object made with an FDM 3D printer.

<img src="https://user-images.githubusercontent.com/88641432/163707718-4045fb65-121a-416b-b63c-976e642626b9.png" height="200">　<img src="https://user-images.githubusercontent.com/88641432/163707086-21b5b5b2-2675-40e4-a898-6b603c9ff8ef.gif" height="200">


## Usage
１. Connect the equipment as shown in the picture below.


<img src="https://user-images.githubusercontent.com/88641432/163779065-156cf1a9-42a7-44a9-acfc-4622e1b00dbe.png" width=600>

２. Execute your programs.

```python
import time
from keyencelib import Profiler

profiler = Profiler(savedir='tests')

# Get and save profiles as an array
with profiler.open():
    array = profiler.get()
    print(array)
```

## Installation
```
pip install git+https://github.com/ut-hnl-lab/keyencelib.git
```

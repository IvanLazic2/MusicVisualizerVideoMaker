# Music visualizer video maker
Make a video for a song or a track with custom visualizers based on loudness, frequency...

## Example video
https://youtu.be/I2Sk8WoMwIU

## Environment

Run to create an environment
```
pip install virtualenv
```
```
python -m virtualenv <environment-name>
```

Run to install packages
```
pip install -r requirements.txt
```

## How to make your own visualizer

### Step 1
Imports
```py
import gizeh as gz
import numpy as np
from PIL import Image, ImageDraw
from Visualizer import Visualizer
from Options import Options
```

### Step 2
Create a class for the visualizer in ./visualizers/ directory inheriting Visualizer class
```py
class MyCustomVisualizer(Visualizer)
{
  
}
```

### Step 3
Create a constructor with one mandatory parameter ```audioFile``` and your custom parameters, for example: ```x```, ```y```, ```color```, ```scale```...
```py
def __init__(self, audioFile, x, y, color, scalePercentage)
{
  super().__init__(audioFile)
  
  self.X = x
  self.Y = y
  self.Color = color
  self.Scale = int(scalePercentage * Options.HEIGHT)
}
```
Variable       | Description                                        | Type      | Required |
---------------|----------------------------------------------------|-----------|----------|
```audioFile```| Path to and audio file to use for video generation | ```str``` | Yes      |

### Step 4
Create a method ```Render``` with one mandatory parameter ```time``` and optional keyword arguments ```**kwargs``` </br>

```py
def Render(self, time, **kwargs)
{

}
```
Variable  | Description                       | Type        | Required |
----------|-----------------------------------|-------------|----------|
```time```| Represents passed time in seconds | ```float``` | Yes      |

### Step 5
Inside ```Render``` we will be creating a circle which radius changes based on music loudness, but you can create any shape or object as long as it has some parameters that can change based on loudness or frequency

## Existing visualizers:

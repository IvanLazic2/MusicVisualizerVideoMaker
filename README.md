# Music visualizer video maker
Make a video for a track with custom visualizers based on loudness and frequency

## Example video
https://youtu.be/I2Sk8WoMwIU

## Environment

Run to create environment
```
pip install virtualenv
```
```
python -m virtualenv <environment-name>
```
Run to activate environment
```
environment\Scripts\activate
```
> To deactivate run: ```environment\Scripts\deactivate.bat```

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
Create a class for the visualizer in ./visualizers/ directory inheriting ```Visualizer``` class
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
Variable       | Description                                       | Type      | Required |
---------------|---------------------------------------------------|-----------|----------|
```audioFile```| Path to an audio file to use for video generation | ```str``` | Yes      |

### Step 4
Create a method ```Render``` with one mandatory parameter ```time``` and optional keyword arguments ```**kwargs```

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

Here we are using gizeh library for vector graphics
> **Note** \
> PIL usually produces higher quality frames but gizeh is faster to render

```py
radius = self.Loudness[self.GetMoment(time)] * self.Scale

surface = gz.Surface(Options.WIDTH, Options.HEIGHT)
circle = gz.circle(radius, xy=(self.X, self.Y), fill=tuple(x / 255 for x in self.Color))
circle.draw(surface)
return surface.get_npimage(transparent=True)
```

Example with PIL
```py
radius = self.Loudness[self.GetMoment(time)] * self.Scale

image = Image.new("RGBA", (Options.WIDTH, Options.HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)
draw.ellipse((self.X - radius, self.Y - radius, self.X + radius, self.Y + radius), fill=self.Color)
return np.asarray(image)
```
> 1. ```Loudness``` is a numpy array which contains music loudness data. Its length is number of frames
> 2. ```GetMoment(time)``` returns current frame number

### Step 6
Here we will create a visualizer - a white circle in the middle of the screen that responds to music
```py
from Video import Video
from visualizers.MyCustomVisualizer import MyCustomVisualizer
from Options import Options  

if __name__ == "__main__":
  audioFile = "audio/audio.wav"
  video = Video(audioFile, output="video.mp4")
  
  myCustomVisualizer = MyCustomVisualizer(audioFile,
                                          x=Options.WIDTH / 2
                                          y=Options.HEIGHT / 2
                                          color=(255, 255, 255)
                                          scalePercentage=0.9
                                          )
  
  circle = video.ShowTransparent(myCustomVisualizer.Render)
  
  video.Generate([circle])
```

> ```Video``` object takes the path to the audio file and output name \
> ```Video.ShowTransparent``` takes a render method and optional keyword arguments, and makes background transparent \
> ```Video.Generate``` takes a list of objects to render

The result is saved in a file named ```output```

## Existing visualizers:

import gizeh as gz
import numpy as np
from PIL import Image, ImageDraw
from Visualizer import Visualizer
from Options import Options

#SCALE = 300
#MIN_RADIUS = 10
#MAX_RADIUS = 250
#MIN_PEAK = 1.5
#PEAK_INTERVAL = (1, 2)
#DIFFERENCE_LIMIT = 3
#DROPOFF_SPEED = 3
#TARGET_FREQ = 30

class CircleVisualizer(Visualizer):
    def __init__(self, 
                 audioFile, 
                 x = Options.WIDTH / 2, 
                 y = Options.HEIGHT / 2, 
                 color = (255, 0, 0), 
                 scalePercentage = 0.74, 
                 minRadiusPercentage = 0.02, 
                 maxRadiusPercentage = 0.61, 
                 differenceLimit = 3, 
                 dropoffSpeed = 3
                 ):

        super().__init__(audioFile)

        self.LoudnessConvolved = self.CreateLoudnessConvolved(kernelSize=10)

        self.radiusPrev = 0


        self.X = x
        self.Y = y
        self.Color = color
        self.Scale = int(scalePercentage * Options.HEIGHT)
        self.MinRadius = int(minRadiusPercentage * Options.HEIGHT)
        self.MaxRadius = int(maxRadiusPercentage * Options.HEIGHT)
        self.DifferenceLimit = differenceLimit
        self.DropoffSpeed = dropoffSpeed

        

    def Render(self, time, **kwargs):
        radius = 0
        result = None

        if kwargs.get("reactiveRadius"):
            radius = self.renderReactiveRadius(time)

        if kwargs.get("useGizeh"):
            surface = gz.Surface(Options.WIDTH, Options.HEIGHT)
            circle = gz.circle(radius, xy=(self.X, self.Y), fill=tuple(x / 255 for x in self.Color))
            circle.draw(surface)
            result = surface.get_npimage(transparent=True)
        else:
            image = Image.new("RGBA", (Options.WIDTH, Options.HEIGHT), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.ellipse((self.X - radius, self.Y - radius, self.X + radius, self.Y + radius), fill=self.Color)
            result = np.asarray(image)

        return result

    def renderReactiveRadius(self, time):
        radius = self.LoudnessConvolved[self.GetMoment(time)] * self.Scale

        if radius < self.MinRadius:
           radius = self.MinRadius
        elif radius > self.MaxRadius:
            radius = self.MaxRadius

        if radius < self.radiusPrev:
            if abs(radius - self.radiusPrev) > self.DifferenceLimit:
                radius = self.radiusPrev - self.DropoffSpeed

        self.radiusPrev = radius

        return radius

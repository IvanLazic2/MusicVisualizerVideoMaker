import math
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from Visualizer import Visualizer
from Options import Options

class BackgroundImageVisualizer(Visualizer):
    def __init__(self, 
                 audioFile, 
                 imageFile, 
                 scale = 5,
                 zoomPercentage = 0.17,
                 rotationAngleScale = 10, 
                 rotationSpeed = 1,
                 widthSwayPercentage = 0.13,
                 heightSwayPercentage = 0.05,
                 widthSwaySpeed = 1,
                 heightSwaySpeed = 2,
                 minBrightness = 0.5,
                 blurScale = 9):

        super().__init__(audioFile)

        self.kernelSize = 50
        self.kernel = np.ones(self.kernelSize) / self.kernelSize
        self.loudnessConvolved = np.convolve(self.Loudness, self.kernel)

        self.Scale = scale
        self.Zoom = int(Options.HEIGHT * zoomPercentage)
        self.RotationAngleScale = rotationAngleScale
        self.RotationSpeed = rotationSpeed
        self.WidthSwayLength = int(Options.WIDTH * widthSwayPercentage)
        self.HeightSwayLength = int(Options.HEIGHT * heightSwayPercentage)
        self.WidthSwaySpeed = widthSwaySpeed
        self.HeightSwaySpeed = heightSwaySpeed
        self.MinBrightness = minBrightness
        self.BlurScale = blurScale


        self.CurrentLoudness = 0

        self.Image = Image.open(imageFile)
        self.Image = self.Image.resize((Options.WIDTH, Options.HEIGHT), Image.ANTIALIAS)
        self.Enhancer = ImageEnhance.Brightness(self.Image)

        self.Ratio = self.Image.width / self.Image.height


    def Render(self, time, **kwargs):
        self.CurrentLoudness = self.loudnessConvolved[self.GetMoment(time)]

        if kwargs.get("reactiveBrightness"):
            self.Image = self.renderReactiveBrightness(time)

        if kwargs.get("reactiveBlur"):
            self.Image = self.renderReactiveBlur(time)

        if kwargs.get("reactiveRotation"):
            self.Image = self.renderReactiveRotation(time)

        if kwargs.get("progressiveRotation"):
            self.Image = self.renderProgressiveRotation(time)

        if kwargs.get("progressiveSway"):
            self.Image = self.renderProgressiveSway(time)

        return np.asarray(self.Image.resize((Options.WIDTH, Options.HEIGHT)))

    def renderReactiveBrightness(self, time):
        
        factor = self.CurrentLoudness * self.Scale

        if factor < self.MinBrightness:
            factor = self.MinBrightness

        return self.Enhancer.enhance(factor)

    def renderReactiveBlur(self, time):
        return self.Image.filter(ImageFilter.GaussianBlur(radius=self.CurrentLoudness*self.BlurScale))

    def renderReactiveRotation(self, time):
        return self.Image.rotate(self.CurrentLoudness * 20)

    ####################### TODO #####################
    def renderReactiveZoom(self, time):
        pass
    ##################################################

    def renderProgressiveRotation(self, time):
        return self.Image.rotate(math.sin(self.RotationSpeed * time) * self.RotationAngleScale, resample=Image.BICUBIC)

    def renderProgressiveSway(self, time):
        widthPosition = (Options.WIDTH / 2) + math.sin(self.WidthSwaySpeed * time) * self.WidthSwayLength
        heightPosition = (Options.HEIGHT / 2) + math.sin(self.HeightSwaySpeed * time) * self.HeightSwayLength

        left = widthPosition - (Options.WIDTH / 2) + (self.Zoom * self.Ratio)
        top = heightPosition - (Options.HEIGHT / 2) + self.Zoom
        right = widthPosition + (Options.WIDTH / 2) - (self.Zoom * self.Ratio)
        bottom = heightPosition + (Options.HEIGHT / 2) - self.Zoom

        return self.Image.crop((left, top, right, bottom))
    
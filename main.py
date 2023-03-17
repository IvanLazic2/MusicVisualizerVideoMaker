#import gizeh as gz
#import moviepy.editor as mpy

from Video import Video
from visualizers.CircleVisualizer import CircleVisualizer
from visualizers.BackgroundImageVisualizer import BackgroundImageVisualizer
from Options import Options        

if __name__ == "__main__":
    audioFile = "audio/audio.wav"

    video = Video(audioFile)

    #backgroundImage = video.RenderStillBackgroundImage("images/image.jpg")
    backgroundImageVisualizer = BackgroundImageVisualizer(audioFile, 
                                                          "images/image2.jpg", 
                                                          scale=5,
                                                          zoomPercentage=0.17,
                                                          rotationAngleScale=10,
                                                          rotationSpeed=1,
                                                          widthSwayPercentage=0.13,
                                                          heightSwayPercentage=0.05,
                                                          widthSwaySpeed=1,
                                                          heightSwaySpeed=2,
                                                          minBrightness=0.5,
                                                          blurScale=7
                                                          )

    backgroundImage = video.Show(backgroundImageVisualizer.Render,
                                 reactiveBrightness=True,
                                 reactiveBlur=True,
                                 progressiveRotation=True,
                                 progressiveSway=True
                                 )

    #textTitle = video.ShowTransparent(video.RenderText, text="Title bla", surfaceW=722, surfaceH=404, xy=(320, 40), fill=(0, 0, 1), fontsize=50, fontweight="bold", fontfamily="Tahoma")
    #textAuthor = video.ShowTransparent(video.RenderText, text="Author bla bla", surfaceW=722, surfaceH=404, xy=(320, 80), fill=(0, 0, 1), fontsize=25, fontweight="normal", fontfamily="Tahoma")

    circleVisualizer = CircleVisualizer(audioFile,
                                        x=Options.WIDTH / 2,
                                        y=Options.HEIGHT / 2,
                                        color=(255, 255, 255),
                                        scalePercentage=0.9, 
                                        minRadiusPercentage=0.02, 
                                        maxRadiusPercentage=0.7, 
                                        differenceLimit=3, 
                                        dropoffSpeed=2
                                        )

    circleVisualizer2 = CircleVisualizer(audioFile,
                                        x=Options.WIDTH / 4,
                                        y=Options.HEIGHT / 4,
                                        color=(255, 255, 255),
                                        scalePercentage=0.5,
                                        minRadiusPercentage=0.02, 
                                        maxRadiusPercentage=0.7, 
                                        differenceLimit=3, 
                                        dropoffSpeed=2
                                        )

    circleVisualizer3 = CircleVisualizer(audioFile,
                                        x=3 * Options.WIDTH / 4,
                                        y=3 * Options.HEIGHT / 4,
                                        color=(255, 255, 255),
                                        scalePercentage=0.5,
                                        minRadiusPercentage=0.02, 
                                        maxRadiusPercentage=0.7, 
                                        differenceLimit=3, 
                                        dropoffSpeed=2
                                        )


    circle = video.ShowTransparent(circleVisualizer.Render,
                                   reactiveRadius=True,
                                   useGizeh=False
                                   )

    circle2 = video.ShowTransparent(circleVisualizer2.Render,
                                    reactiveRadius=True,
                                    useGizeh=False
                                    )

    circle3 = video.ShowTransparent(circleVisualizer3.Render,
                                    reactiveRadius=True,
                                    useGizeh=False
                                    )

    video.Generate([backgroundImage, circle, circle2, circle3])

class Options:
    # AUDIO SETTINGS
    SAMPLE_RATE = 44100       # 22050 prije
    N_FFT = 4096              # 2048*4 prije, 2650
    HOP_LENGTH = 256          # 512 prije
    AUDIO_SILENCE = -80

    # VIDEO SETTINGS
    WIDTH = 722 // 4 # 722
    HEIGHT = 404 // 4 # 405 404
    FPS = 60

    # COLORS
    BLUE = (59/255, 89/255, 152/255)
    GREEN = (176/255, 210/255, 63/255)
    WHITE = (255, 255, 255)
    WHITE_GIZEH = (1, 1, 1)
import sys 
import pygame
# WARNING: continue

def main():
    pygame.mixer.init()
    pygame.mixer.music.load("/Users/gorsenkovegor/Downloads/mp3/Nirvana.mp3")

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)



if __name__ == "__main__":
    sys.exit(main())

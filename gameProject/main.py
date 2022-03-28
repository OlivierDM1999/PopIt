import random
from cvzone.HandTrackingModule import HandDetector
import pygame
import numpy as np
import cv2
import time


# Initialization
pygame.init()

# Create window and display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pop It !")

# Clock initialization for fps
fps = 30
clock = pygame.time.Clock()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Width
cap.set(4, 720) # Height

# Load images
imgBalloon = pygame.image.load("../PopIt/Resources/Balloon1.png").convert_alpha()
imgBalloon = pygame.transform.scale(imgBalloon, (154, 168))
hitbox = imgBalloon.get_rect()
hitbox.x, hitbox.y = 500, 500


def resetBalloon():
    hitbox.x = random.randint(100, img.shape[1] - 100)
    hitbox.y = img.shape[0]+50


# Detector
# Définit la certitude à min 80% pour considérer qu'on a bien une main
# Nombre de mains peut être augmenté sans souci
detector = HandDetector(detectionCon=0.8, maxHands=1)


# Loop !
start = True
speed = 15
score = 0
startTime = time.time()
gameTime = 30

while start:
    # Get event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Logic application

    # OpenCV
    success, img = cap.read() # OpenCV uses BGR but pygame uses RGB so we need a conversion
    img = cv2.flip(img, 1) # on peut flip en passant (img, 1) dans la direction horizontale (0 pour verticale)
    hands, img = detector.findHands(img, flipType=False)

    hitbox.y -= speed
    if hitbox.y < -10:
        resetBalloon()
        speed += 1

    if hands: # In the list of hands
        hand = hands[0] # Take the first hand
        # We take the point at the tip of the index :
        x, y= hand['lmList'][8][0], hand['lmList'][8][1]
        #print(x, ' ', y)
        #print(hitbox.collidepoint(x, y))
        # Then we check if (x,y) is inside the baloon :
        if hitbox.collidepoint(x, y):
            #print(" ================== TOUCHE ================== ")
            score += 10
            resetBalloon()

    timeRemain = int(gameTime - (time.time() - startTime))
    if timeRemain <= 0 :
        window.fill((255, 255, 255))

        font = pygame.font.Font('../PopIt//Resources/Secret Admirer.ttf', 50)
        textScore = font.render(f'Your score: {score}', True, (255, 50, 50))
        textTime = font.render(f'Time is up !', True, (255, 50, 50))
        window.blit(textScore, (500, 350))
        window.blit(textTime, (500, 275))

    else :
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()  # convert makes it easier for pygame to process the display
        frame = pygame.transform.flip(frame, True, False)

        window.blit(frame, (0, 0))
        #pygame.draw.rect(window, (0, 255, 0), hitbox) # Affiche la hitbox en vert
        window.blit(imgBalloon, hitbox)

        font = pygame.font.Font('../PopIt//Resources/Secret Admirer.ttf', 50)
        textScore = font.render(f'Score: {score}', True, (255, 50, 50))
        textTime = font.render(f'Time: {timeRemain}', True, (255, 50, 50))
        window.blit(textScore, (35, 35))
        window.blit(textTime, (1000, 35))

    # Update display
    pygame.display.update()
    # Set fps
    clock.tick(fps)

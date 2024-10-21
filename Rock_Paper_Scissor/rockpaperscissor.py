# Importing libraries
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time 
import random
import pygame

# Initialize Pygame for sound
pygame.mixer.init()

# Load sound files and handle errors
try:
    pygame.mixer.music.load('d:/CODE/Proj/Game Development/Rock_Paper_Scissor/Resources/music.mp3')  # Background music
    win_sound = pygame.mixer.Sound('d:/CODE/Proj/Game Development/Rock_Paper_Scissor/Resources/score_sound.wav')  # Sound when player wins
    lose_sound = pygame.mixer.Sound('d:/CODE/Proj/Game Development/Rock_Paper_Scissor/Resources/hit_sound.wav')  # Sound when AI wins
     
except pygame.error as e:
    print(f"Error loading sound: {e}")

# Play background music in a loop
pygame.mixer.music.play(-1)

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    pygame.mixer.music.stop()  # Stop background music if webcam fails to open
    exit()

cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]

while True:
    # Load background image and handle error
    try:
        imgBG = cv2.imread('D:/CODE/Proj/Game Development/Rock_Paper_Scissor/Resources/BG.png')
        if imgBG is None:
            raise FileNotFoundError("Background image not found!")
    except FileNotFoundError as e:
        print(e)
        break

    success, img = cap.read()
    if not success:
        print("Error: Failed to capture image from webcam.")
        break

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # Rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # Paper
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # Scissors

                     

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'D:/CODE/Proj/Game Development/Rock_Paper_Scissor/Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Player wins
                    if (playerMove == 1 and randomNumber == 3) or (playerMove == 2 and randomNumber == 1) or (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
                        win_sound.play()  # Play win sound effect

                    # AI wins
                    elif (playerMove == 3 and randomNumber == 1) or (playerMove == 1 and randomNumber == 2) or (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
                        lose_sound.play()  # Play lose sound effect

    imgBG[234:654, 795:1195] = imgScaled

    # Only overlay imgAI if it's been generated
    if stateResult and 'imgAI' in locals():
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # Display scores
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()  # Reset timer when game starts
        stateResult = False

    if key == ord('q'):  # Graceful exit
        break

# Stop background music and release resources
pygame.mixer.music.stop()
cap.release()
cv2.destroyAllWindows()



     

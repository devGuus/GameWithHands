import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

Hand = mphands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)
hands = mphands.Hands()

last_x = 0
last_y = 0

speed = 0

while True:
    data, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    handsPoints = results.multi_hand_landmarks
    height, width, _ = image.shape
    score = []

    if handsPoints:
        for points in handsPoints:
            mp_drawing.draw_landmarks(image, points, mphands.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                cordx, cordy = int(cord.x*width), int(cord.y*height)
                score.append((cordx, cordy))

                if id == 8: # indicador 
                    if last_x is not None and last_y is not None:
                        dist = ((cordx - last_x) ** 2 + (cordy - last_y) ** 2) ** 0.5
                        speed = 20 * dist
                        
                if points.landmark[4].y < points.landmark[3].y and points.landmark[4].y < points.landmark[2].y and points.landmark[4].y < points.landmark[1].y and points.landmark[4].y < points.landmark[0].y:
                    # polegar estendido
                    distanc = ((points.landmark[4].x - points.landmark[8].x) ** 2 + (points.landmark[4].y - points.landmark[8].y) ** 2) ** 0.5
                    if distanc < 0.05:
                        # clicar
                        pyautogui.click()                        

        screenWidth, screenHeight = pyautogui.size()
        pyautogui.moveTo(screenWidth - cordx, screenHeight - cordy)
        last_x, last_y = cordx, cordy

        # fingers = [8, 12, 16, 20] #selecionando ponta dos 4 dedos
        # fingersJamp = [8, 4]
        
        # cont = 0
        # if points:
        #     if score[4][0] < score[2][0]: # verificando polegar
        #         cont +=1  
        #     for i in fingers:
        #         if score[i][1] < score[i - 2][1]: # verificando se o dedo está fechado 'score[x][y]'
        #             cont+=1
                    
        #     if score[8][1] < score[4][0]:
        #         print('jump')
        # print(cont) 

    cv2.imshow('Handtracker', image)
    cv2.waitKey(1)
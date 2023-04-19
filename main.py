import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

Hand = mphands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)
hands = mphands.Hands()

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
            print(points)
            mp_drawing.draw_landmarks(image, points, mphands.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                cordx, cordy = int(cord.x*width), int(cord.y*height)
               #cv2.putText(image, str(id), (cordx, cordy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                score.append((cordx, cordy))

        fingers = [8, 12, 16, 20]


    cv2.imshow('Handtracker', image)
    cv2.waitKey(1)

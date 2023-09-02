import cv2
import mediapipe as mp  
import random

cap = cv2.VideoCapture(0)  # Obtain camera to capture the live

# This is a drawing module; it will detect the hand part and draw in cv2
mp_drawing = mp.solutions.drawing_utils

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6)
gesture = ["None", "scissor","rock","paper"]
user = 0
sys = 0
flag = 0 #last round gesture
sys_ges = 'None'

while True:
    if user != 0 and flag != user:
        sys = random.randint(1, 3)
        sys_ges = gesture[sys]
    if user == 0:
        sys = 0
    flag = user
    # `ret` represents whether the frame was read successfully,
    # and `frame` obtains the picture from the camera
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

    # Convert the frame to the BGR format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            p0_x = hand_landmarks.landmark[0].x
            p0_y = hand_landmarks.landmark[0].y

            p5_x = hand_landmarks.landmark[5].x
            p5_y = hand_landmarks.landmark[5].y
            distance_0_5 = ((p0_x - p5_x)**2 + (p0_y - p5_y)**2)**0.5
            base = distance_0_5/0.8

            p8_x = hand_landmarks.landmark[8].x
            p8_y = hand_landmarks.landmark[8].y
            distance_0_8 = ((p0_x - p8_x)**2 + (p0_y - p8_y)**2)**0.5

            p12_x = hand_landmarks.landmark[12].x
            p12_y = hand_landmarks.landmark[12].y
            distance_0_12 = ((p0_x - p12_x)**2 + (p0_y - p12_y)**2)**0.5

            p16_x = hand_landmarks.landmark[16].x
            p16_y = hand_landmarks.landmark[16].y
            distance_0_16 = ((p0_x - p16_x)**2 + (p0_y - p16_y)**2)**0.5

            p20_x = hand_landmarks.landmark[20].x
            p20_y = hand_landmarks.landmark[20].y
            distance_0_20 = ((p0_x - p20_x)**2 + (p0_y - p20_y)**2)**0.5
            
            # scissor
        if distance_0_8>base and distance_0_12>base:
            user = 1
            # paper
        if distance_0_8>base and distance_0_12>base and distance_0_16>base and distance_0_20>base:
            user = 3
            # rock
        if distance_0_8<base and distance_0_12<base and distance_0_16<base and distance_0_20<base:
            user = 2

        cv2.putText(frame, "you: "+gesture[user],(50,20),0,1,(0,0,225),2)
        cv2.putText(frame, "Computer: "+sys_ges,(50,50),0,1,(0,0,225),2)
        if sys == user:
            cv2.putText(frame, "Draw",(50,70),0,1,(0,0,225),2)
        elif user+1 == sys or user-2 == sys:
            cv2.putText(frame, "you lose",(50,70),0,1,(0,0,225),2)
        else:
            cv2.putText(frame, "you win",(50,70),0,1,(0,0,225),2)
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Build a window UI frame and display the content stored in the `frame` variable
    cv2.imshow('MediaPipe Hands', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
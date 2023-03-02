import cv2
import numpy as np
import mediapipe as mp

def point_in_box(p, x, y, w, h):
    if (x<p[0] and p[0]<x+w) and (y<p[1] and p[1]<y+h):
        return True
    else:
        return False

def fingers_in_box(finger_list, x, y, w, h):
    cont = 0
    for i in range(len(finger_list)):
        if point_in_box(finger_list[i], x, y, w, h) == True:
            cont =  cont+1
    
    if cont == len(finger_list):
        return True
    else:
        return False

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

alpha_up = 0.5
alpha_left = 0.5
alpha_right = 0.5

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 2,
    min_detection_confidence = 0.5) as hands:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)


        #cv2.line(frame, (0, int(height/2)), (width, int(height/2)), (255,0,0), 5)
        #cv2.line(frame, (int(width/3), 0), (int(width/3), height), (255,0,0), 5)
        #cv2.line(frame, (int(2*width/3), 0), (int(2*width/3), height), (255,0,0), 5)

        margin = 10

        x_up, y_up, w_up, h_up = int(width/3)+margin, margin, int(width/3)-2*margin, int(height/2)-2*margin
        sub_frame = frame[y_up:y_up+h_up, x_up:x_up+w_up]
        white_rect = np.ones(sub_frame.shape, dtype=np.uint8) * 255
        frame[y_up:y_up+h_up, x_up:x_up+w_up] = cv2.addWeighted(sub_frame, alpha_up, white_rect, 1-alpha_up, 1.0)

        x_left, y_left, w_left, h_left = margin, int(height/2)+margin, int(width/3)-2*margin, int(height/2)-2*margin
        sub_frame = frame[y_left:y_left+h_left, x_left:x_left+w_left]
        white_rect = np.ones(sub_frame.shape, dtype=np.uint8) * 255
        frame[y_left:y_left+h_left, x_left:x_left+w_left] = cv2.addWeighted(sub_frame, alpha_left, white_rect, 1-alpha_left, 1.0)

        x_right, y_right, w_right, h_right = int(2*width/3)+margin, int(height/2)+margin, int(width/3)-2*margin, int(height/2)-2*margin
        sub_frame = frame[y_right:y_right+h_right, x_right:x_right+w_right]
        white_rect = np.ones(sub_frame.shape, dtype=np.uint8) * 255
        frame[y_right:y_right+h_right, x_right:x_right+w_right] = cv2.addWeighted(sub_frame, alpha_right, white_rect, 1-alpha_right, 1.0)

        if results.multi_hand_landmarks is not None:
            
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255,255,0), thickness=4, circle_radius=5),
                    mp_drawing.DrawingSpec(color=(255,0,255), thickness=4))
                

                x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * width)
                y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * height)

                x2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                y2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)

                x3 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * width)
                y3 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * height)

                x4 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * width)
                y4 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * height)

                x5 = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * width)
                y5 = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * height)

                if fingers_in_box([[x1,y1], [x2,y2], [x3,y3], [x4,y4], [x5,y5]], x_up, y_up, w_up, h_up) == True:
                    alpha_up = 0.2
                else:
                    alpha_up = 0.5

                if fingers_in_box([[x1,y1], [x2,y2], [x3,y3], [x4,y4], [x5,y5]], x_left, y_left, w_left, h_left) == True:
                    alpha_left = 0.2
                else:
                    alpha_left = 0.5
                
                if fingers_in_box([[x1,y1], [x2,y2], [x3,y3], [x4,y4], [x5,y5]], x_right, y_right, w_right, h_right) == True:
                    alpha_right = 0.2
                else:
                    alpha_right = 0.5
                
                #for (i, points) in enumerate(hand_landmarks.landmark):
                #    if i in index:
                #        x = int(points.x * width)
                #        y = int(points.y * height)
                #        cv2.circle(frame, (x, y), 10, (255, 255, 0), -1)

                        
                """
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255,255,0), thickness=4, circle_radius=5),
                    mp_drawing.DrawingSpec(color=(255,0,255), thickness=4))
                """
                """
                x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * width)
                y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * height)

                x2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                y2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)

                x3 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * width)
                y3 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * height)

                x4 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * width)
                y4 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * height)

                x5 = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * width)
                y5 = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * height)

                cv2.circle(frame, (x1, y1), 3, (255, 255, 0), 3)
                cv2.circle(frame, (x2, y2), 3, (255, 255, 0), 3)
                cv2.circle(frame, (x3, y3), 3, (255, 255, 0), 3)
                cv2.circle(frame, (x4, y4), 3, (255, 255, 0), 3)
                cv2.circle(frame, (x5, y5), 3, (255, 255, 0), 3)
                """
        cv2.imshow("XDDD", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
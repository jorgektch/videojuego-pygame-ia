import cv2
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Capturadora de video streaming
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5) as face_mesh:

    while True:
        # Lectura de video
        ret, frame = cap.read()
        if ret == True:
            # Imagen espejo
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            # BGR a RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Obteniendo resultados de la deteccion
            results = face_mesh.process(frame_rgb)

            # Dibujado marcas
            if results.multi_face_landmarks is not None:
                for face_landmarks in results.multi_face_landmarks:
                    """
                    mp_drawing.draw_landmarks(frame, face_landmarks,
                        mp_face_mesh.FACEMESH_CONTOURS, #FACE_CONNECTIONS
                        mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                        mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))
                    """
                    """
                    mp_drawing.draw_landmarks(frame, face_landmarks)
                    """
                    x_sup = int(face_landmarks.landmark[10].x * width)
                    y_sup = int(face_landmarks.landmark[10].y * height)
                    
                    x_inf = int(face_landmarks.landmark[152].x * width)
                    y_inf = int(face_landmarks.landmark[152].y * height)

                    x_mean_vertical = int((x_sup + x_inf)/2)
                    y_mean_vertical = int((y_sup + y_inf)/2)

                    x_left = int(face_landmarks.landmark[234].x * width)
                    y_left = int(face_landmarks.landmark[234].y * height)

                    x_right = int(face_landmarks.landmark[454].x * width)
                    y_right = int(face_landmarks.landmark[454].y * height)

                    cv2.line(frame, (x_sup, y_sup), (x_inf, y_inf), (255,0,0), 5)

                    cv2.circle(frame, (x_sup, y_sup), 10, (255,0,255), -1)
                    cv2.circle(frame, (x_inf, y_inf), 10, (255,0,255), -1)
                    cv2.circle(frame, (x_mean_vertical, y_mean_vertical), 10, (255,0,255), -1)
                    cv2.circle(frame, (x_left, y_left), 10, (255,0,255), -1)
                    cv2.circle(frame, (x_right, y_right), 10, (255,0,255), -1)

                    cv2.line(frame, (x_left, y_left), (x_right, y_right), (255,0,0), 5)

                    radians = -math.atan2(y_sup-y_inf,x_sup-x_inf)
                    degrees = math.degrees(radians)
                    degrees = round(degrees)
                    
                    dist_vertical = math.dist([x_sup, y_sup], [x_inf, y_inf])
                    dist_horizontal = math.dist([x_right, y_right], [x_left, y_left])
                    ratio = dist_vertical/dist_horizontal
                    ratio = round(ratio, 2)

                    dx = None
                    if degrees < 85:
                        dx = 1
                    elif degrees > 95:
                        dx = -1
                    else:
                        dx = 0

                    y_mean_horizontal = (y_right + y_left)/2


                    dy = None
                    if y_mean_vertical < y_mean_horizontal:
                        dy = -1
                    else:
                        dy = 0

                    cv2.putText(frame, "dx: "+str(dx), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(frame, "dy: "+str(dy), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    #print(degrees)

                    """
                    x = int(face_landmarks.landmark[130].x * width)
                    y = int(face_landmarks.landmark[130].y * height)
                    cv2.circle(frame, (x, y), 5, (255,0,255), 2)
                    print(x, y)

                    x = int(face_landmarks.landmark[359].x * width)
                    y = int(face_landmarks.landmark[359].y * height)
                    cv2.circle(frame, (x, y), 5, (255,0,255), 2)
                    print(x, y)
                    """

            # 
            cv2.imshow("Probando face mesh", frame)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        else:
            break

cap.release()
cv2.destroyAllWindows()

"""
python -m venv env
.\env\Scripts\activate
pip install mediapipe
pip install opencv_python
pip install pygame
pip freeze > requirements.txt
pip install -r requirements.txt
"""
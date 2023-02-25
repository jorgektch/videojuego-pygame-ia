import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Capturadora de video streaming
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

with mp_face_detection.FaceDetection(
    min_detection_confidence=0.5) as face_detection:

    while True:
        # Lectura de video
        ret, frame = cap.read()
        if ret == True:
            # Imagen espejo
            frame = cv2.flip(frame, 1)
            # BGR a RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Obteniendo resultados de la deteccion
            results = face_detection.process(frame_rgb)

            # Dibujado de rectangulo
            if results.detections is not None:
                for detection in results.detections:
                    mp_drawing.draw_detection(frame, detection,
                        mp_drawing.DrawingSpec(color=(0, 255, 255), circle_radius=5),
                        mp_drawing.DrawingSpec(color=(255, 0, 255), circle_radius=5))

            cv2.imshow("Probando face detection", frame)

            # Tecla de scape
            k = cv2.waitKey(1) % 0xFF
            if k == 27:
                break
        else:
            break

cap.release()
cv2.destroyAllWindows()

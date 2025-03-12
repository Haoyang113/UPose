import cv2
import mediapipe as mp
from clientUDP import ClientUDP
import global_vars 
import time

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
timeSincePostStatistics = 0

client = ClientUDP(global_vars.HOST,global_vars.PORT)
client.start()

cap = cv2.VideoCapture(0)  # Open webcam

with mp_pose.Pose(min_detection_confidence=0.80, min_tracking_confidence=0.5, model_complexity = global_vars.MODEL_COMPLEXITY,static_image_mode = False,enable_segmentation = True) as pose: 
    while cap.isOpened():
        ti = time.time()
        success, image = cap.read()
        if not success:
            break

        image = cv2.flip(image, 1)
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        tf = time.time()

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:

            if time.time()-timeSincePostStatistics>=1:
                print("Theoretical Maximum FPS: %f"%(1/(tf-ti)))
                timeSincePostStatistics = time.time()

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                mp_drawing.DrawingSpec(color=(255, 100, 0), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
            )

        cv2.imshow('MediaPipe Face Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

        data = ""
        i = 0
        if results.pose_world_landmarks:
            world_landmarks = results.pose_world_landmarks
            for i in range(0,33):
                data += "{}|{}|{}|{}|{}\n".format(i,world_landmarks.landmark[i].x,world_landmarks.landmark[i].y,world_landmarks.landmark[i].z,world_landmarks.landmark[i].visibility)

            client.sendMessage(data)

cap.release()
cv2.destroyAllWindows()

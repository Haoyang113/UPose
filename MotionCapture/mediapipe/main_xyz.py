import cv2
import mediapipe as mp
from clientUDP import ClientUDP
import global_vars 
import time
from upose import UPose

pose_tracker = UPose("mediapipe")
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
            #Calculate rotations
            pose_tracker.newFrame(results)
            pelvis_rotation = pose_tracker.getPelvisRotation()
            torso_rotation = pose_tracker.getTorsoRotation()
            left_shoulder_rotation = pose_tracker.getLeftShoulderRotation()
            right_shoulder_rotation = pose_tracker.getRightShoulderRotation()
            left_elbow_rotation = pose_tracker.getLeftElbowRotation()
            right_elbow_rotation = pose_tracker.getRightElbowRotation()
            left_hip_rotation = pose_tracker.getLeftHipRotation()
            right_hip_rotation = pose_tracker.getRightHipRotation()
            left_knee_rotation = pose_tracker.getLeftKneeRotation()
            right_knee_rotation = pose_tracker.getRightKneeRotation()

            #Print Euler angles
            #print("Pelvis rotation: %f %f %f" % (pelvis_rotation["euler"][0],pelvis_rotation["euler"][1],pelvis_rotation["euler"][2]))
            #print("Torso rotation: %f %f %f" % (torso_rotation["euler"][0],torso_rotation["euler"][1],torso_rotation["euler"][2]))
            #print("Left Shoulder rotation: %f %f %f" % (left_shoulder_rotation["euler"][0],left_shoulder_rotation["euler"][1],left_shoulder_rotation["euler"][2]))
            #print("Right Shoulder rotation: %f %f %f" % (right_shoulder_rotation["euler"][0],right_shoulder_rotation["euler"][1],right_shoulder_rotation["euler"][2]))
            #print("Left Elbow rotation: %f %f %f" % (left_elbow_rotation["euler"][0],left_elbow_rotation["euler"][1],left_elbow_rotation["euler"][2]))
            #print("Right Elbow rotation: %f %f %f" % (right_elbow_rotation["euler"][0],right_elbow_rotation["euler"][1],right_elbow_rotation["euler"][2]))
            #print("Left Hip rotation: %f %f %f" % (left_hip_rotation["euler"][0],left_hip_rotation["euler"][1],left_hip_rotation["euler"][2]))
            #print("Right Hip rotation: %f %f %f" % (right_hip_rotation["euler"][0],right_hip_rotation["euler"][1],right_hip_rotation["euler"][2]))
            #print("Left Knee rotation: %f %f %f" % (left_knee_rotation["euler"][0],left_knee_rotation["euler"][1],left_knee_rotation["euler"][2]))
            #print("Right Knee rotation: %f %f %f" % (right_knee_rotation["euler"][0],right_knee_rotation["euler"][1],right_knee_rotation["euler"][2]))


            world_landmarks = results.pose_world_landmarks
            for i in range(0,33):
                data += "{}|{}|{}|{}|{}\n".format(i,world_landmarks.landmark[i].x,world_landmarks.landmark[i].y,world_landmarks.landmark[i].z,world_landmarks.landmark[i].visibility)

            client.sendMessage(data)

cap.release()
cv2.destroyAllWindows()

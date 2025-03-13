import cv2
from mmpose.apis import MMPoseInferencer
from clientUDP import ClientUDP
import global_vars 
import time


timeSincePostStatistics = 0

client = ClientUDP(global_vars.HOST,global_vars.PORT)
client.start()

cap = cv2.VideoCapture(0)  # Open webcam

inferencer = MMPoseInferencer(pose3d='human3d', device='mps') 

while cap.isOpened():
        ti = time.time()
        success, image = cap.read()
        if not success:
            break

        image = cv2.flip(image, 1)
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result_generator = inferencer(image)
        result = next(result_generator, None)
        tf = time.time()

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if result is not None:

            predictions = result['predictions'][0][0]

            if time.time()-timeSincePostStatistics>=1:
                print("Theoretical Maximum FPS: %f"%(1/(tf-ti)))
                timeSincePostStatistics = time.time()

            #mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
            #    mp_drawing.DrawingSpec(color=(255, 100, 0), thickness=2, circle_radius=4),
            #    mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
            #)

        cv2.imshow('MediaPipe Face Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
   
        if result is not None:           
            predictions = result['predictions'][0][0]
            data = ""
            i = 0
            if 'keypoints' in predictions:
                for i, keypoint in enumerate(predictions['keypoints']): 
                    data += "{}|{}|{}|{}|{}\n".format(i, keypoint[0], keypoint[1], keypoint[2],predictions['keypoint_scores'][i])  
                client.sendMessage(data)  
cap.release()
cv2.destroyAllWindows()

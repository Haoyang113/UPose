import numpy as np
import math
import mediapipe as mp
from scipy.spatial.transform import Rotation as R

class UPose:
    def __init__(self, source="mediapipe"):
        if source.lower() != "mediapipe":
            raise ValueError("Only 'mediapipe' source is supported currently.")
        self.source = source
        self.world_landmarks = None
        self.mp_pose = mp.solutions.pose
        self.resetFrame()

    def resetFrame(self):
        self.pelvis_rotation = None
        self.torso_rotation = None
        self.left_shoulder_rotation = None
        self.right_shoulder_rotation = None
        self.left_elbow_rotation = None
        self.right_elbow_rotation = None
        self.left_hip_rotation = None
        self.right_hip_rotation = None
        self.left_knee_rotation = None
        self.right_knee_rotation = None

    def newFrame(self, results):
        """Feed a new MediaPipe results object."""
        self.resetFrame()
        if results.pose_world_landmarks:
            self.world_landmarks = results.pose_world_landmarks
        else:
            self.world_landmarks = None

    def getPelvisRotation(self):
        """Returns signed Y-axis pelvis rotation in degrees, or None if unavailable."""

        if self.pelvis_rotation is not None:
            return self.pelvis_rotation
    
        if not self.world_landmarks:
            return None

        LM = self.mp_pose.PoseLandmark
        p1 = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_HIP.value])
        p2 = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_HIP.value])

        direction = p2 - p1
        direction = direction / np.linalg.norm(direction)

        direction_xz = np.array([direction[0], 0, direction[2]])
        direction_xz = direction_xz / np.linalg.norm(direction_xz)

        angle_rad = math.atan2(direction_xz[2], direction_xz[0])
        angle_deg = math.degrees(angle_rad)

        euler = np.array([0, -angle_deg, 0])
        local = R.from_euler('zxy',[0, 0, -angle_deg],degrees=True)

        self.pelvis_rotation = {
            "world": local,
            "local": local,
            "euler": euler
        }

        return self.pelvis_rotation

    def getTorsoRotation(self):

        if self.torso_rotation is not None:
            return self.torso_rotation
        
        if not self.world_landmarks:
            return None

        # Get landmarks
        LM = self.mp_pose.PoseLandmark
        left_hip = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_HIP.value])
        right_hip = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_HIP.value])
        left_shoulder = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_SHOULDER.value])
        right_shoulder = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_SHOULDER.value])

        # Compute midpoints
        pelvis = (left_hip + right_hip) / 2
        shoulder_center = (left_shoulder + right_shoulder) / 2

        # Direction vector from pelvis to shoulders
        direction = shoulder_center - pelvis
        direction = direction / np.linalg.norm(direction)

        # Get pelvis rotation in degrees
        pelvis_rot = self.getPelvisRotation()
        if pelvis_rot is None:
            return None
        
        base_rotation = pelvis_rot["world"]

        # Inverse rotate direction vector into local space
        local_direction = base_rotation.inv().apply(direction)

        # Compute angles
        rot_z = math.asin(-local_direction[0]) * 180.0 / math.pi
        rot_x = math.atan2(local_direction[2], local_direction[1]) * 180.0 / math.pi

        euler = np.array([rot_x, 0, rot_z])
        local = R.from_euler('zxy',[rot_z, rot_x, 0], degrees=True)

        self.torso_rotation = {
            "world": base_rotation * local,
            "local": local,
            "euler": euler
        }

        return self.torso_rotation

    def getLeftShoulderRotation(self):
   
        if self.left_shoulder_rotation is not None:
            return self.left_shoulder_rotation
        
        if not self.world_landmarks:
            return None

        # Get landmarks
        LM = self.mp_pose.PoseLandmark
        left_shoulder = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_SHOULDER.value])
        left_elbow = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_ELBOW.value])

        direction = left_elbow - left_shoulder
        direction = direction / np.linalg.norm(direction)

        # Get pelvis rotation in degrees
        torso_rot = self.getTorsoRotation()
        if torso_rot is None:
            return None
        
        base_rotation = torso_rot["world"]

        local_direction = base_rotation.inv().apply(direction)

        rot_z = -math.asin(local_direction[1]) * 180.0 / math.pi + 90
        rot_y = math.atan2(local_direction[2], -local_direction[0]) * 180.0 / math.pi
        
        if rot_z < -180:
            rot_z += 360

        euler = np.array([0, rot_y, rot_z])
        local = R.from_euler('zxy', [rot_z, 0, rot_y], degrees=True)

        self.left_shoulder_rotation = {
            "euler": euler,
            "local": local,
            "world": base_rotation*local
        }

        return self.left_shoulder_rotation

    def getRightShoulderRotation(self):
   
        if self.right_shoulder_rotation is not None:
            return self.right_shoulder_rotation
        
        if not self.world_landmarks:
            return None

        # Get landmarks
        LM = self.mp_pose.PoseLandmark
        right_shoulder = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_SHOULDER.value])
        right_elbow = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_ELBOW.value])

        direction = right_elbow - right_shoulder
        direction = direction / np.linalg.norm(direction)

        # Get pelvis rotation in degrees
        torso_rot = self.getTorsoRotation()
        if torso_rot is None:
            return None
        
        base_rotation = torso_rot["world"]

        local_direction = base_rotation.inv().apply(direction)

        rot_z = math.asin(local_direction[1]) * 180.0 / math.pi - 90
        rot_y = -math.atan2(local_direction[2], local_direction[0]) * 180.0 / math.pi

        if rot_z < -180:
            rot_z += 360

        euler = np.array([0, rot_y, rot_z])
        local = R.from_euler('zxy', [rot_z, 0, rot_y], degrees=True)

        self.right_shoulder_rotation = {
            "euler": euler,
            "local": local,
            "world": base_rotation*local
        }

        return self.right_shoulder_rotation

    def getLeftElbowRotation(self):
        
        if self.left_elbow_rotation is not None:
            return self.left_elbow_rotation
        
        if not self.world_landmarks:
            return None

        LM = self.mp_pose.PoseLandmark
        elbow = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_ELBOW.value])
        wrist = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_WRIST.value])
        shoulder_rot = self.getLeftShoulderRotation()
       

        if shoulder_rot is None:
            return None

        direction = wrist - elbow
        direction = direction / np.linalg.norm(direction)

        base_rotation = shoulder_rot["world"]
        local_direction = base_rotation.inv().apply(direction)

        rot_z = math.asin(-local_direction[0]) * 180.0 / math.pi
        rot_x = math.atan2(local_direction[2], local_direction[1]) * 180.0 / math.pi

        euler = np.array([rot_x, 0, rot_z])
        local = R.from_euler('zxy', [rot_z, rot_x, 0], degrees=True)

        self.left_elbow_rotation= {
            "euler": euler,
            "local": local,
            "world": base_rotation * local
        }

        return self.left_elbow_rotation

    def getRightElbowRotation(self):
        
        if self.right_elbow_rotation is not None:
            return self.right_elbow_rotation
        
        if not self.world_landmarks:
            return None

        LM = self.mp_pose.PoseLandmark
        elbow = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_ELBOW.value])
        wrist = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_WRIST.value])
        shoulder_rot = self.getRightShoulderRotation()

        if shoulder_rot is None:
            return None

        direction = wrist - elbow
        direction = direction / np.linalg.norm(direction)

        base_rotation = shoulder_rot["world"]
        local_direction = base_rotation.inv().apply(direction)

        rot_z = math.asin(-local_direction[0]) * 180.0 / math.pi
        rot_x = math.atan2(local_direction[2], local_direction[1]) * 180.0 / math.pi

        euler = np.array([rot_x, 0, rot_z])
        local = R.from_euler('zxy', [rot_z, rot_x, 0], degrees=True)

        self.right_elbow_rotation= {
            "euler": euler,
            "local": local,
            "world": base_rotation * local
        }

        return self.right_elbow_rotation

    def getLeftHipRotation(self):
        if self.left_hip_rotation is not None:
            return self.left_hip_rotation

        if not self.world_landmarks:
            return None

        LM = self.mp_pose.PoseLandmark
        left_hip = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_HIP.value])
        left_knee = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_KNEE.value])

        direction = left_knee - left_hip
        direction = direction / np.linalg.norm(direction)

        pelvis_rot = self.getPelvisRotation()
        if pelvis_rot is None:
            return None

        base_rotation = pelvis_rot["world"]
        local_direction = base_rotation.inv().apply(direction)

        rot_z = math.asin(local_direction[0]) * 180.0 / math.pi
        rot_x = math.atan2(-local_direction[2], -local_direction[1]) * 180.0 / math.pi

        if rot_x == -180:
            rot_x = 0

        euler = np.array([rot_x, 0, rot_z + 180])
        local = R.from_euler('zxy', [rot_z + 180, rot_x, 0], degrees=True)

        self.left_hip_rotation = {
            "euler": euler,
            "local": local,
            "world": base_rotation * local
        }

        return self.left_hip_rotation

    def getRightHipRotation(self):
        if self.right_hip_rotation is not None:
            return self.right_hip_rotation

        if not self.world_landmarks:
            return None

        LM = self.mp_pose.PoseLandmark
        right_hip = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_HIP.value])
        right_knee = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_KNEE.value])

        direction = right_knee - right_hip
        direction = direction / np.linalg.norm(direction)

        pelvis_rot = self.getPelvisRotation()
        if pelvis_rot is None:
            return None

        base_rotation = pelvis_rot["world"]
        local_direction = base_rotation.inv().apply(direction)

        rot_z = math.asin(local_direction[0]) * 180.0 / math.pi
        rot_x = math.atan2(-local_direction[2], -local_direction[1]) * 180.0 / math.pi

        if rot_x == -180:
            rot_x = 0

        euler = np.array([rot_x, 0, rot_z + 180])
        local = R.from_euler('zxy', [rot_z + 180, rot_x, 0], degrees=True)

        self.right_hip_rotation = {
            "euler": euler,
            "local": local,
            "world": base_rotation * local
        }

        return self.right_hip_rotation

    def getLeftKneeRotation(self):
        if self.left_knee_rotation is not None:
            return self.left_knee_rotation

        if not self.world_landmarks:
            return None

        LM = self.mp_pose.PoseLandmark
        left_knee = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_KNEE.value])
        left_ankle = self._landmark_to_np(self.world_landmarks.landmark[LM.LEFT_ANKLE.value])

        direction = left_ankle - left_knee
        direction = direction / np.linalg.norm(direction)

        thigh_rot = self.getLeftHipRotation()
        if thigh_rot is None:
            return None

        base_rotation = thigh_rot["world"]
        local_direction = base_rotation.inv().apply(direction)

        rot_z = math.asin(-local_direction[0]) * 180.0 / math.pi
        rot_x = math.atan2(local_direction[2], local_direction[1]) * 180.0 / math.pi

        euler = np.array([rot_x, 0, rot_z])
        local = R.from_euler('zxy', [rot_z, rot_x, 0], degrees=True)

        self.left_knee_rotation = {
            "euler": euler,
            "local": local,
            "world": base_rotation * local
        }

        return self.left_knee_rotation

    def getRightKneeRotation(self):
        if self.right_knee_rotation is not None:
            return self.right_knee_rotation

        if not self.world_landmarks:
            return None

        LM = self.mp_pose.PoseLandmark
        right_knee = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_KNEE.value])
        right_ankle = self._landmark_to_np(self.world_landmarks.landmark[LM.RIGHT_ANKLE.value])

        direction = right_ankle - right_knee
        direction = direction / np.linalg.norm(direction)

        thigh_rot = self.getRightHipRotation()
        if thigh_rot is None:
            return None

        base_rotation = thigh_rot["world"]
        local_direction = base_rotation.inv().apply(direction)

        rot_z = math.asin(-local_direction[0]) * 180.0 / math.pi
        rot_x = math.atan2(local_direction[2], local_direction[1]) * 180.0 / math.pi

        euler = np.array([rot_x, 0, rot_z])
        local = R.from_euler('zxy', [rot_z, rot_x, 0], degrees=True)

        self.right_knee_rotation = {
            "euler": euler,
            "local": local,
            "world": base_rotation * local
        }

        return self.right_knee_rotation


    def _landmark_to_np(self, landmark):
        return np.array([landmark.x, -landmark.y, -landmark.z])

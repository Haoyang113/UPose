# pose_utils.py
# 职责：存放所有与姿态计算、角度计算、动作分类相关的纯函数。

import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """计算由三个点 a, b, c 构成的角度，角度的顶点是 b。"""
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def compute_joint_angles(landmarks):
    """计算所有需要的关节角度"""
    angles = {}
    try:
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        angles['left_knee'] = calculate_angle(left_hip, left_knee, left_ankle)
        angles['right_knee'] = calculate_angle(right_hip, right_knee, right_ankle)
        angles['left_hip'] = calculate_angle(left_shoulder, left_hip, left_knee)
        angles['right_hip'] = calculate_angle(right_shoulder, right_hip, right_knee)
        angles['left_elbow'] = calculate_angle(left_shoulder, left_elbow, left_wrist)
        angles['right_elbow'] = calculate_angle(right_shoulder, right_elbow, right_wrist)
    except:
        pass
    return angles

def compute_joint_velocities(last_angles, current_angles, dt):
    """计算关节角速度"""
    velocities = {}
    if last_angles and current_angles and dt > 0.001:
        for angle_name, current_value in current_angles.items():
            if angle_name in last_angles:
                velocity = (current_value - last_angles.get(angle_name, current_value)) / dt
                velocities['d_' + angle_name] = velocity
    return velocities

def classify_action(landmarks, angles):
    """根据关节点和角度信息，进行简单的动作分类"""
    is_left_hand_up = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y < landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
    is_right_hand_up = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y < landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
    if is_left_hand_up and is_right_hand_up: hand_pose = "双手举起"
    elif is_left_hand_up: hand_pose = "左手举起"
    elif is_right_hand_up: hand_pose = "右手举起"
    else: hand_pose = "双手自然放下"
    avg_knee_angle = (angles.get('left_knee', 180) + angles.get('right_knee', 180)) / 2
    avg_hip_angle = (angles.get('left_hip', 180) + angles.get('right_hip', 180)) / 2
    if avg_knee_angle < 120 and avg_hip_angle < 140: body_pose = "蹲下"
    elif avg_knee_angle < 150 and avg_hip_angle < 150: body_pose = "坐下"
    elif avg_knee_angle > 160 and avg_hip_angle > 160: body_pose = "站立"
    else: body_pose = "过渡姿态"
    return f"{hand_pose} {body_pose}"
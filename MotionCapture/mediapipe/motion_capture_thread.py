# motion_capture_thread.py
# 职责：定义后台工作线程，负责所有耗时的摄像头和MediaPipe操作。

import cv2
import mediapipe as mp
import numpy as np
import time
from PyQt5.QtCore import QThread, pyqtSignal

# 从其他模块导入
from clientUDP import ClientUDP
from upose import UPose
from pose_utils import compute_joint_angles, compute_joint_velocities, classify_action

mp_pose = mp.solutions.pose


class MotionCaptureThread(QThread):
    # 定义信号，用于向主线程发送数据
    frame_updated = pyqtSignal(np.ndarray)
    status_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._is_running = True
        self.is_recording = False
        self.is_paused = False
        self.recorded_data = []

    def run(self):
        # 初始化所有对象
        pose_tracker = UPose(source="mediapipe", flipped=False)
        mp_drawing = mp.solutions.drawing_utils
        client = ClientUDP('127.0.0.1', 52733)
        client.start()
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            self.status_updated.emit("致命错误: 无法打开摄像头。")
            return

        last_angles = None
        last_time = time.time()

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self._is_running and cap.isOpened():
                success, image = cap.read()
                if not success:
                    self.status_updated.emit("错误: 摄像头画面读取失败。")
                    break

                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image_rgb)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    current_time = time.time()

                    angles = compute_joint_angles(landmarks)
                    dt = current_time - last_time
                    velocities = compute_joint_velocities(last_angles, angles, dt)
                    pose_label = classify_action(landmarks, angles)

                    if not self.is_paused:
                        last_time = current_time
                        last_angles = angles

                    if self.is_recording and not self.is_paused:
                        log_entry = {'timestamp': current_time, 'pose': pose_label}
                        log_entry.update(angles)
                        log_entry.update(velocities)
                        self.recorded_data.append(log_entry)

                    # (保持不变) 发送旋转数据到 Unity
                    data_to_unity = "mprot\n"
                    if results.pose_world_landmarks:
                        pose_tracker.newFrame(results)
                        pose_tracker.computeRotations()
                        # (此处省略了所有get rotation和拼接data_to_unity字符串的代码, 保持和您原来的一致)
                        pelvis_rotation = pose_tracker.getPelvisRotation()["local"].as_quat()
                        pelvis_visibility = pose_tracker.getPelvisRotation()["visibility"]
                        torso_rotation = pose_tracker.getTorsoRotation()["local"].as_quat()
                        torso_visibility = pose_tracker.getTorsoRotation()["visibility"]
                        left_shoulder_rotation = pose_tracker.getLeftShoulderRotation()["local"].as_quat()
                        left_shoulder_visibility = pose_tracker.getLeftShoulderRotation()["visibility"]
                        right_shoulder_rotation = pose_tracker.getRightShoulderRotation()["local"].as_quat()
                        right_shoulder_visibility = pose_tracker.getRightShoulderRotation()["visibility"]
                        left_elbow_rotation = pose_tracker.getLeftElbowRotation()["local"].as_quat()
                        left_elbow_visibility = pose_tracker.getLeftElbowRotation()["visibility"]
                        right_elbow_rotation = pose_tracker.getRightElbowRotation()["local"].as_quat()
                        right_elbow_visibility = pose_tracker.getRightElbowRotation()["visibility"]
                        left_hip_rotation = pose_tracker.getLeftHipRotation()["local"].as_quat()
                        left_hip_visibility = pose_tracker.getLeftHipRotation()["visibility"]
                        right_hip_rotation = pose_tracker.getRightHipRotation()["local"].as_quat()
                        right_hip_visibility = pose_tracker.getRightHipRotation()["visibility"]
                        left_knee_rotation = pose_tracker.getLeftKneeRotation()["local"].as_quat()
                        left_knee_visibility = pose_tracker.getLeftKneeRotation()["visibility"]
                        right_knee_rotation = pose_tracker.getRightKneeRotation()["local"].as_quat()
                        right_knee_visibility = pose_tracker.getRightKneeRotation()["visibility"]
                        data_to_unity += "{}|{}|{}|{}|{}|{}\n".format(0, pelvis_rotation[0], pelvis_rotation[1],
                                                                      pelvis_rotation[2], pelvis_rotation[3],
                                                                      pelvis_visibility)
                        data_to_unity += "{}|{}|{}|{}|{}|{}\n".format(1, torso_rotation[0], torso_rotation[1],
                                                                      torso_rotation[2], torso_rotation[3],
                                                                      torso_visibility)
                        data_to_unity += "{}|{}|{}|{}|{}|{}\n".format(2, left_shoulder_rotation[0],
                                                                      left_shoulder_rotation[1],
                                                                      left_shoulder_rotation[2],
                                                                      left_shoulder_rotation[3],
                                                                      left_shoulder_visibility)
                        data_to_unity += "{}|{}|{}|{}|{}|{}\n".format(3, right_shoulder_rotation[0],
                                                                      right_shoulder_rotation[1],
                                                                      right_shoulder_rotation[2],
                                                                      right_shoulder_rotation[3],
                                                                      right_shoulder_visibility)
                        data_to_unity += "{}|{}|{}|{}|{}|{}\n".format(4, left_elbow_rotation[0], left_elbow_rotation[1],
                                                                      left_elbow_rotation[2], left_elbow_rotation[3],
                                                                      left_elbow_visibility)
                        data_to_unity += "{}|{}|{}|{}|{}|{}\n".format(5, right_elbow_rotation[0],
                                                                      right_elbow_rotation[1], right_elbow_rotation[2],
                                                                      right_elbow_rotation[3], right_elbow_visibility)
                        data_to_unity += "{}|{}|{}|{}|{}|{}\n".format(6, left_hip_rotation[0], left_hip_rotation[1],
                                                                      left_hip_rotation[2], left_hip_rotation[3],
                                                                      left_hip_visibility)
                        data_to_unity += "{}|{}|{}|{}|{}|{}\n".format(7, right_hip_rotation[0], right_hip_rotation[1],
                                                                      right_hip_rotation[2], right_hip_rotation[3],
                                                                      right_hip_visibility)
                        data_to_unity += "{}|{}|{}|{}|{}|{}\n".format(8, left_knee_rotation[0], left_knee_rotation[1],
                                                                      left_knee_rotation[2], left_knee_rotation[3],
                                                                      left_knee_visibility)
                        data_to_unity += "{}|{}|{}|{}|{}|{}\n".format(9, right_knee_rotation[0], right_knee_rotation[1],
                                                                      right_knee_rotation[2], right_knee_rotation[3],
                                                                      right_knee_visibility)
                        client.sendMessage(data_to_unity)

                    mp_drawing.draw_landmarks(image_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    self.status_updated.emit(f"当前动作: {pose_label}")

                # 发射信号，将处理后的图像发送给主线程
                self.frame_updated.emit(image_rgb)

                time.sleep(0.01)  # 稍微让出CPU

        cap.release()
        client.disconnect()
        self.status_updated.emit("线程已结束。")

    def stop(self):
        self._is_running = False

    def toggle_record(self):
        if not self.is_recording:
            self.is_recording = True
            self.is_paused = False
            self.recorded_data.clear()
            print("--- 🔴 开始录制 ---")

    def toggle_pause(self):
        if self.is_recording:
            self.is_paused = not self.is_paused
            if self.is_paused:
                print("--- ⏸️ 录制已暂停 ---")
            else:
                print("--- ▶️ 录制已继续 ---")
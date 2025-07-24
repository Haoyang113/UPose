# main_gui.py
# 职责：创建和管理图形用户界面（GUI），响应用户交互，并启动整个应用。

import sys
import csv
import time
from datetime import datetime
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

# 从其他模块导入
from motion_capture_thread import MotionCaptureThread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UPose 可视化动捕与记录系统")
        self.setGeometry(100, 100, 1200, 800)

        # UI组件
        self.video_label = QLabel("正在启动摄像头...", self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black; color: white;")

        self.info_box = QTextEdit(self)
        self.info_box.setReadOnly(True)
        self.info_box.setMaximumHeight(100)

        self.start_button = QPushButton("开始录制")
        self.pause_button = QPushButton("暂停/继续")
        self.stop_button = QPushButton("停止并保存")

        # 布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_label, 1)  # 视频占主要空间
        main_layout.addWidget(self.info_box)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # 创建并启动工作线程
        self.worker = MotionCaptureThread()
        self.worker.frame_updated.connect(self.update_image)
        self.worker.status_updated.connect(self.update_status)
        self.worker.start()

        # 连接按钮点击事件
        self.start_button.clicked.connect(self.start_recording)
        self.pause_button.clicked.connect(self.pause_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        self.update_button_states()

    def update_image(self, cv_img):
        """更新视频画面"""
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        qt_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def update_status(self, message):
        """更新状态信息文本框"""
        self.info_box.setText(message)

    def update_button_states(self):
        """根据当前状态更新按钮的可用性"""
        recording = self.worker.is_recording
        self.start_button.setEnabled(not recording)
        self.pause_button.setEnabled(recording)
        self.stop_button.setEnabled(recording)

    def start_recording(self):
        self.worker.toggle_record()
        self.info_box.append("🔴 开始录制... (可按“暂停/继续”)")
        self.update_button_states()

    def pause_recording(self):
        self.worker.toggle_pause()
        status = "⏸️ 录制已暂停" if self.worker.is_paused else "▶️ 录制已继续"
        self.info_box.append(status)

    def stop_recording(self):
        if not self.worker.is_recording:
            return

        self.worker.is_recording = False  # 强制停止
        self.save_data_dialog(self.worker.recorded_data)
        self.update_button_states()

    def save_data_dialog(self, data):
        """弹出'另存为'对话框并保存数据"""
        if not data:
            self.info_box.append("⚠️ 没有可保存的数据。")
            return

        root = tk.Tk()
        root.withdraw()

        filepath = filedialog.asksaveasfilename(
            initialfile=f"pose_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filepath:
            self.info_box.append("⚠️ 保存已取消。")
            return

        self.info_box.append(f"正在保存数据到 {filepath} ...")
        QApplication.processEvents()  # 刷新UI

        headers = set()
        for row in data:
            headers.update(row.keys())

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=sorted(list(headers)))
                writer.writeheader()
                writer.writerows(data)
            self.info_box.append(f"✅ 数据成功保存到: {filepath}")
        except Exception as e:
            self.info_box.append(f"❌ 保存失败: {e}")

    def closeEvent(self, event):
        """关闭窗口时确保后台线程也一并关闭"""
        self.info_box.append("正在关闭线程，请稍候...")
        self.worker.stop()
        self.worker.wait()  # 等待线程完全结束
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
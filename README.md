# Vision-Based Tracking System
2축 카메라 기반 실시간 비행체 추적 시스템
(YOLO Object Detection + Kalman Filter Motion Tracking)

## Overview
이 시스템은 2축 카메라를 이용한 비행체 추적 시스템으로, YOLO를 활용한 객체 감지와 Kalman 필터를 이용한 모션 추적을 결합하여 실시간으로 비행체를 3D 공간에서 추적합니다.

## Project Structure
```
vision_based_tracking_system/
│
├── detector/
│   ├── yolo_detector.py
│   └── ...
│
├── tracker/
│   ├── kalman_filter.py
│   └── ...
│
├── controller/
│   ├── motor_controller.py
│   └── ...
│
├── utils/
│   └── camera_utils.py
│
├── main.py
└── README.md
```

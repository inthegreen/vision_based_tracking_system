# Vision-Based Tracking System
2축 카메라 기반 실시간 비행체 추적 시스템
(YOLO Object Detection + Kalman Filter Motion Tracking)

## Overview
이 시스템은 2축 카메라를 이용한 비행체 추적 시스템으로, YOLO를 활용한 객체 감지와 Kalman 필터를 이용한 모션 추적을 결합하여 실시간으로 비행체를 3D 공간에서 추적합니다.

## Features

## System Architecture
```
                   +-------------------+
                   |      Camera       |
                   | (Real-time Input) |
                   +---------+---------+
                             |
                             v
                   +-------------------+
                   |  YOLO Detection   |
                   +---------+---------+
                             |
                             v
                   +-------------------+
                   |  Tracking Module  |
                   | (Kalman fallback) |
                   +---------+---------+
                             |
                             v
                   +-------------------+
                   |  Trajectory /     |
                   | Angle Estimation  |
                   +---------+---------+
                             |
                             v
                   +-------------------+
                   |  Motor Command    |
                   +---------+---------+
                             |
                             v
                   +-------------------+
                   |     Arduino       |
                   |  Stepper Control  |
                   +---------+---------+
                             |
                             v
                   +-------------------+
                   |  Stepper Motors   |
                   +-------------------+

```
## Demo / Example Output

## Project Structure
```
project_root/
├─ models/                        # YOLO 학습 weight(.pt), calibration data
│   └─ yolov8_custom.pt
│
├─ data/                          # 샘플 영상/이미지, 테스트용 데이터
│   ├─ samples/
│   └─ test_videos/
│
├─ vision_based_tracking_system/
│   ├─ camera/
│   │   ├─ 🔧 Camera.py              # 카메라 캡처 클래스
│   │   ├─ 🔧 MotorControl.py       # x, y 계산
│   │   └─ __init__.py
│   │
│   ├─ trajectory/
│   │   ├─ 🔧 Trajectory_Prediction.py # 비행체 위치 예측
│   │   ├─ 🔧 kalman_filter.py       # Kalman Filter 모듈
│   │   └─ __init__.py
│   │
│   ├─ utils/
│   │   ├─ stepper_comm.py        # Serial 통신 (PC → Arduino)
│   │   └─ __init__.py
│   │
│   ├─ __init__.py
│   └─ main.py                    # 전체 파이프라인 실행 엔트리포인트
│
├─ DualAxisStepper/
│   ├─ DualAxisStepper.ino        # 아두이노 2축 스텝모터 제어
│   └─ README.md                  # 펌웨어 관련 설명
│
├─ requirements.txt
├─ README.md
└─ run.py                         # 실행 스크립트 (python run.py)
```

## How It Works
### 1. Detection
### 2. Tracking (Kalman + KCF + CSRT)
### 3. Trajectory Calculation
### 4. Motor Control Pipeline

## Installation

## Usage

## Configuration Files
config.yaml 설명

## Hardware Setup

## Serial Communication Protocol
(선택)

## Future Work

## License

## Contact

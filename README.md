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
                   | (Kalman + KCF/    |
                   |   CSRT fallback)  |
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
├─ config/                        # config YAML 파일들
│   ├─ camera.yaml
│   ├─ tracking.yaml
│   ├─ motor.yaml
│   └─ system.yaml
│
├─ vision_based_tracking_system/
│   ├─ camera/
│   │   ├─ Camera.py              # 카메라 캡처 클래스
│   │   ├─ camera_utils.py        # 카메라 관련 도우미 함수
│   │   └─ __init__.py
│   │
│   ├─ detection/
│   │   ├─ yolo_detector.py       # YOLO 추론 래퍼
│   │   ├─ preprocessor.py        # 전처리
│   │   └─ __init__.py
│   │
│   ├─ trajectory/
│   │   ├─ Trajectory_Prediction.py # 비행체 위치 예측
│   │   ├─ kalman_filter.py       # Kalman Filter 모듈
│   │   └─ __init__.py
│   │
│   ├─ communication/
│   │   ├─ stepper_comm.py        # Serial 통신 (PC → Arduino)
│   │   └─ protocol.py            # 커스텀 통신 프로토콜 정의
│   │   └─ __init__.py
│   │
│   ├─ utils/
│   │   ├─ math_utils.py          # 좌표계 변환, 각도 계산
│   │   ├─ draw_utils.py          # bbox, crosshair 그리기
│   │   ├─ io_utils.py            # 파일/로그 입출력
│   │   ├─ timer.py               # FPS 측정
│   │   └─ __init__.py
│   │
│   ├─ __init__.py
│   └─ main.py                    # 전체 파이프라인 실행 엔트리포인트
│
├─ DualAxisStepper/
│   ├─ DualAxisStepper.ino        # 아두이노 2축 스텝모터 제어
│   └─ README.md                  # 펌웨어 관련 설명
│
├─ docs/                          # 문서 (아키텍처 다이어그램, 개념 정리 등)
│   ├─ architecture_diagram.png
│   ├─ tracking_algorithm_notes.md
│   └─ hardware_setup.md
│
├─ tests/                         # 유닛 테스트 및 통합 테스트
│   ├─ test_detector.py
│   ├─ test_tracker.py
│   ├─ test_comm.py
│   └─ README.md
│
├─ scripts/                       # 개발 편의 스크립트
│   ├─ export_video.py
│   ├─ calibration_tool.py
│   └─ dataset_viewer.py
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

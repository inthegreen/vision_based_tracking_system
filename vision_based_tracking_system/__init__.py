"""
vision_based_tracking_system: 2축 카메라를 이용한 비행체 추적 시스템

이 패키지는 YOLO(You Only Look Once) 기반 객체 감지와 Kalman Filter를 이용한 
모션 추적 알고리즘을 결합하여 비행체 추적을 수행합니다. 주로 드론 또는 로켓과 같은 
공중 물체의 실시간 추적에 사용하고자 합니다. 이 패키지는 추적 시스템을 설정하고, 
추적 결과를 시각화하는 데 필요한 핵심 기능들을 제공하고자 합니다.

주요 개발 목표:
    - 실시간 비디오 소스 처리
    - YOLO를 이용한 객체 감지
    - Kalman Filter를 이용한 비행체 궤도 예측 및 보정
    - 카메라 제어
"""

# Trajectory_Prediction 모듈을 불러옵니다.
from .Trajectory_Prediction import *

# camera_control 내부의 camera_control.py 모듈만 불러옵니다.
from .camera_control import camera_control

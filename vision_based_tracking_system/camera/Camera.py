from ultralytics import YOLO
import time
import cv2
import torch

class Camera:
    def __init__(self, stream_url, model="yolo11n.pt", confidence_threshold=0.3):
        self.model = YOLO(model)
        self.cap = cv2.VideoCapture(stream_url)
        self.conf_thresh = confidence_threshold
        self.prior_size = None

    def detection(self):
        results = self.model("/content/street.jpg", conf=self.conf_thresh)[0]
        boxes = results.boxes.xyxy
        confs = results.boxes.conf
        h, w = results.orig_shape
        image_size = w * h

        if boxes.shape[0] == 0:
            return None  # 탐지 없음

        # 좌표 분리
        x1, y1, x2, y2 = boxes.T

        # 크기 계산
        width  = x2 - x1
        height = y2 - y1
        sizes  = width * height

        # 이미지 중심과 거리 계산
        cx, cy = w / 2, h / 2
        dx = (x1 + x2) / 2 - cx
        dy = (y1 + y2) / 2 - cy
        distance = torch.hypot(dx, dy)

        # 이미지의 반대각선 절반 (거리 정규화용)
        half_diagonal = (w**2 + h**2)**0.5 / 2
        
        if self.prior_size is not None:
            # 기존 prior 기반 평균 score
            size_ratio = torch.abs(1 - (sizes / self.prior_size))
            distance_ratio = distance / half_diagonal
            score = size_ratio + distance_ratio
        else:
            # prior 없을 때: size + 중심 거리 기반 score
            size_score = 1 - (sizes / image_size)
            distance_ratio = distance / half_diagonal
            score = size_score + distance_ratio

        # score가 가장 낮은 객체 선택
        best_idx = score.argmin()

        # prior 크기 업데이트
        self.prior_size = sizes[best_idx]

        # 선택된 박스 좌표와 confidence 반환
        return boxes[best_idx], confs[best_idx]

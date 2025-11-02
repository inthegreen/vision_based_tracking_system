# 목표
실시간 비디오에서 객체를 탐지하고 추적하는 시스템을 개발합니다. 이 시스템은 객체 탐지 모델과 OpenCV 추적기를 결합하여, 객체를 탐지한 후 추적하고 (x1, x2, y1, y2), confidence, detection_time을 실시간으로 반환합니다.



# 기능 요구 사항
## 1. 실시간 비디오 처리
  * 스마트폰을 사용하여 실시간으로 프레임을 읽습니다
  * 예시 코드:
~~~
cap = cv2.VideoCapture("http://172.21.114.222:8080/video")
~~~

## 2. Object Detection
  * 첫 프레임 혹은 추적한 객체가 없는 프레임에서 jellyfishtest.pt모델을 사용하여 영상에서 객체를 탐지합니다. (https://github.com/Freezing1999/vision_based_tracking_system/blob/40547121316734e7985863426aea68ddd815678a/jellyfishtest.pt)
  * 탐지한 객체가 없는 경우 반복합니다.
  * 예시 코드:
~~~
model = YOLO("yolo11n.pt")  # load a model
ret, frame = cap.read()
results = model(frame)  # Detection
~~~

## 3. Object Tracking
  * .pt모델로 탐지된 객체를 추적하는 기능을 구현합니다.
  * 탐지된 객체의 좌표로 바운딩 박스를 정의하고, 이를 추적기에 전달하여 추적을 시작합니다.
  * 추적에 실패하는 경우 2. Object Detection으로 돌아가 다시 객체를 탐지를 시작합니다.
  * 예시 코드:
~~~
bbox = results.xyxy[0][0].cpu().numpy()

tracker = cv2.legacy.TrackerCSRT_create()
tracker.init(frame, tuple(bbox))  # 추적기 초기화
~~~

## 4. Return real-time coordinates
   * 객체가 탐지되거나 추적될 때마다, 해당 객체의 좌표와 신뢰도 또는 추적 성공 여부를 실시간으로 반환합니다.
   * 반환 형식:
     - 객체 탐지 시: (x1, x2, y1, y2), confidence
     - 객체 추적 시: (x1, x2, y1, y2), success(1.0)
     - 탐지/추적 실패 시: (x1, x2, y1, y2), 0.0 
   - 좌표(x1, x2, y1, y2): 객체의 위치와 크기 (좌측 상단 (x1, y1), 우측 하단 (x2, y2)). 추적 실패 시 이전 좌표를 그대로 반환하거나, 기본값 (0, 0, 0, 0)을 반환.(pixel 단위)
   - 신뢰도(confidence): 탐지된 객체의 정확도(0과 1 사이의 실수)
   - 추적 성공 여부(success): 추적기가 객체를 성공적으로 추적했는지 여부 (1.0 / 0.0)



# 기타 요구 사항
* 성능 최적화
  - 실시간 처리 성능이 중요합니다. 가능한 한 빠른 객체 탐지 및 추적을 구현하도록 최적화해야 합니다.
* 에러 처리
  - 추적이 실패한 경우에는 객체 탐지로 돌아가서 새로운 객체를 탐지하고 추적을 재시작합니다.
  - 기타 에러 발생시 예외 처리 또는 적절한 에러 메시지를 출력하고 시스템이 종료되지 않도록 처리합니다.
  - 2개 이상의 객체 탐지 시 최대 유사도 선택
  - 비유사도 계산식: (1-size/prior_size)(distance_from_center/half_diagonal)
 
   
* 코드의 가독성
  - 명확한 변수 및 함수명 사용
  - 주석 달기
  - 적절한 코드 블록 사용 (들여쓰기, 긴 함수나 클래스를 잘게 나누어 작성)



# 참고자료 
* https://salmon1113.tistory.com/104
* https://blueberry-kyu.tistory.com/15
* https://github.com/ultralytics/ultralytics/blob/81a614cfe5e26b8b9d1fead69478ace76a8b3a40/ultralytics/solutions/solutions.py#L171

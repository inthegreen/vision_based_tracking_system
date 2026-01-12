import numpy as np

'''위치좌표(x, y, z), 속도, 가속도, 가속도 분산'''
#x,y,z, 속도, 속도 분산 in
#가속도 계산
#input parameter은 어떤 형식?
class KalmanFilter:

    def __init__(self, dt, process_noise, init_variance):
        #상태 벡터 x:[x, y, z, vx, vy, vz, ax, ay, az](9*1)
        #dt : 두 상태 사이의 시간 간격
        self.x = np.zeros((9,1))
        self.dt = dt

        #상태 전이 행렬 A (등가속도 모델)
        self.A = np.eye(9)
        for i in range(3):
            self.A[i, i + 3]     = dt
            self.A[i, i + 6]     = 0.5 * dt**2
            self.A[i + 3, i + 6] = dt

        #측정 행렬 H (위치, 속도, 가속도를 모두 측정을 가정함)
        #만일 위치만 측정한다면 3 x 9 행렬로 수정 필요
        self.H = np.eye(9)

        #오차 공분산 행렬 P
        self.P = np.eye(9) * init_variance

        # 프로세스 노이즈 Q
        self.Q = np.eye(9) * process_noise
        
    def predict(self):
        #예측 단계 : x = A*x, P = A*p*A^T + Q
        self.x = np.dot(self.A, self.x) #내적 연산
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x

    def update(self, z, R_value):
        #z : 측정값 [x, y, z, vx, vy, vz, ax, ay, az]
        #R_value : 현재 프레임의 측정 분산 (가변 적용)
        R = np.eye(9) * R_value

        #칼만 이득 K = P*H^T * inv(H*P*H^T + R) -> 관측값에 부여할 가중치 계산
        S = np.dot(np.dot(self.H, self.P), self.H.T) + R #측정 오차의 공분산 업데이트
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        #상태 보정 : x = x + K*(z - H*x)
        y = z - np.dot(self.H, self.x)
        self.x = self.x + np.dot(K, y) #x 보정값 업데이트

        #오차 공분산 수정 : P = (I - K*H)*P
        I = np.eye(9)
        self.P = np.dot((I - np.dot(K, self.H)), self.P)

        return self.x, self.P





    # def object_detect(self):
    #     model = YOLO("yolo11n.pt")

    #     while(True):
    #         ret, frame = self.cam.read()
    #         results = model(frame)

    #         if not ret:
    #             print("kalmanFilter : video not detected")
    #             break

    #         bbox, score = self.cam.detection(frame)

    
if __name__ == "__main__":
    pass
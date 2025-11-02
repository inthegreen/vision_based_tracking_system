import time
import numpy as np

class Trajectory:
    """
    X/Z축 모터와 카메라 정보를 기반으로
    이동 경로(trajectory)를 계산하고 관리하는 클래스
    """

    def __init__(
        self,
        motor_x,                 # X축 모터 각도 (radian) (저장 안함)
        motor_z,                 # Z축 모터 각도 (radian) (저장 안함)
        camera_width_angle,      # 카메라 가로 시야각 (radian)
        camera_height_angle,     # 카메라 세로 시야각 (radian)
        image_height_pixel,      # 이미지 높이 픽셀 수
        image_width_pixel,       # 이미지 가로 픽셀 수
        target_x1,               # 타겟 x1 좌표 (저장 안함)
        target_x2,               # 타겟 x2 좌표 (저장 안함)
        target_y1,               # 타겟 y1 좌표 (저장 안함)
        target_y2,               # 타겟 y2 좌표 (저장 안함)
        camera_scale=1,          # 카메라 배율 (저장 안함)
        timestamp=None,          # 관측 시간
        sigma2=50,
        alpha=0.1,
        motor_var=0.01,
    ):
        # timestamp 기본값 지정
        if timestamp is None:
            timestamp = time.time()
        self.timestamp = timestamp

        # 카메라 정보
        self.camera_width_angle = camera_width_angle
        self.camera_height_angle = camera_height_angle
        self.image_height_pixel = image_height_pixel
        self.image_width_pixel = image_width_pixel


        # 초기 위치 및 공분산 계산
        self.p, self.sigma_p = self.compute_covariance_matrix(target_x1, target_x2, target_y1, target_y2, motor_x, motor_z,
                              p_w=self.image_width_pixel, p_h=self.camera_height_angle, scale=camera_scale):

        # 속도, 가속도 초기화
        self.v = None
        self.sigma_v = None
        self.a = None
        self.sigma_a = None

        #분산 정보
        self.sigma2=sigma2
        self.alpha=alpha
        self.motor_var=motor_var

    def compute_covariance_matrix(self, x1, x2, y1, y2, azimuth_motor, elevation_motor,
                              p_w=None, p_h=None, scale=None):
         # None 처리
        if p_w is None:
            p_w = self.image_width_pixel
        if p_h is None:
            p_h = self.image_height_pixel
        if scale is None:
            scale = 1

                                  
        # 시야각 계산
        theta_w = self.camera_width_angle/scale
        theta_h = self.camera_height_angle/scale
        
        # 상수 계산
        k = theta_w / p_w
        h = theta_h / p_h
    
        # dleta x,y 계산
        dx = x1 - x2
        dy = y1 - y2
    
        # A, B
        A = k * dx
        B = h * dy
    
        # 삼각 함수 미리 계산
        cosA, sinA = np.cos(A), np.sin(A)
        cosB, sinB = np.cos(B), np.sin(B)
    
        sinAcosB = sinA * cosB
        cosAsinB = cosA * sinB
        C = cosA * cosB
    
        # u, Dp 및 dDp/dC 계산
        u = 0.5 * np.arccos(C)
        D_p = 1.0 / np.tan(u)
        dDp_dC = 1.0 / (2.0 * np.sqrt(1.0 - C**2) * (np.sin(u)**2))
    
        # 편미분
        Dp_dx1 = k * sinAcosB * dDp_dC
        Dp_dx2 = -Dp_dx1
        Dp_dy1 = h * cosAsinB * dDp_dC
        Dp_dy2 = -Dp_dy1
    
        # 공분산 sigma_X
        alpha_sigma2 = self.alpha * self.sigma2
        sigma_X = np.array([[self.sigma2, alpha_sigma2, 0, 0],
                            [alpha_sigma2, self.sigma2, 0, 0],
                            [0, 0, self.sigma2, alpha_sigma2],
                            [0, 0, alpha_sigma2, self.sigma2]])
    
        # Jacobian J_sph
        J_sph = np.array([[Dp_dx1, Dp_dx2, Dp_dy1, Dp_dy2],
                          [-k, -k, 0, 0],
                          [0, 0, h, h]])
    
        sigma_motor = np.diag([0, motor_var, motor_var])
        sigma_s = J_sph @ sigma_X @ J_sph.T + sigma_motor
        sigma_s[0, 0] *= 2 #angle variance
    
        # 좌표 변환
        phi = azimuth_motor - 0.5 * k * (x1 + x2 - p_w)
        theta = elevation_motor - 0.5 * h * (y1 + y2 - p_h)
        sinphi, cosphi = np.sin(phi), np.cos(phi)
        sintheta, costheta = np.sin(theta), np.cos(theta)
    
        # 재사용 가능한 중간값
        sinphi_sintheta = sinphi * sintheta
        sinphi_costheta = sinphi * costheta
        cosphi_sintheta = cosphi * sintheta
        cosphi_costheta = cosphi * costheta
    
        # 위치
        Px = D_p * cosphi_costheta
        Py = D_p * sinphi_sintheta
        Pz = D_p * cosphi
    
        # Jacobian J
        J = np.array([[cosphi_costheta, -D_p * sinphi_sintheta, D_p * cosphi_costheta],
                      [sinphi_sintheta, D_p * sinphi_sintheta, D_p * cosphi_sintheta],
                      [cosphi, 0, -D_p * sinphi]])
    
        sigma_r = J @ sigma_s @ J.T
    
        return np.array([Px, Py, Pz]), sigma_r

    def update_target(
        self,
        motor_x,
        motor_z,
        target_x1,
        target_x2,
        target_y1,
        target_y2,
        image_height_pixel=None,
        image_width_pixel=None,
        camera_scale=1,
        timestamp=None,
    ):
        # 시간 갱신
        if timestamp is None:
            timestamp = time.time()
        dt = timestamp - self.timestamp
        self.timestamp = timestamp
    
        # 기본값 설정
        if image_width_pixel is None:
            image_width_pixel = self.image_width_pixel
        if image_height_pixel is None:
            image_height_pixel = self.camera_height_angle
    
        # 위치 및 공분산 계산
        p_new, sigma_p_new = self.compute_covariance_matrix(
            target_x1, target_x2, target_y1, target_y2,
            motor_x, motor_z,
            p_w=image_width_pixel,
            p_h=image_height_pixel,
            scale=camera_scale
        )
    
        # 속도 및 공분산 계산
        v_new = p_new - self.p
        sigma_v_new = (self.sigma_p + sigma_p_new) / (dt ** 2)
    
        # 등가속도 계산 (속도가 이미 있는 경우)
        if self.v is not None:
            a = (v_new - self.v) / dt
            sigma_a = (self.sigma_v + sigma_v_new) / (dt ** 2)
            self.a = a
            self.sigma_a = sigma_a
    
        # 값 업데이트
        self.v = v_new
        self.sigma_v = sigma_v_new
        self.p = p_new
        self.sigma_p = sigma_p_new


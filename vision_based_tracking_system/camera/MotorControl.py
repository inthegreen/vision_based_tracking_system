class MotorControl:
    """
    2축(X, Z) 스텝모터 제어값 계산
    """
    def __init__(self, motor_x, motor_z):
        self.motor_x = motor_x
        self.motor_z = motor_z

    def calculate_steps(self, target_pos):
        '''
        Help ~
        '''
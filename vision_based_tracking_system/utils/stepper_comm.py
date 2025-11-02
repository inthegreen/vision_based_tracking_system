import serial
import struct
import math

class MotorController(serial.Serial):
    def __init__(self, port, steps_per_rev=3200, baudrate=115200, timeout=1):
        super().__init__(port, baudrate, timeout=timeout) # timeout초 동안 기다림
        self.steps_per_rev= 3200
    def send_xy(self, x, y):
        """
        X/Z축 속도를 2바이트(big-endian, signed)로 변환하여 전송
        """
        packet=x.to_bytes(2, 'big', signed=True) +y.to_bytes(2, 'big', signed=True)
        self.write(packet)
        # 각각의 값을 2바이트(16비트)로 변환하여, 'big endian' 형식으로 정렬하고,
        # signed=True를 통해 음수도 표현할 수 있도록 합니다.
        # 두 값을 이어붙여 하나의 패킷(bytes 객체)으로 만듭니다.

    def read_steps(self):
        '''
        아두이노에서 전송된 4바이트 currentPosition 읽고 long으로 복원
        '''
        if self.in_waiting >= 8:  # X축+Z축 4바이트씩
            data = self.read(8)
            if len(data) == 8:
                pos_x, pos_z = struct.unpack('<ll', data)  # little-endian long 2개
                return pos_x, pos_z
        return None, None

    def read_angles(self):
        '''
        아두이노에서 전송된 4바이트 currentPosition 읽고 스텝에서 라디안 단위 각도로 변환
        '''
        x_steps, z_steps = self.read_steps()
        if None in (x_steps, z_steps):
            return None, None
        return (x_steps/self.steps_per_rev)*2*math.pi , (z_steps/self.steps_per_rev)*2*math.pi

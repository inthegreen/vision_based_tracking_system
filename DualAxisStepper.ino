#include <AccelStepper.h>

// X,Z축 스텝 모터 핀 설정 (A4988 드라이버 사용)
#define X_STEP_PIN 2
#define X_DIR_PIN 5
#define Z_STEP_PIN 4
#define Z_DIR_PIN 7
#define ENABLE_PIN 8  // 모터 활성화 (LOW = 활성화)

// AccelStepper 라이브러리 사용 (드라이버 모드)
AccelStepper stepperX(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);
AccelStepper stepperZ(AccelStepper::DRIVER, Z_STEP_PIN, Z_DIR_PIN);
//:: -> Scope resolution operator, DRIVER is predefined in Accelstepper

void setup() {
  Serial.begin(115200); // 시리얼 통신 시작, 속도는 115200bps

  // 스텝 모터 설정
  stepperX.setMaxSpeed(500); //(step/sec)
  stepperX.setAcceleration(300); //(step/sec^2)

  stepperZ.setMaxSpeed(500);
  stepperZ.setAcceleration(300);

  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(ENABLE_PIN, LOW);  // 모터 활성화

  // X축, Z축 스텝 모터 속도 초기화
  stepperX.setSpeed(0);
  stepperZ.setSpeed(0);

  stepperX.setCurrentPosition(0);  // 현재 위치를 0으로 초기화
}

void loop() {
  // 모터  항상 실행 (비동기 동작, 부드러운 속도 조절)
  stepperX.runSpeed();
  stepperZ.runSpeed();

  if (Serial.available() >=4) {
    int16_t x = (Serial.read() <<8) |Serial.read(); //big endian
    int16_t z = (Serial.read() <<8) |Serial.read();

    // X축, Z축 스텝 모터 속도 및 방향 설정
    stepperX.setSpeed(x);
    stepperZ.setSpeed(z);

    // currentPosition() 전송 (long → 4바이트)
    long pos_X = stepperX.currentPosition();
    Serial.write((uint8_t*)&pos_X, sizeof(pos_X));  // 4바이트 그대로 전송
    long pos_Z = stepperZ.currentPosition();
    Serial.write((uint8_t*)&pos_Z, sizeof(pos_Z));  // 4바이트 그대로 전송
    // Serial.write(buf, len)
    // buf: an array to send as a series of bytes.
    // len: the number of bytes to be sent from the array.
    // (uint8_t*)&pos -> pos 변수의 메모리 주소를 바이트 단위 포인터로 변환
    // sizeof(pos) -> 전송할 바이트 수
    // Serial.write 내부 동작:
    //   for (int i = 0; i < sizeof(pos); i++) {
    //       sendByte(ptr[i]); // ptr[i] = *(ptr + i)
    //       // ptr 포인터는 1바이트씩 증가 (+1)
    //   }
  }

  delay(10); // 0.01 sec delay
}

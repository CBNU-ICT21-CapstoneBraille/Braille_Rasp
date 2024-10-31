import serial
from time import sleep

# 시리얼 포트 설정 
ser = serial.Serial('/dev/ttyUSB0', 9600) 

def send_command(command):
    ser.write(command.encode())  # 문자열을 바이트로 인코딩해서 전송
    sleep(0.1)  # 안정적인 통신을 위해 약간의 지연을 둠

# 점자 패턴 출력 루프
no_module = 1
while True:
    for i in range(no_module):
        for j in range(6):
            send_command(f"ON {i} {j}")
            sleep(0.5)  # 500ms 지연
            send_command(f"OFF {i} {j}")

import asyncio
from bleak import BleakClient, BleakScanner
import serial
from time import sleep

#BLE 장치
DEVICE_NAME = "S20 FE"
SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

#BLE 탐색
async def connect_to_device():
    print("장치 검색 중...")

    devices = await BleakScanner.discover()

    device = None
    for d in devices:
        if DEVICE_NAME in d.name:
            device = d
            break

    if not device:
        print("장치를 찾을 수 없습니다.")
        return

    #연결 시도
    async with BleakClient(device) as client:
        print(f"장치 {device.name}에 연결되었습니다.")

        #BLE 서비스 데이터 수신
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        print("OCR 텍스트 수신 대기...")
        await asyncio.sleep(60)

        #수신 종료
        await client.stop_notify(CHARACTERISTIC_UUID)

# BLE 장치에서 데이터를 수신시 호출 callback
def notification_handler(sender: int, data: bytearray):
    #데이터를 문자열 변환
    text = data.decode("utf-8")
    print(f"수신한 텍스트: {text}")

async def main():
    await connect_to_device()

asyncio.run(main())


# 시리얼 포트 설정
ser = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    for char in text:
        if char.isalpha():  # 알파벳 문자인지 확인
            ser.write(char.encode())
            print(f"Sent '{char}' to Arduino.")
            sleep(0.5)  # 각 문자 전송 후 0.5초 지연
        else:
            print(f"'{char}' is not a letter.")

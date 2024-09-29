import asyncio
from bleak import BleakClient, BleakScanner

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
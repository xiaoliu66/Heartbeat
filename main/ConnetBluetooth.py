import asyncio

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

# 设备的Characteristic UUID
par_notification_characteristic = "00002a37-0000-1000-8000-00805f9b34fb"
# 设备的MAC地址
device_address = "C8:06:E2:3C:E1:91"

value = 0


# 监听回调函数，此处为打印消息
def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    global value
    # print("rev data:", data)   # 读取到的数据 rev data: bytearray(b'\x06V')
    # print("rev data:", int.from_bytes(data))

    #  rev data: bytearray(b'\x06\x82')
    # ❤: 130
    # bytearray(b'\x06T') 转换为十进制，我们首先需要理解这个字节串的含义。bytearray 表示一组字节，其中 \x06 和 \x54 是十六进制表示的两个字节。
    #
    #     1.\x06 对应的十进制值是 6。 暂时不知道这个值有啥用
    #     2.\x54 对应的十进制值是 84。  心跳的值， T 的ascii 的十六进制是54
    value = int(data.hex().split('06')[1], 16);

    print('❤:', value)
    return value
    # print(data.decode('ascii'))
    # print(data)


# 将心跳数据返回给Ui
def getHeartNum():
    global value
    return value


async def main():
    print("starting scan...")

    # 基于MAC地址查找设备
    device = await BleakScanner.find_device_by_address(
        device_address, cb=dict(use_bdaddr=False)  # use_bdaddr判断是否是MOC系统
    )
    if device is None:
        print("could not find device with address '%s'", device_address)
        return

    # 事件定义
    disconnected_event = asyncio.Event()

    # 断开连接事件回调，当设备断开连接时，会触发该函数，存在一定延迟
    def disconnected_callback(client):
        print("Disconnected callback called!")
        disconnected_event.set()

    print("connecting to device...")
    async with BleakClient(device, disconnected_callback=disconnected_callback) as client:
        print("Connected")

        await client.start_notify(par_notification_characteristic, notification_handler);

        # value1 = await client.read_gatt_char(uuid)
        # print('value',value)
        await disconnected_event.wait()  # 休眠直到设备断开连接，有延迟。此处为监听设备直到断开为止
        # await asyncio.sleep(10.0)           #程序监听的时间，此处为10秒
        # await client.stop_notify(par_notification_characteristic)


# asyncio.run(main())

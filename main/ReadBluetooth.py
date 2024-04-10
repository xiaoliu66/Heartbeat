# import asyncio
# from bleak import BleakClient, BleakGATTCharacteristic
#
# address = "C8:06:E2:3C:E1:91"
# MODEL_NBR_UUID = "0x2A37"
# MODEL_NBR_UUID1 = "0x180D"
# MODEL_NBR_UUID2 = "180D"
#
# def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
#     print("rev data:", data)
#
# async def main(address):
#     async with BleakClient(address) as client:
#         await client.start_notify(MODEL_NBR_UUID,notification_handler)
#         model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#         print("Model Number: {0}".format("".join(map(chr, model_number))))
#
#
# asyncio.run(main(address))

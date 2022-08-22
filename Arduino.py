from serial import Serial
import DataBase as db


class Serial_Arduino:
    def __init__(self):
        self.ser = Serial("COM6", 19200)

    def push(self):
        print("push")
        self.ser.write('1'.encode())

    def pull(self):
        print("wait")
        db.data_from_arduino = str(self.ser.readline()).split("b'")[1].split("\\r\\n")[0]
        print(db.data_from_arduino)

# ser = Serial("COM7", 19200)
# data = str(ser.readline()).split("b'")
# print(data)
# time.sleep(1)
# ser.write('1'.encode())

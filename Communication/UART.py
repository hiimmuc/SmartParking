# TODO: connect with arduino with uart serial communication, also use for reading RFID
import serial


class UART():
    def __init__(self, port, baud_rate=9600, timeout=0):
        self.rfid_serial_port = serial.Serial(port, baud_rate, timeout)

    def read_id(self):
        id_num = []
        i = 0
        while True:
            serial_data = self.rfid_serial_port.read()
            data = serial_data.decode('utf-8')
            i = i + 1
            if i == 12:
                i = 0
                ID = "".join(map(str, id_num))
                print(ID)
                break
            else:
                id_num.append(data)
        return id_num


if __name__ == '__main__':
    uart = UART('COM1')
    uart.read_id()

# TODO: connect with plc via rs485, modbus rtu

from easymodbus.modbusClient import ModbusClient


class RS485:
    def __init__(self, port="COM0", is_rtu=True, ip=None):
        self.connected_to_plc = False
        self.port = port
        self.ip = ip
        self.is_rtu = is_rtu

    def check_connection(self):
        #  check connection
        try:
            if self.is_rtu:
                plc = ModbusClient(f'COM{self.port}')
            else:
                plc = ModbusClient(self.ip, self.port)
            self.connected_to_plc = True
            plc.close()
        except:
            self.connected_to_plc = False

    def write(self, type_, address, value):
        try:
            #  check connection
            try:
                if self.is_rtu:
                    plc = ModbusClient(f'COM{self.port}')
                else:
                    plc = ModbusClient(self.ip, self.port)
            except Exception as e:
                print("Error", e)
            if not plc.is_connected():
                plc.connect()
            if plc.is_connected():
                print("PlC is connected, writing_time")
                self.connected = True

            if type_ == 'coil':
                plc.write_single_coil(address, value)
            elif type_ == 'reg':
                plc.write_single_register(address, value)
        except Exception as e:
            self.popup_msg(msg=e, src_msg='write_to_PLC_core', type_msg='warning')
            self.connected = False

    def read(self, type_, address):
        """read data from plc with type and address defined

        Args:
            type_ (str): type of reading functions. Available: hr, ir, coil.
            address (int): address of reading type. eg. 1, 2, 3.

        Returns:
            [list]: list of results
        """
        try:
            if self.is_rtu:
                plc = ModbusClient(f'COM{self.port}')
            else:
                plc = ModbusClient(self.ip, self.port)

            if not plc.is_connected():
                plc.connect()
            if type_.strip() == 'hr':
                return plc.read_holdingregisters(address, 1)[0]

            if type_.strip() == 'ir':
                return plc.read_inputregisters(address, 1)[0]

            if type_.strip() == 'coil':
                return plc.read_coils(address, 1)[0]
        except Exception as e:
            self.popup_msg(e, src_msg='read_from_PLC')

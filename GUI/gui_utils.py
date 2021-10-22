import os
import sys
from pathlib import Path

import cv2
import pandas as pd
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

try:
    from config import *

    from GUI.gui import *
    from GUI.gui_thread import *
except Exception as e:
    sys.stdout.write(str(e))

    from gui import *
    from gui_thread import *


def convert_cv2qt(cv_img, size=(640, 360)):
    '''Convert cv image to qt image to display on gui

    Args:
        cv_img (ndarray): BGR image

    Returns:
        image: RGB image with qt format
    '''
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(*size, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)


# noinspection PyAttributeOutsideInit
class App(Ui_MainWindow, VideoThread, QtWidgets.QWidget):
    def __init__(self, MainWindow, rs485, model) -> None:
        super().__init__()
        self.setupUi(MainWindow)

        self.model = model
        self.rs485_pipe = rs485

        self.rs485_connected = False

        self.uart_connected = False
        self.detect_flag = True

        self.is_error = False
        self.running = False
        self.current_slot_num = 37
        self.max_slots = 99

        self.thread = VideoThread()
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.camera_screen)

        self.startButton.clicked.connect(self.start_program)
        self.stopButton.clicked.connect(self.stop_program)
        self.InputID.returnPressed.connect(self.get_id_input)

        # timer for reading step
        self.timer = QtCore.QTimer()

        # Table
        self.table = {'database': {'ID': [],
                                   'plate_id': [],
                                   'plate_path': []},
                      'account': {'ID': [],
                                  'money_left': []},
                      'plc': {}}

        # databsase root
        self.root_dir = str(Path("backup"))

    # TODO: complete here
    def start_program(self):
        self.thread.start()
        # self.rs485_pipe.check_connection()
        # self.rs485_connected = self.rs485_pipe.connected_to_plc
        self.program_pipeline()
        self.update_lcd_led(mode='reset')
        self.running = True

    def stop_program(self):
        self.thread.stop()
        self.running = False
        sys.exit(1)

    def popup_msg(self, msg, src_msg='', type_msg='error'):
        """Create popup window to the ui

        Args:
            msg (str): message you want to show to the popup window
            src_msg (str, optional): source of the message. Defaults to ''.
            type_msg (str, optional): type of popup. Available: warning, error, information. Defaults to 'error'.
        """
        try:
            self.popup = QMessageBox()
            if type_msg.lower() == 'warning':
                self.popup.setIcon(QMessageBox.Warning)
            elif type_msg.lower() == 'error':
                self.popup.setIcon(QMessageBox.Critical)
                self.is_error = True
            elif type_msg.lower() == 'info':
                self.popup.setIcon(QMessageBox.Information)

            self.popup.setText(f"[{type_msg.upper()}] -> From: {src_msg}\nDetails: {msg}")
            self.popup.setStandardButtons(QMessageBox.Ok)
            self.popup.exec_()
            print(f'[{type_msg.upper()}]: {msg} from {src_msg}')
        except Exception as e:
            print('-> From: popup_msg', e)

    # +++++++++++++++++++++++++++++++++++ Camera view handling ++++++++++++++++++++++++++++++++++++++++

    @pyqtSlot(np.ndarray, list)
    def camera_screen(self, cv_img):
        '''continuous update camera screen using thread

        Args:
            cv_img (array): BGR image
        '''
        self.current_frame = cv_img
        qt_img = convert_cv2qt(self.current_frame, size=(640, 360))
        self.screen.setPixmap(qt_img)

    def update_extracted_image(self, screen, cv_img):
        '''update image on screen

        Args:
            cv_img:
            screen ([str]): which screen to update in or out
        '''
        qt_img = convert_cv2qt(cv_img)
        if screen == 'view_in':
            self.ViewPlateIn.setPixmap(qt_img)
        elif screen == 'view_out':
            self.ViewPlateOut.setPixmap(qt_img)

    # +++++++++++++++++++++++++++++++++++ License detection handling ++++++++++++++++++++++++++++++++++++++++
    def is_detected_plate(self):
        if self.detect_flag:
            self.current_plate, self.current_plate_id, _ = self.model.extract_info(self.current_frame,
                                                                                   detection=True,
                                                                                   ocr=False,
                                                                                   preprocess=True)

            if len(self.current_plates) > 0:
                return True
            else:
                return False

    # +++++++++++++++++++++++++++++++++++ PLC tracking table handling ++++++++++++++++++++++++++++++++++++++++

    def check_if_expand(self, table_name):
        try:
            table = self.tableWidget

            n_rows = table.rowCount()
            data_length = len(self.table[table_name])
            gap = data_length - n_rows
            if gap > 0:
                for i in range(n_rows, data_length):
                    table.insertRow(i)
        except Exception as e:
            self.popup_msg(str(e), src_msg='check_if_expanding', type_msg='error')

    def tracking_plc_table(self, mode='init'):
        try:
            table_name = 'plc'
            table = self.tableWidget
            if mode != 'init':
                # reset table
                nrows = table.rowCount()
                table.setVerticalHeaderLabels(tuple(["newRow"] * nrows))  # set name
                table.clearContents()

            self.read_csv(table_name)
            self.check_if_expand(table_name)
            table = self.tableWidget
            # update table
            for i in range(len(self.table[table_name]['name'])):
                table.setVerticalHeaderItem(i, QTableWidgetItem(self.table[table_name]['name'][i]))
                table.setItem(i, 0, QTableWidgetItem(self.table[table_name]['type'][i]))
            print('-> Tracking PLC table')
        except Exception as e:
            self.popup_msg(str(e), src_msg='tracking_plc_table', type_msg='error')

    def update_tracking_plc_table(self):
        """Read data from PLC and update the tracking table widget in UI widget.
        """
        try:
            if self.rs485_connected:
                table_name = 'plc'
                table = self.tableWidget
                # read value from plc and update tracking values
                for i in range(len(self.table[table_name]['name'])):
                    address = int(self.table[table_name]['address'][i])
                    type_ = self.table[table_name]['type'][i]
                    values = self.rs485_pipe.read(type_, address)

                    table.setItem(i, 1, QTableWidgetItem(f"{values}"))
            else:
                self.popup_msg("Com is not connect", src_msg='update_tracking_table', type_msg='warning')
        except Exception as e:
            self.popup_msg(str(e), src_msg='update_tracking_table')

    # +++++++++++++++++++++++++++++++++++ CSV files handling ++++++++++++++++++++++++++++++++++++++++

    def read_csv(self, table_name):
        ''' Read data from csv

        Args:
            table_name (str): name of file to read
        '''
        try:
            csv_path = Path(self.root_dir, f"{table_name}.csv")
            data = pd.read_csv(csv_path)
            if table_name == 'database':
                self.table[table_name]['ID'] = list(data['ID'])
                self.table[table_name]['plate'] = list(data['plate_id'])
                self.table[table_name]['plate_path'] = list(data['plate_path'])
            elif table_name == 'account':
                self.table[table_name]['ID'] = list(data['ID'])
                self.table[table_name]['money_left'] = list(data['money_left'])
            elif table_name == 'plc':
                self.table[table_name]['name'] = list(data['name'])
                self.table[table_name]['type'] = list(data['type'])
                self.table[table_name]['address'] = list(data['address'])
            print(f'[INFO] Read {table_name} table from csv')
        except Exception as e:
            self.popup_msg(f'Error: {e}', 'read_csv', 'error')

    def write_csv(self, table_name):
        '''Write dictionary dataframe to csv

        Args:
            table_name (dict):  data to write
        '''
        try:
            df = pd.DataFrame.from_dict(self.table[table_name])
            csv_path = str(Path(self.root_dir, f"{table_name}.csv"))
            df.to_csv(csv_path, sep=',', index=False)
        except Exception as e:
            self.popup_msg(f'Error: {e}', 'write_csv', 'error')

    def init_all_table(self):
        self.read_csv('account')
        self.read_csv('database')
        self.read_csv('plc')

    # +++++++++++++++++++++++++++++++++++ ID part handling ++++++++++++++++++++++++++++++++++++++++

    # track slot in park and money in account after that display on screen
    def get_id_input(self):
        text = self.InputID.text()
        self.currentID = text
        self.InputID.clear()

    def database_handle(self, id=0, plate_num=None, plate=None, mode='add'):
        if mode == 'add':
            save_path = str(Path(self.root_dir, f"{plate_num}.jpg"))

            self.table['database']['ID'].append(id)
            self.table['database']['plate_id'].append(plate_num)
            self.table['database']['plate_path'].append(save_path)
            cv2.imwrite(save_path, plate)

            self.write_csv('database')
        if mode == 'remove':
            save_path = str(Path(self.root_dir, f"{plate_num}.jpg"))

            self.table['database']['ID'].remove(id)
            self.table['database']['plate_id'].remove(plate_num)
            self.table['database']['plate_path'].remove(save_path)
            os.remove(save_path)

            self.write_csv('database')

    # +++++++++++++++++++++++++++++++++++ Utils function ++++++++++++++++++++++++++++++++++++++++++

    def update_lcd_led(self, lcd='', value=0, mode='default'):
        '''Change number in lcd display to value

        Args:
            mode:
            lcd (str): name of lcd
            value (int): Value to display
        '''
        lcd_box = {'TotalSlot': self.TotalSlot,
                   'MoneyLeft': self.MoneyLeft,
                   'SlotCount': self.SlotCount}
        if lcd in lcd_box.keys():
            lcd_box[lcd].display(str(int(value)))
        else:
            mode = 'reset'
            print(f'[WARNING] LCD {lcd} not specified')

        if mode == 'reset':
            lcd_box['MoneyLeft'].display(00000)
            self.current_slot_num = len(self.table['database']['ID'])
            self.max_slots = len(self.table['account']['ID'])
            lcd_box['SlotCount'].display(self.current_slot_num)
            lcd_box['TotalSlot'].display(self.max_slots)

    def update_label(self, label, value):
        '''Change text of label box (only plate number)

        Args:
            label (str): label box name
            value (str): string to display in label box
        '''
        if label == 'extractedInfo':
            self.extractedInfo.setText(value)
        pass

    def update_color_led_label(self, label, color):
        '''Change color of label box to look as led on, off or error

        Args:
            label (srt): name of label box
            color (srt): color to display
        '''
        if label == 'ledTrigger':
            self.ledTrigger.setStyleSheet(f"background-color: {color}")
        elif label == 'Verify':
            self.VerifyBox.setStyleSheet(f"background-color: {color}")
        pass

    def delay(self, seconds):
        '''delay'''
        ms = int(seconds * 1000)
        self.timer.singleShot(ms, self.dummy_clock)

    def dummy_clock(self):
        '''do nothing, just to delay
        '''
        pass

    # TODO: complete here
    def park_control(self, method):
        '''
        '''
        if method == 'pay':
            # tru tien tai khoan
            ticket = Parking.price
            # cap nhat self.MoneyLeft toi so du hien tai
            pass
        elif method == 'open left':
            # mo cong vao
            self.SlotCount += 1

            pass
        elif method == 'open right':
            # mo cong ra
            self.SlotCount -= 1
            pass

    def image_flow(self, image, image_path, mode='save'):
        '''control flow of image to communicate with excel and backup folder

        Args:
            image (image): [description]
            name (name to save): id of plate
            format (str, optional): format of image. Defaults to 'jpg'.
            mode (str, optional): save or delete. Defaults to 'save'.
        '''
        if mode == 'save':
            cv2.imwrite(image_path, image)
        elif mode == 'delete':
            if os.path.exists(image_path):
                os.remove(image_path)

    # +++++++++++++++++++++++++++++++++++ start ++++++++++++++++++++++++++++++++++++++++++
    # TODO: complete here
    def program_pipeline(self):
        try:
            self.init_all_table()
            self.update_lcd_led()
            if self.is_detected_plate():
                self.detect_flag = False
                #  read database if exits plot
                plates = self.current_plates
                plate_ids = self.current_plate_ids

                # Xe di ra khoi khu vuc
                if plate_ids in self.table['database']['plate_id'] or self.currentID in self.table['account']['ID']:
                    idx = self.table['database']['id'].index(plate_ids)
                    plate_path = self.table['database']['plate_path'][idx]
                    plate_img = cv2.imread(plate_path)
                    self.update_extracted_image('view_out', plate_img)
                    self.update_label('extractedInfo', f"{plate_ids}")
                    self.update_extracted_image('view_in', plates[0])
                    self.update_color_led_label('Verify', 'green')
                    self.update_color_led_label('ledTrigger', 'red')
                    # >> get id from rfid
                    self.park_control('pay')
                    self.park_control('open right')
                    self.update_lcd_led('Money')
                    self.update_lcd_led('SlotCount')
                    # TODO xoa khoi database
                    self.database_handle(id=self.currentID, plate_num=plate_ids, plate=plate_img, mode='remove')
                    self.delay(3)
                    self.update_lcd_led(mode='reset')

                else:
                    # Xe di vao khu vuc
                    self.update_extracted_image('view_in', plates[0])
                    self.update_label('extractedInfo', f"{plate_ids}")
                    self.update_color_led_label('Verify', 'red')
                    self.update_color_led_label('ledTrigger', 'green')
                    # >> get id from rfid
                    self.park_control('open left')
                    # TODO them vao database
                    self.database_handle(id=self.currentID, plate_num=plate_ids, plate=plates[0], mode='add')

                    self.update_lcd_led('Money')
                    self.update_lcd_led('SlotCount')

                # sau khi lam xong hanh dong tren thi phat co cho detect tiep
                self.detect_flag = True
            else:
                # khong co xe
                self.update_color_led_label('Verify', 'white')
                self.update_color_led_label('ledTrigger', 'white')
                self.detect_flag = True

        except Exception as e:
            self.popup_msg(str(e), 'program_pipeline', 'error')


def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App(MainWindow=MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()

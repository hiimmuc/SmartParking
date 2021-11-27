import os
import sys
from pathlib import Path

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
        # create thread
        self.thread = VideoThread(recognizer_model=model)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.program_pipeline)

        self.startButton.clicked.connect(self.start_program)
        self.stopButton.clicked.connect(self.stop_program)
        self.InputID.returnPressed.connect(self.get_id_input)

        # ===========================================================

        self.model = model
        self.rs485_pipe = rs485

        self.rs485_connected = False
        self.processing_flag = False

        self.is_error = False
        self.running = False
        self.idle_count = 0
        self.current_slot_num = 0
        self.max_slots = 3
        self.currentID = None
        self.current_plate = None
        self.got_id = False
        self.plate_in = False
        self.bar_closed = [True, True]  # 0 for left 1 for right

        # timer for reading step
        self.timer = QtCore.QTimer()

        # Table
        self.table = {'database': {},
                      'account': {'ID': [],
                                  'money_left': []},
                      'plc': {}}

        # databsase root
        self.root_dir = str(Path("backup"))

    # TODO: complete here
    def start_program(self):
        self.init_all_table()
        self.update_lcd_led()

        # check rs485
        self.rs485_pipe.check_connection()
        self.rs485_connected = self.rs485_pipe.connected_to_plc
        self.update_tracking_plc_table()

        # run video`
        self.thread.start()
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
                self.is_error = True
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

    def camera_screen(self, cv_img):
        '''continuous update camera screen using thread

        Args:
            cv_img (array): BGR image
        '''
        qt_img = convert_cv2qt(cv_img, size=(640, 360))
        self.screen.setPixmap(qt_img)

    def update_extracted_image(self, screen, cv_img):
        '''update image on screen

        Args:
            cv_img:
            screen ([str]): which screen to update in or out
        '''
        qt_img = convert_cv2qt(cv_img, size=(359, 179))
        if screen == 'view_in':
            self.ViewPlateIn.setPixmap(qt_img)
        elif screen == 'view_out':
            self.ViewPlateOut.setPixmap(qt_img)

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

    def update_tracking_plc_table(self):
        """Read data from PLC and update the tracking table widget in UI widget.
        """
        try:

            if self.rs485_connected:
                table_name = 'plc'
                table = self.tableWidget
                # read value from plc and update tracking values
                for i, name in enumerate(self.table[table_name]['name']):

                    address = int(self.table[table_name]['address'][i])
                    type_ = self.table[table_name]['type'][i]
                    values = self.rs485_pipe.read(type_, address)

                    table.setItem(i, 0, QTableWidgetItem(f"{name}"))
                    table.setItem(i, 1, QTableWidgetItem(f"{values}"))

                    if name == 'flag':
                        self.processing_flag = bool(values)
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
            data = pd.read_csv(csv_path, converters={i: str for i in range(0, self.max_slots)})

            if table_name == 'database':
                self.table[table_name]['Index'] = list(data['Index'])
                self.table[table_name]['ID'] = list(data['ID'])
                self.table[table_name]['plate_id'] = list(data['plate_id'])
                self.table[table_name]['plate_path'] = list(data['plate_path'])
                self.max_slots = len(self.table[table_name]['Index'])
                # print(self.table[table_name])

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

    # +++++++++++++++++++++++++++++++++++ ID module handling ++++++++++++++++++++++++++++++++++++++++

    # track slot in park and money in account after that display on screen
    def get_id_input(self, auto_clear=False):
        text = self.InputID.text()
        if auto_clear:
            self.InputID.clear()
        return text if len(text) > 0 else ''

    def database_handle(self, id=0, plate_num=None, save_path='', mode='add'):
        '''Handling database.csv

        Args:
            id (int, optional): ID of id card. Defaults to 0.
            plate_num (int, optional): number of plate. Defaults to None.
            save_path (str, optional): saving part for plate image. Defaults to ''.
            mode (str, optional): add or remove id from database. Defaults to 'add'.

        Returns:
            int: id of add or remove.
        '''
        if mode == 'add':

            idx = self.slots_control()[0]
            # take first available slot
            print((self.current_slot_num, self.max_slots))

            if self.current_slot_num < self.max_slots:
                self.table['database']['ID'][idx] = id
                self.table['database']['plate_id'][idx] = plate_num
                self.table['database']['plate_path'][idx] = save_path
            else:
                self.popup_msg('Database is full', 'database_handle', 'warning')
                self.park_control('close left', 0)
                self.park_control('close right', 0)

            self.write_csv('database')
            return idx

        if mode == 'remove':
            idx = self.table['database']['ID'].index(id)

            self.table['database']['ID'][idx] = ' '
            self.table['database']['plate_id'][idx] = ' '
            self.table['database']['plate_path'][idx] = ' '

            self.write_csv('database')

            return idx

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
            mode = 'default'

        if mode == 'default':
            self.current_slot_num = self.max_slots - len(self.slots_control())

            lcd_box['MoneyLeft'].display(00000)
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

    def delay(self, seconds):
        '''delay'''
        ms = int(seconds * 1000)
        self.timer.singleShot(ms, self.dummy_clock)

    def dummy_clock(self):
        '''do nothing, just to delay
        '''
        pass

    def pay_money(self, currentID):
        '''Pay money from account'''
        # tru tien tai khoan
        ticket = Parking.price
        # cap nhat self.MoneyLeft toi so du hien tai
        idx = self.table['account']['ID'].index(currentID)
        current_money = str(int(self.table['account']['money_left'][idx]) - ticket)

        self.table['account']['money_left'][idx] = current_money
        self.write_csv('account')

        return current_money

    def park_control(self, state, idx=None):
        '''control activities of parking lot

        Args:
            method (str): pay , enter ofr exit
            currentID (str): id of card
            idx (int, optional): index of slot. Defaults to None.

        Returns:
            int: current slot number
        '''
        if idx is not None:
            idx += 1
            msg = 0
            print('Enter idx not None')

            if state == 'enter':
                self.current_slot_num += 1
                msg = idx * 10 + 1
            elif state == 'exit':
                self.current_slot_num -= 1
                msg = idx * 10 + 0

            self.rs485_pipe.write('reg', 200, msg)
            return self.current_slot_num

    def image_flow(self, image, image_path, mode='save'):
        '''control flow of image to communicate with excel and backup folder

        Args:
            image (image): [description]
            name (name to save): id of plate
            format (str, optional): format of image. Defaults to 'jpg'.
            mode (str, optional): save or delete. Defaults to 'save'.
        '''
        if mode == 'save':
            if isinstance(image, np.ndarray):
                cv2.imwrite(image_path, image)
            else:
                print('Error: image is not numpy array')
        elif mode == 'delete':
            if os.path.exists(image_path):
                os.remove(image_path)

    def slots_control(self):
        remain_slots = []
        for i in range(len(self.table['database']['ID'])):
            if self.table['database']['ID'][i] == ' ':
                remain_slots.append(i)
        return remain_slots

    # +++++++++++++++++++++++++++++++++++ program pipeline ++++++++++++++++++++++++++++++++++++++++++

    @ pyqtSlot(np.ndarray, list)
    def program_pipeline(self, frame=None, plate_info=None):
        id_exist = False
        plate_exist = False
        current_money = 0

        ID = self.get_id_input()

        if ID != self.currentID:
            if frame is not None and self.got_id:
                default_frame = np.ones_like(frame)
                self.update_extracted_image('view_in', default_frame)
                self.update_extracted_image('view_out', default_frame)

        try:

            assert frame is not None, "Camera source is not found"
            # show frame from camera
            self.camera_screen(frame)
            self.current_plate, plate_ids, conf = plate_info
            os.makedirs(Path(self.root_dir, 'saved_plate_img'), exist_ok=True)

            if not self.processing_flag:
                # validate ID
                if len(ID) == 10:
                    self.currentID = ID
                    self.got_id = True
                    print(f'[INFO] currentID: {self.currentID}')

                    if self.currentID in self.table['database']['ID']:
                        id_exist = True
                        current_money = self.pay_money(self.currentID)
                    else:
                        id_exist = False
                        idx = self.table['account']['ID'].index(self.currentID)
                        current_money = self.table['account']['money_left'][idx]

                    self.MoneyLeft.display(current_money)

                else:
                    self.got_id = False

                # validate plate
                if plate_ids and conf > 0.6:
                    self.plate_in = True
                    print(f'[INFO] plate_ids: {plate_ids}, {conf}')

                    save_path = str(Path(self.root_dir, 'saved_plate_img',  f"{str(plate_ids)}.jpg"))
                    if plate_ids in self.table['database']['plate_id']:
                        plate_exist = True
                    else:
                        plate_exist = False

                else:
                    self.plate_in = False

                # * if vehicle come into camera view and plate is detected
                if self.plate_in and self.got_id:
                    if id_exist and plate_exist:
                        print("[INFO] Xe di ra khoi khu vuc")
                        idx = self.table['database']['ID'].index(self.currentID)

                        # * 1. doc anh bien xe luu o database
                        plate_in_img = cv2.imread(self.table['database']['plate_path'][idx])

                        # * 2. update vao view out
                        self.update_extracted_image('view_out', plate_in_img)
                        self.update_label('extractedInfo', f'{plate_ids}')

                        # * 3. update anh camera quay dc vao view in
                        self.update_extracted_image('view_in', self.current_plate)

                        # * 4. update led label verify -> green
                        self.update_color_led_label('Verify', 'green')

                        # * 5. xoa khoi database by database_handle(remove)
                        rm_idx = self.database_handle(id=self.currentID,
                                                      plate_num=plate_ids,
                                                      save_path=save_path,
                                                      mode='remove')

                        # * 6. truyen tin hieu mo cong ben phai park_control(open right)
                        slot_now = self.park_control(state='exit', idx=rm_idx)

                        # * 7. remove image view
                        self.image_flow(self.current_plate, save_path, mode='delete')

                        # * 8. update slots count (so xe hien tai trong bai)
                        self.update_lcd_led('SlotCount', slot_now)

                        self.plate_in = False
                        self.got_id = False

                    else:
                        print("[INFO] Xe di vao khu vuc")

                        # * 1. update anh camera quay duoc len view in, den khi co anh moi thi moi doi anh
                        self.update_extracted_image('view_in', self.current_plate)
                        default_frame = np.ones_like(frame)
                        self.update_extracted_image('view_out', default_frame)

                        # * 2. update led label verify -> red
                        self.update_color_led_label('Verify', 'yellow')

                        self.update_color_led_label('ledTrigger', 'green')

                        # * 3. update label extractedInfo to plate id
                        self.update_label('extractedInfo', f'{plate_ids}')

                        # * 4. them vao database by database_handle(add)
                        add_idx = self.database_handle(id=self.currentID,
                                                       plate_num=plate_ids,
                                                       save_path=save_path,
                                                       mode='add')

                        # * 5. truyen tin hieu mo cong ben trai park_control(open left)
                        slot_now = self.park_control(state='enter', idx=add_idx)

                        # * 6. add image view
                        self.image_flow(self.current_plate, save_path, mode='save')

                        # * 7. update led slot count
                        self.update_lcd_led('SlotCount', slot_now)

                        # * 8. bat bit flag
                        self.rs485_pipe.write('coil', 101, 1)

                        self.processing_flag = True

                        self.plate_in = False
                        self.got_id = False

                    self.update_tracking_plc_table()

                if len(ID) >= 10:
                    # >> when receive all 10 digits of ID, then clear
                    self.InputID.clear()

                self.update_color_led_label('ledTrigger', 'yellow')

            else:
                # >> to notice that processing is running and wait for next turn
                self.update_color_led_label('ledTrigger', 'red')

                if self.idle_count > 30:
                    self.update_tracking_plc_table()
                    self.idle_count = 0

                self.idle_count += 1

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

to display application to track entrance. 1 to display real time cammera, 1 to display captured image and its information. 1 table to track rs485 and some text blabla

table to track coil in plc

flow cho gui:
start de khoi dong he thong
stop de dung va thoat ung dung

- CameraView hien hinh anh realtime quay duoc tu camera dong thoi chay qua yolo
- neu phat hien plate yolo tra ve hinh anh da crop + preprocess -> hien len CameraViewIn, khach hang tien hanh quet the vao rfid de lay id (id scan form id card) va hien so tien con lai trong tai khoan the(money left in account), lay thong tin nay tu account.csv; dong thoi Countbox + 1 va hien thi; add id, number plate, path to save plate picture vao database.csv; textlabel(ledtriggerblock sang xanh, k co xe thi k co mau)
- khi xe ra ledtrigger sang do, quet the vao de lay rfid roi trich xuat trong database plate num va plate path roi plot platepath len camera view in, dong thoi plot plate detect luc do len camera view out hien lai plate detect dc luc do, so sanh voi plate naum , neu trung khop thi verify hien mau xanh truyen xuong plc mo cong.; tru tien trong tai khoan cua id do, xoa id do khoi database.csv, -1 tron slotcount
- sau 3s thi tu dong reset lai hien thi lcd ve 0 cho id, con cho slot count thi luon hien thi

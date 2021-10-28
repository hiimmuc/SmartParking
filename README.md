Main functions:
- 1 plc để điều khiển các thành phần thực thi, giao tiếp rs485
- 1 arduino để đọc thẻ ID, sử dụng rf id, giao tiếp với máy tính bằng UART
- 1 camera để đọc biển số xe
Đọc biển số:
- mô hình detect biển số xe  để detect và crop, allign biển số xe trong ảnh -> đâu ra là ảnh trực diện
- mô hình OCR để detect chữ trong ảnh trực diện
-> đầu ra cuối là ảnh trực diện + chữ, tên ảnh đặt bằng ID
lưu vào csv ID / biển / số tiền còn
- code comunication để giao tiếp rs485, uart
- code gui để hiển thị 2 khung ảnh, 1 table theo dõi truyền nhận, 1 box hiện thông tin nhận diện, 2 button thủ công đề phòng sai sót

model weight
https://drive.google.com/file/d/1gdKWeb6EFlpq8sQtu8CTiL1mtHfFtL0Y/view?usp=sharing
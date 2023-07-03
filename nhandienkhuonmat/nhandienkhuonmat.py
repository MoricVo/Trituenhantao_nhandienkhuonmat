import cv2
import numpy as np
import os #Thư vieen dùng để truy cập các thư viện trong máy 
import sqlite3 # Khai báo clds sql lite để truy xuất tới csdl lấy dữ liệu 
from PIL import Image #Truy xuất tới nguồn ảnh đã có

#Training hinh anh nhan dien voi thu vien nhan dien khuon mat
#import cả 2 thư viện 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")#Thư viện nhận diện được khuôn mặt mình
recognizer = cv2.face.LBPHFaceRecognizer_create()#Thao tác traning với khuôn mặt của người dùng

recognizer.read('C:/Users/Jarvi/Desktop/nhandienkhuonmat/nhan_dang/Chay_data.yml')#Đọc được file sinh ra khi đã traning xong xem xét xem tập dữ liệu đã có trên camera chưa

# lay profile cua id tren database
def getProfile(id):#Lấy ra thông tin của người trong csdl 

    conn = sqlite3.connect('C:/Users/Jarvi/Desktop/nhandienkhuonmat/SQLiteStudio/data.db')#Lấy đường dẫn trong csdl
    query = "SELECT * FROM people WHERE ID="+str(id) #Viết hàm query để sectlect các id mình đã truyền vào chuyển về dạng chuổi
    cursor = conn.execute(query) #Thực hiện câu lệnh này

    profile = None #Tạo 1 biến lưu giá trị lấy từ database về

    for row in cursor: #
        profile = row

    conn.close() #Đóng chương trình
    return profile #Return lại biến profile để dùng

cap = cv2.VideoCapture(0)#Truy cập đến camera

fontface = cv2.FONT_HERSHEY_SIMPLEX

while(True):#Sử dụng vòng lặp while 

    ret, frame = cap.read() #Đọc dữ liệu từ camera ret bằng tru frame dữ liệu ảnh

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Màu đã có giải thích

    faces = face_cascade.detectMultiScale(gray) #kết hợp giữa webcam và face_cascade để nhận diện được khuôn mặt mình

    for (x, y, w, h) in faces: # vòng for vẽ hình vuoog trên khuon mặt

        cv2.rectangle(frame, (x, y), (x+w, y+h), (100,10,0), 4) #Bước này sẽ vẽ hình 

        roi_gray = gray[y:y+h , x:x+w]#Cắt ảnh trên camera và so sánh với tập dữ liệu và màu ảnh phải là màu xám


        id,confidence = recognizer.predict(roi_gray)#Sau khi cắt xong để máy nhận diện để nhận diện ta có lệnh recongizer truyền vào
        #ảnh màu xám nếu người ấy có trên tập dữ liệu sẻ hiện thông tin id và độ chính xác với biến confidence

        if confidence < 40:#Nếu độ chính xác nhỏ hơn 40 thì chương trình tiếp tục 
            profile = getProfile(id) #Lấy id được từ hàm kiểm tra nhận diễn ảnh 

            if(profile != None):#Nếu profile có dữ liệu thì trả về dữ liệu đấy còn không thì không biết người đó là ai 
                cv2.putText(frame, ""+str(profile[1]), (x+10, y+h+30), fontface, 1, (100,255,0), 3)
                cv2.putText(frame, "Tuoi: "+str(profile[2]), (x+10, y+h+68), fontface, 1, (100,255,0), 2)
                cv2.putText(frame, "Gioi tinh: "+str(profile[3]), (x+10, y+h+92), fontface, 1, (100,255,0), 2)
            else:#Trả về khi không nhận dạng được 
                cv2.putText(frame, "Unknown" , (x + 10, y + h + 30), fontface, 1, (10, 0, 255), 5)

    cv2.imshow('Image',frame) #Show thông tin hình ảnh khi đã kiểm ra
    if(cv2.waitKey(1) == ord('q')):#Điều kiện để thoát nếu nhấn nút q thì thoát 
        break;



cap.release()#Giải phóng bộ nhớ
cv2.destroyAllWindows() #Hủy chương trình

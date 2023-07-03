import cv2 #Đây là import thư viện open CV
import numpy as np #Numpy 1 thư viện hổ trợ của python giúp chúng ta thao tác với mãng được nhanh hơn và chích xác hơn so với dùng List Table
import sqlite3
import os

def insertOrUpdate(id, name, age, gender): #Hàm def có tham số để truy cập đến các giá trị dữ liệu từ sql server

    conn = sqlite3.connect('C:/Users/Jarvi/Desktop/nhandienkhuonmat/SQLiteStudio/data.db') #Hàm kết nối đến qsl có tham số là chứa đường dẫn chứa các file database

    query = "SELECT * FROM people WHERE ID=" + str(id)#lệnh Kiểm tra xem id đã tồn tại hay chưa nếu tồn tại rồi sẽ update nếu chưa sẽ insect str(id) ép kiểu id thành kiểu chuỗi str==string
    #tức và là có 1 chuỗi id nên ta cần ép kiểu để chứa được dạng số vừa kí tự 
    cusror = conn.execute(query) #biến cussror ta sẽ lấy đc bản ghi từ biến qery 

    isRecordExist = 0 #biến này tạo ra để kiểm tra xem nếu trong database có id rồi thì sẽ gán nó bằng 1 còn nếu chưa thì gán bằng 0 để có thể insect hoặc update  

    for now in cusror: #Duyệt từng hàng trên bản ghi
        isRecordExist = 1 #Nếu có tồn tại thì chuyển về bằng 1

    if(isRecordExist == 0):# kiểm tra nếu chưa có bản ghi nào thì insect vào database
        query = "INSERT INTO people(id, name, age, gender) VALUES("+str(id)+ ",'"+ str(name)+"','"+ str(age)+"','"+ str(gender)+"')" #Tất cả đều ép kiểu về chuỗi
    else:
        query = "UPDATE people SET name= '"+str(name)+"',age= '"+ str(age)+"',gender= '"+ str(gender)+"' WHERE ID="+ str(id) #Cìn nếu không thì phải update dữ liệu lên bắng cách
        #xét lại giá trị cho nó

    conn.execute(query) #Bắt đầu thực thi câu lệnh query
    conn.commit() #Commit nó đi
    conn.close() #Đóng nó 

#load thư viện kiểu mặc định nhận diện của opencv 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") #Đây là thư viện nhận diện khuôn mặt của openCV "haarcascade_frontalface_default.xml"
#đường dẫn

cap = cv2.VideoCapture(0) #Hàm truy cập vào vào webcam(camera) của hệ thống


#insert vào data.db
#Cho người dùng nhập từ bàn phím vào để lưu giá trị sau đó để mình traning cho AI hiểu để khi nhận dạng sẽ hiển thị thông tin đúng chính xác người được nhận diện
id = input("Nhap ID: ")
name = input("Nhap ho ten: ")
age = input("Nhap so tuoi: ")
gender = input("Nhap gioi tinh: ")

insertOrUpdate(id, name, age, gender) #Gọi lại hàm chứa database truyền vào 4 tham số để lưu vào database {0}

sampleNum = 0 #Ví dụ lưu 10 ảnh ta sẽ lưu với thứ tự 1.1 1.2 1.3.. nếu vậy ta sẽ tạo 1 biến sampleNum gán nó khởi tạo=0;

while(True):
    ret, frame = cap.read() #Đọc dữ liệu từ webcam biến đầu tiên ret trả về true nếu truy cập thành công biến frame lấy dữ liệu thành công từ webcam

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Chuyển màu ảnh về thành màu sáng để train frame là dl BGR và viết ngược của màu RGB trong opencv định nghĩa như v

    faces = face_cascade.detectMultiScale(gray, 1.3, 5) #Nhận diện khuôn mặt được vật thể trên webcam truyền vào màu sáng để máy có thể nhận diện 

    for (x, y, w, h) in faces:#Vòng lập tạo vòng khung bao quanh khuôn mặt để nhận diện trên hệ trục tọa độ 
        cv2.rectangle(frame, (x, y), (x+ w, y+ h), (100,10,0), 4)#Hàm này giúp vẽ được hình vuông bao quan khuôn mặt tham số đầu frame lấy dữ liệu khuôn mặt x và y tọa độ điểm để vẽ
        # lên hình vuông  (x+ w, y+ h) tọa độ tịnh tiến trong không gian  (100,10,0) tham số màu rgb màu xanh  4 ddojoj dày của khung 

        if not os.path.exists('hinhanh'):#Bước này ta sẻ tạo folder để lưu ảnh mình cắt được chứa trong folder đó,if not os.path.exists('hinhanh')
            #Kiểm tra xem đường dẫn có folder chưa để tạo folder
            os.makedirs('hinhanh')#Nếu chưa ta sẻ truyền vào lệnh makedirs tạo folder mới

        sampleNum +=1 #{1} Ta tiến hành cộng dồn khi nhảy xuống vòng lặp for nó sẽ chạy cho đến khi hết ảnh thì thôi

        cv2.imwrite('hinhanh/User.'+str(id)+'.'+str(sampleNum)+ '.jpg', gray[y: y+ h, x: x+ w]) #Lệnh lưu ảnh hay ghi cv2.imwrite('hinhanh/User.'+str(id)+'.'+str(sampleNum)+ '.jpg'
        #đường dẫn lưu đến thư mục (hinhanh/User.'+str(id)+'.'+str(sampleNum)==User.1.1) cắt theo hình vuông y+ h x+ w

    cv2.imshow('frame',frame) #frame là tiêu đề của ảnh frame2 là dữ liệu hình ảnh
    cv2.waitKey(1) #Kết thúc chương trình

    if sampleNum > 100: #Nếu tải quá 288 hình ảnh thì tự động dừng chụp
        break; #Nếu lớn hơn 100 ảnh thì dừng
cap.release()#Giải phóng bộ nhớ
cv2.destroyAllWindows() #Hủy kết thúc chương trfinh


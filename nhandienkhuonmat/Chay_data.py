import cv2
import numpy as np
import os #Truy cấp vào hệ dẫn hay còn gọi truy cập vào đường dẫn trong máy 
from PIL import Image #Import để trích xuất được ảnh khi tạo ảnh xong

recognizer = cv2.face.LBPHFaceRecognizer_create() #import thư viện viện mặc định của opencv để traning hình ảnh nhận diện

path = 'hinhanh' #biến lấy đường dẫn lấy đến thư mục ảnh

def getImageWithID(path): #Hàm lấy ra được id và 1 list dữ liệu ảnh để tiến hành traning

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)] #Lấy tất cả các ảnh từ đường dẫn của ảnh, imagePaths lưu các đường dẫn,for f in os.listdir(path)truy cập tất cả
    #các file ảnh trong đường dẫn

    #print(imagePaths)

    faces = [] #Tạo 1 mãng face để lưu dữ liệu ảnh
    IDs = [] # lưu id

    for imagePath in imagePaths:#Dùng for duyệt tất cả cac đường dẫn 

        faceImg = Image.open(imagePath).convert('L')  #Truy xuất tất cả các ảnh ra và convert nó về dạng ảnh PIL để thao tác với mảng và tiến hành traning  Image.open(imagePath).convert('L')
        #Mở ảnh đưa về đúng định dạng

        faceNp = np.array(faceImg, 'uint8') #Khi đã có faceimge sao đó ta đưa nó về dạng mảng đến train tất cả các ảnh có trong 1 mảng,np mảng numpi

        print(faceNp) #In ra ma trận các điểm ảnh

        #Cắt để lấy ID của hình ảnh

        Id = int(os.path.split(imagePath)[-1].split('.')[1]) #Lấy ra id để cho máy hiểu ảnh thuộc id nào đẻ train nhưng ta phải ép kieu về int
        #os.path.split(imagePath)[-1].split('.')[1] cắt id 
    

        faces.append(faceNp) #Sau khi mà lấy đc dữ liệu ảnh thì add vào mảng 
        IDs.append(Id)  #Tương tự ở trên

        cv2.imshow('Chay data ', faceNp) # 
        cv2.waitKey(10)

    return faces, IDs #trả về lại 2 mảng id và imge 


faces, IDs = getImageWithID(path) #Lưu lại 2 mãng đó

#hoạt động - train hoạt động với 2 tham số
recognizer.train(faces, np.array(IDs))
#Sau khi train xong nó sẻ trả về 1 file ta cần lưu file 
#lưu vào file
if not os.path.exists('nhan_dang'):#Nếu chưa có file
    os.makedirs('nhan_dang') #Tiến hành tạo file

recognizer.save('nhan_dang/Chay_Data.yml') #Lưu file 

cv2.destroyAllWindows()#Đóng chườn trình 

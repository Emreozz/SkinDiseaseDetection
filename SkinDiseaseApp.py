from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import mysql.connector
import cv2
import numpy as np
from datetime import datetime
from keras.models import load_model



class LoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        title_label = QLabel("Tektik Sistemi", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")
        title_label.setFont(QFont("Arial", 28))
        title_label.setFixedSize(300, 60)
        title_label.move(int((self.width() - title_label.width()) / 2) + 250, 30)

        # Kullanıcı adı giriş kutusu
        username_label = QLabel("Kullanıcı Adı:", self)
        username_label.setFont(QFont("Arial", 16))
        username_label.setStyleSheet("color: white;")
        username_label.move(150, 120)

        self.username_edit = QLineEdit(self)
        self.username_edit.setFont(QFont("Arial", 14))
        self.username_edit.setFixedSize(300, 40)
        self.username_edit.move(150, 150)

        # Parola giriş kutusu
        password_label = QLabel("Parola:", self)
        password_label.setFont(QFont("Arial", 16))
        password_label.setStyleSheet("color: white;")
        password_label.move(150, 210)

        self.password_edit = QLineEdit(self)
        self.password_edit.setFont(QFont("Arial", 14))
        self.password_edit.setFixedSize(300, 40)
        self.password_edit.move(150, 240)
        self.password_edit.setEchoMode(QLineEdit.Password)

        # Giriş düğmesi
        login_button = QPushButton("Giriş Yap", self)
        login_button.setFont(QFont("Arial", 16))
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                border-radius: 20px;
                color: #ECF0F1;
                border: 2px solid #3498DB;
                padding: 5px 20px;
                outline: none;
            }
            QPushButton:hover {
                background-color: #2980B9;
                border: 2px solid #2980B9;
            }
            QPushButton:pressed {
                background-color: #21618C;
                border: 2px solid #21618C;
            }
        """)
        login_button.setFixedSize(200, 50)
        login_button.move(int((self.width() - login_button.width()) / 2) + 250, 320)
        login_button.clicked.connect(self.login)
        register_button = QPushButton("Kayıt Ol", self)
        register_button.setFont(QFont("Arial", 16))
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                border-radius: 20px;
                color: #ECF0F1;
                border: 2px solid #27AE60;
                padding: 5px 20px;
                outline: none;
            }
            QPushButton:hover {
                background-color: #229954;
                border: 2px solid #229954;
            }
            QPushButton:pressed {
                background-color: #1E8449;
                border: 2px solid #1E8449;
            }
        """)
        register_button.setFixedSize(200, 50)
        register_button.move(int((self.width() - login_button.width()) / 2) + 250, 380)
        register_button.clicked.connect(self.register)
        
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin123',
            database='mydatabase88'
        )
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users1 (
                username_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255),
                password VARCHAR(255)
                
            )''')  # Şifre sütunu eklendi

# Hastalıklar tablosunu oluştur
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS diseases (
        disease_id INT AUTO_INCREMENT PRIMARY KEY,
        username_id INT,
        disease_name VARCHAR(255),
        time VARCHAR(255),
        Percentage_of_disease VARCHAR(255),
        result VARCHAR(255),
        FOREIGN KEY (username_id) REFERENCES users1(username_id)
    )''')

          # Resim eklemek için QLabel oluşturun
        image_label = QLabel(self)
        image_label.setPixmap(QPixmap("WhatsApp Image 2023-06-08 at 20.03.32 (1).jpeg"))  # Resmin dosya yolunu buraya ekleyin
        image_label.setScaledContents(True)
        screen_geometry = QApplication.desktop().screenGeometry()
        
        
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        image_label.setFixedHeight(screen_height)

        # Resmi en sağa ve en alta yerleştir
        image_label.move(screen_width - image_label.width()-600, screen_height - image_label.height())

        # Resmi ekrana ekleyin
        image_label.show()
        

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Başlık etiketi için arka plan rengi
        title_rect = QRect(0, 0, self.width(), 100)
        painter.setBrush(QBrush(QColor("black")))
        painter.setPen(QPen(QColor("white"), 2))  # Beyaz kenarlık rengi ve genişliği
        painter.drawRect(title_rect)

        # Diğer arka plan rengi
        body_rect = QRect(0, 100, self.width(), self.height() - 100)
        gradient = QLinearGradient(body_rect.topLeft(), body_rect.bottomLeft())
        gradient.setColorAt(0, QColor("mavi")) 
        gradient.setColorAt(1, QColor("#000080"))  

        painter.setBrush(QBrush(gradient))
        painter.drawRect(body_rect)


    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        username_query = "SELECT username_id FROM users1 WHERE username = %s"
        self.cursor.execute(username_query, (self.username_edit.text(),))
        self.username_id = self.cursor.fetchone()[0]  
        print(self.username_id)

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM  users1  WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()

        if result:
            print("Giriş yapıldı.")
            
            self.parent.setCurrentIndex(2)
        else:
            print("Kullanıcı adı veya parola yanlış.")
            self.show_notification("Yanlış giriş!")

    def show_notification(self, message):
    
        # Bildirim mesajı için QLabel oluştur
        notification_label = QLabel(message, self)
        notification_label.setFont(QFont("Arial", 16))

        # Arka plan için gradyan oluştur
        gradient = QLinearGradient(0, 0, 0, 30)
        gradient.setColorAt(0, QColor("#FF0000"))  # Başlangıç rengi kırmızı
        gradient.setColorAt(1, QColor("#800000"))  # Bitiş rengi koyu kırmızı

        palette = QPalette()
        palette.setBrush(QPalette.Background, gradient)
        notification_label.setAutoFillBackground(True)
        notification_label.setPalette(palette)

        notification_label.setAlignment(Qt.AlignCenter)
        notification_label.setFixedSize(300, 60)  # Yükseklik ve genişlik ayarlandı

        screen_geometry = QApplication.desktop().screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        notification_x = int((screen_width - notification_label.width()) / 2 -680)  # Ekran genişliğinin ortasına yerleştirme
        notification_y = int((screen_height - notification_label.height()) /2 +320)  # Ekran yüksekliğinin ortasına yerleştirme

        notification_label.move(notification_x, notification_y)

        # Bildirimi otomatik olarak kaldırmak için QTimer kullan
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(notification_label.deleteLater)
        timer.start(3000)  # 3 saniye sonra bildirimi kaldır

        # Bildirimi görünür hale getir
        notification_label.show()

    def register(self):
        self.parent.setCurrentIndex(1)


class RegisterScreen(QWidget):
    
    def __init__(self, parent ):
        super().__init__(parent)
        self.parent = parent
        self.connection = LoginScreen().connection


        

        # Başlık etiketi
        title_label = QLabel("Kayıt Sistemi", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24))
        title_label.setFixedSize(300, 60)
        title_label.move(int((self.width() - title_label.width()) / 2)+150, 40)

        # Kullanıcı adı giriş kutusu
        username_label = QLabel("Kullanıcı Adı:", self)
        username_label.setFont(QFont("Arial", 16))
        username_label.setStyleSheet("color: black;")
        username_label.move(50, 120)

        self.username_edit = QLineEdit(self)
        self.username_edit.setFont(QFont("Arial", 14))
        self.username_edit.setFixedSize(300, 40)
        self.username_edit.move(50, 150)

        # Parola giriş kutusu
        password_label = QLabel("Parola:", self)
        password_label.setFont(QFont("Arial", 16))
        password_label.setStyleSheet("color: black;")
        password_label.move(50, 210)

        self.password_edit = QLineEdit(self)
        self.password_edit.setFont(QFont("Arial", 14))
        self.password_edit.setFixedSize(300, 40)
        self.password_edit.move(50, 240)
        self.password_edit.setEchoMode(QLineEdit.Password)

        # Kayıt düğmesi
        register_button = QPushButton("Kayıt Ol", self)
        register_button.setFont(QFont("Arial", 16))
        register_button.setStyleSheet("""
            QPushButton {
                background-color: blue;
                border-radius: 20px;
                color: #ECF0F1;
                border: 2px solid #27AE60;
                padding: 5px 20px;
                outline: none;
            }
            QPushButton:hover {
                background-color: #229954;
                border: 2px solid #229954;
            }
            QPushButton:pressed {
                background-color: #1E8449;
                border: 2px solid #1E8449;
            }
        """)
        register_button.setFixedSize(200, 50)
        register_button.move(int((self.width() - register_button.width()) / 2)+150, 320)
        register_button.clicked.connect(self.register_to_sql)
        
        back_button = QPushButton("Giriş Sayfasına Dön", self)
        back_button.setFont(QFont("Arial", 16))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #34495E;
                border-radius: 20px;
                color: #ECF0F1;
                border: 2px solid #34495E;
                padding: 5px 20px;
                outline: none;
            }
            QPushButton:hover {
                background-color: #2C3E50;
                border: 2px solid #2C3E50;
            }
            QPushButton:pressed {
                background-color: #2C3E50;
                border: 2px solid #2C3E50;
            }
        """)
        back_button.clicked.connect(self.return_login_page)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#16A085"))
        gradient.setColorAt(1, QColor("#27AE60"))

        painter.fillRect(self.rect(), gradient)

    def register_to_sql(self):
        
        username = self.username_edit.text()
        password = self.password_edit.text()

        cursor = self.connection.cursor()
           
        cursor.execute("SELECT username, password FROM users1 WHERE username=%s AND password=%s", (username, password))

        # Sorgu sonuçları okunuyor
        result = cursor.fetchone()

        # Sorgu sonucu boş değilse, kullanıcı zaten kayıtlı demektir.
        if result:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı zaten kayıtlı!")
        else:
            cursor.execute("INSERT INTO users1 (username, password) VALUES (%s, %s)", (username, password))
            self.connection.commit()
            QMessageBox.information(self, "Başarılı", "Kayıt başarılı!")
            
    def return_login_page(self):
        self.parent.setCurrentIndex(0)
        



class Options(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        
        
        
        
    

        self.loaded_model = load_model("final.h5",compile=False) # Modeli yükle
        self.loaded_model.compile()

        self.classes = { 'akiec': 'Actinic keratoses',
            'bcc': 'Basal cell carcinoma',
            'bkl': 'Benign keratosis-like lesions ',
            'df': 'Dermatofibroma',
            'mel': 'Melanoma',  
            'nv': 'Melanocytic nevi',
            'vasc': 'Vascular lesions'
            }
       
        self.select_image_btn = QPushButton("Resim Seç", self)
        self.select_image_btn.setStyleSheet(
            "QPushButton {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 255, 0, 255), stop:1 rgba(0, 128, 0, 255));"  # Gradyan yeşil arka plan rengi
            "   border: 2px solid black;"
            "   color: white;"
            "   border-radius: 10px;"  # Köşelerin daha fazla yuvarlatılması
            "   padding: 10px;"
            "   font-weight: bold;"
            "   text-transform: uppercase;"
            "   text-decoration: none;"
            "   outline: none;"
            "   transition: background-color 0.3s, color 0.3s;"
            "}"
            "QPushButton:hover {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 255, 0, 255), stop:1 rgba(0, 100, 0, 255));"  # Daha koyu yeşil arka plan rengi (hover durumunda)
            "   color: black;"
            "}"
            "QPushButton:pressed {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 200, 0, 255), stop:1 rgba(0, 80, 0, 255));"  # Daha koyu yeşil arka plan rengi (basıldığında)
            "}"
        )
        
        
        self.camera_btn = QPushButton("Connect to camera")
        self.camera_btn.setStyleSheet(
            "QPushButton {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 255, 0, 255), stop:1 rgba(0, 128, 0, 255));"  # Gradyan yeşil arka plan rengi
            "   border: 2px solid black;"
            "   color: white;"
            "   border-radius: 10px;"  # Köşelerin daha fazla yuvarlatılması
            "   padding: 10px;"
            "   font-weight: bold;"
            "   text-transform: uppercase;"
            "   text-decoration: none;"
            "   outline: none;"
            "   transition: background-color 0.3s, color 0.3s;"
            "}"
            "QPushButton:hover {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 255, 0, 255), stop:1 rgba(0, 100, 0, 255));"  # Daha koyu yeşil arka plan rengi (hover durumunda)
            "   color: black;"
            "}"
            "QPushButton:pressed {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 200, 0, 255), stop:1 rgba(0, 80, 0, 255));"  # Daha koyu yeşil arka plan rengi (basıldığında)
            "}"
        )
        self.results_btn = QPushButton("View results")
        self.results_btn.setStyleSheet(
            "QPushButton {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 255, 0, 255), stop:1 rgba(0, 128, 0, 255));"  # Gradyan yeşil arka plan rengi
            "   border: 2px solid black;"
            "   color: white;"
            "   border-radius: 10px;"  # Köşelerin daha fazla yuvarlatılması
            "   padding: 10px;"
            "   font-weight: bold;"
            "   text-transform: uppercase;"
            "   text-decoration: none;"
            "   outline: none;"
            "   transition: background-color 0.3s, color 0.3s;"
            "}"
            "QPushButton:hover {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 255, 0, 255), stop:1 rgba(0, 100, 0, 255));"  # Daha koyu yeşil arka plan rengi (hover durumunda)
            "   color: black;"
            "}"
            "QPushButton:pressed {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 200, 0, 255), stop:1 rgba(0, 80, 0, 255));"  # Daha koyu yeşil arka plan rengi (basıldığında)
            "}"
        )
        self.content_lbl = QLabel()
        
        
        
        
        self.capture_btn = QPushButton("Capture")
        self.capture_btn.setStyleSheet(
            "QPushButton {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 255, 0, 255), stop:1 rgba(0, 128, 0, 255));"  # Gradyan yeşil arka plan rengi
            "   border: 2px solid black;"
            "   color: white;"
            "   border-radius: 10px;"  # Köşelerin daha fazla yuvarlatılması
            "   padding: 10px;"
            "   font-weight: bold;"
            "   text-transform: uppercase;"
            "   text-decoration: none;"
            "   outline: none;"
            "   transition: background-color 0.3s, color 0.3s;"
            "}"
            "QPushButton:hover {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 255, 0, 255), stop:1 rgba(0, 100, 0, 255));"  # Daha koyu yeşil arka plan rengi (hover durumunda)
            "   color: black;"
            "}"
            "QPushButton:pressed {"
            "   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(0, 200, 0, 255), stop:1 rgba(0, 80, 0, 255));"  # Daha koyu yeşil arka plan rengi (basıldığında)
            "}"
        )
        self.capture_btn.hide() 
        self.sidebar_widget = QWidget()
        
        
        

        

        # Create layout for sidebar widget and add search bar
        sidebar_layout = QVBoxLayout()
        
        sidebar_layout.addWidget(self.camera_btn)
        sidebar_layout.addWidget(self.capture_btn)
        sidebar_layout.addWidget(self.results_btn)
        sidebar_layout.addWidget(self.select_image_btn)
        sidebar_layout.addStretch(1)

        self.sidebar_widget.setLayout(sidebar_layout)
        
        
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Bir şeyler yazın...")
        search_bar.setAlignment(Qt.AlignCenter)
        search_bar.setStyleSheet("QLineEdit {"
        "border: 2px solid #4A90E2;"
        "padding: 8px;"
        "background-color: #000080;"
        "color: #FFFFFF;"
        "font-size: 16px;"
        "}")

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.sidebar_widget, 0, 0, 2, 1)  # Sidebar widget'ı 0-1. satırlar, 0. sütuna yerleştir
        self.main_layout.addWidget(search_bar, 0, 1, 1, 2)  # Search bar'ı 0. satır, 1-2. sütunlara yerleştir
        self.main_layout.addWidget(self.content_lbl, 1, 1, 1, 1)  # Content layout'ı 1. satır, 1. sütuna yerleştir
        self.content_lbl.setAlignment(Qt.AlignRight)

        self.main_layout.setColumnStretch(1, 4)

        self.setLayout(self.main_layout)
        
        self.camera_btn.clicked.connect(self.connect_to_camera)
        self.capture_btn.clicked.connect(self.capture_image)
        self.results_btn.clicked.connect(self.view_results)
        self.select_image_btn.clicked.connect(self.select_image)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_camera)
        self.sidebar_visible = True  # Keep track of sidebar visibility
        self.set_sidebar_gradient()
        search_bar.textChanged.connect(self.search_content)
        
            

    def paintEvent1(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        # Draw custom regions
        painter.setBrush(QColor(0, 0, 255))  # Blue color
        painter.drawRect(9, 0, 160, 50)  # Widget's top region

    def set_sidebar_gradient(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(0, 0, 128))  # Arka plan rengi: Koyu Mavi (#000080)
        
        self.sidebar_widget.setAutoFillBackground(True)
        self.sidebar_widget.setPalette(palette)

    def select_image(self):
        self.disconnect_from_camera()
        
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Resim Dosyaları (*.png *.jpg *.jpeg)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_files = file_dialog.selectedFiles()
            for file_path in selected_files:
                pixmap = QPixmap(file_path)
                print(file_path)
                # qimage = pixmap.toImage()
                # width = qimage.width()
                # height = qimage.height()
                # bytes_per_line = qimage.bytesPerLine()
                # image_data = qimage.constBits().asarray(height * bytes_per_line)

                # # QImage'ı NumPy dizisine dönüştürme
                # frame = np.array(image_data, dtype=np.uint8).reshape(height, width, 4)
                frame = cv2.imread('{}'.format(file_path))
                frame = cv2.resize(frame, (224, 224))
                # OpenCV'nin frame tipine dönüştürme
                # frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
                
                self.content_lbl.setPixmap(pixmap)
                self.content_lbl.setScaledContents(True)
                # Convert QPixmap to QImage to pass to the predict method
                
                self.predict1(frame)
        else:
            # Dosya seçimini iptal ettiğinde fonksiyonu sonlandır
            return
        
    

    def toggle_camera(self):
        if self.camera_connected:
            self.disconnect_from_camera()  # Kamera bağlantısını kes
        else:
            self.connect_to_camera()  # Kameraya bağlan

    

    def disconnect_from_camera(self):
        if self.cap is not None:
            self.cap.release()  # Kameradan bağlantıyı kes
            self.cap = None

        self.timer.stop()  # Timer'ı durdur
        self.content_lbl.clear()  # Kamera görüntüsünü temizle
        self.capture_btn.hide()  # Capture düğmesini gizle
        self.camera_connected = False  # Kamera bağlantısı durumunu güncelle

    def connect_to_camera(self):
        if self.capture_btn.isVisible():
            self.timer.stop()  # Stop the timer to update camera image
            self.cap.release()  # Disconnect from the camera
            self.cap = None
            self.capture_btn.hide()  # Hide the capture button
        else:
            if self.cap is None:
                self.cap = cv2.VideoCapture(0)  # Connect to camera

            if not self.timer.isActive():
                self.timer.start(50)  # Start timer to update camera image

            self.capture_btn.show()  # Show the capture button

        
    def update_camera(self):
        
        ret, frame = self.cap.read()  # Read camera image

        if ret:
            # Transfer the captured frame to self.camera_lbl
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)

            if self.content_lbl is not None:
                self.content_lbl.setPixmap(pixmap.scaled(self.content_lbl.size(), Qt.KeepAspectRatio))
                self.content_lbl.setScaledContents(True)
            
    def capture_image(self):

        ret, frame = self.cap.read()  
        if ret:
            self.predict1(frame)
            
             
            
    def predict1(self, image):
        # img = cv2.resize(image, (224, 224))
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Gerekli renk formatı dönüşümü
        self.login = LoginScreen()
        self.connection = self.login.connection

        result = self.loaded_model.predict(image.reshape(1, 224, 224, 3))
        max_prob = max(result[0])
        print(result[0], max_prob)
        threshold = max_prob*100
        if threshold > 10:
             result_disease = "doktora gitmelisiniz"
        else:
             result_disease = "doktora gitmenize gerek yok"

        class_ind = list(result[0]).index(max_prob)
        class_name = list(self.classes)[class_ind]
        print(class_name)
        self.cursor = self.connection.cursor()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        username_id = self.login.username_id 

        
        insert_query = "INSERT INTO diseases (username_id, disease_name,time,percentage_of_disease,result) VALUES (%s, %s,%s, %s,%s)"
        self.cursor.execute(insert_query, (username_id, class_name,current_time,threshold,result_disease))

        self.connection.commit()
        

    def view_results(self):
        self.login = LoginScreen().login().username
        self.connection = self.login.connection
        self.disconnect_from_camera()
        username_id = self.login.login().user
        

        query = "SELECT disease_name,time,percentage_of_disease,result FROM diseases WHERE username_id = %s"
        self.cursor =self.connection.cursor()
        


        # SQL sorgusunu çalıştır
        self.cursor.execute(query, (username_id,))

        # Sonuçları al
        results = self.cursor.fetchall()

        # Sonuçları "content_lbl" etiketiyle ekrana yazdır
        content = ""
        for row in results:
            print(row)
            content += f"Username ID: {username_id} Disease Name: {row[0]} Time: {row[1]} Percentage: {row[2]} Result: {row[3]}\n\n"
        # Stil uygula ve font boyutunu ve rengini ayarla
        
        content_style = "QLabel { font-size: 40px; color: #000080; text-align: left; }"
        self.content_lbl.setStyleSheet(content_style)
        self.content_lbl.setText(content)

    
    def search_content(self, text):
        # content_lbl'deki metni al
        content_text = self.content_lbl.text()

        # Aranan kelimeyi metinde ara ve güncellemeleri yap
        filtered_text = ""

        if text:
            lines = content_text.split("\n")
            filtered_lines = [line for line in lines if text.lower() in line.lower()]
            filtered_text = "\n".join(filtered_lines)

        # filtered_text'i kullanarak content_lbl'yi güncelle
        if filtered_text:
            self.content_lbl.setText(filtered_text)
        else:
            self.content_lbl.setText(content_text)

app = QApplication(sys.argv)
window = QStackedWidget()
login_screen = LoginScreen(window)
register_screen = RegisterScreen(window)
options_screen = Options(window)
window.addWidget(login_screen)
window.addWidget(register_screen)
window.addWidget(options_screen)

window.showMaximized()
sys.exit(app.exec_())
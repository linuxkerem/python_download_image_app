from PyQt5 import QtWidgets
import sys
import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from selenium.webdriver import Keys
import time

from selenium.webdriver.common.by import By

from wallpaperform import Ui_MainWindow
from selenium import webdriver


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.open_button.clicked.connect(self.dosyaac)
        self.ui.start_button.clicked.connect(self.start)
    def dosyaac(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, "Choose Directory", "E:\\")
        self.ui.path_text.setText(self.dir_path)

    def start(self):
        QMessageBox.information(self,"Bilgilendirme","Lütfen işlem bitti yazısı çıkana kadar program ile etkileşim kurmayınız")
        if self.ui.wallp_text.text()=="":
            QMessageBox.critical(self, "Hata", "Kelime yazılmadan işlem başlatılamaz")
        else:
            current_path = os.path.dirname(os.path.abspath(__file__))
            current_path = current_path.replace("\\", "\\\\")
            query = self.ui.wallp_text.text()
            path = self.ui.path_text.text()
            if path=="":
                path = current_path
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--headless")
            driver = webdriver.Chrome(current_path+ "\chromedriver.exe", options=chromeOptions)
            driver.maximize_window()
            driver.get('https://images.google.com/')
            box = driver.find_element(By.XPATH, '//*[@id="sbtc"]/div/div[2]/input')
            box.send_keys(query)
            box.send_keys(Keys.ENTER)

            def scroll_to_bottom():
                last_height = driver.execute_script('\
                return document.body.scrollHeight')
                while True:
                    driver.execute_script('\
                    window.scrollTo(0,document.body.scrollHeight)')
                    time.sleep(3)
                    new_height = driver.execute_script('\
                    return document.body.scrollHeight')
                    try:
                        driver.find_element(By.CSS_SELECTOR, ".YstHxe input").click()
                        time.sleep(3)
                    except:
                        pass
                    if new_height == last_height:
                        break
                    last_height = new_height

            scroll_to_bottom()
            adet = self.ui.count_sayac.text()
            for i in range(1, int(adet)+1):
                try:
                    img = driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img')
                    img.screenshot(str(path) + query + ' (' + str(i) + ').png')
                    time.sleep(0.2)
                except:
                    continue
            driver.close()
            self.ui.result_label.setText("İşlem başarı ile tamamlandı.")
            if self.ui.path_text.text()=="":
                QMessageBox.about(self,"Dikkat","Konum belirtilmediği için görseller klasörün içerisine kaydedildi.")
            QMessageBox.information(self, "Son", "İşlem başarıyla tamamlandı")


app = QtWidgets.QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())

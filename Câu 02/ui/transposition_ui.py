import sys
import requests
from PyQt5 import QtWidgets, uic

class TranspositionUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(TranspositionUI, self).__init__()
        
        # Load trực tiếp file UI bằng tên (Không dùng đường dẫn phức tạp)
        uic.loadUi('transposition.ui', self)
        
        # URL của API Flask đang chạy ngầm
        self.api_url = "http://127.0.0.1:5000/api/transposition"
        
        # Kết nối sự kiện nút bấm (Đảm bảo trong Qt Designer bạn đã đặt đúng các tên này)
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_decrypt.clicked.connect(self.handle_decrypt)

    def handle_encrypt(self):
        plain_text = self.txt_plain.toPlainText()
        key = 8 # Khóa hoán vị (Tạm thời cố định là 8)
        
        if not plain_text:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản cần mã hóa!")
            return

        try:
            payload = {"plain_text": plain_text, "key": key}
            response = requests.post(f"{self.api_url}/encrypt", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                self.txt_cipher.setPlainText(result.get('encrypted_text', ''))
            else:
                QtWidgets.QMessageBox.critical(self, "Lỗi API", "Không thể xử lý mã hóa.")
        except requests.exceptions.ConnectionError:
            QtWidgets.QMessageBox.critical(self, "Lỗi kết nối", "Vui lòng bật Server API (api.py) trước!")

    def handle_decrypt(self):
        cipher_text = self.txt_cipher.toPlainText()
        key = 8 # Khóa hoán vị
        
        if not cipher_text:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản cần giải mã!")
            return

        try:
            payload = {"cipher_text": cipher_text, "key": key}
            response = requests.post(f"{self.api_url}/decrypt", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                self.txt_plain.setPlainText(result.get('decrypted_text', ''))
            else:
                QtWidgets.QMessageBox.critical(self, "Lỗi API", "Không thể xử lý giải mã.")
        except requests.exceptions.ConnectionError:
            QtWidgets.QMessageBox.critical(self, "Lỗi kết nối", "Vui lòng bật Server API (api.py) trước!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TranspositionUI()
    window.show()
    sys.exit(app.exec_())
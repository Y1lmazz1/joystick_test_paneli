import sys
import pygame
import math
import os # Klasör yolları için eklendi
from PyQt6 import QtWidgets, uic, QtCore

class JWinTester(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("tasarim.ui", self) 
        
        # --- GÖRSEL KLASÖRÜ TANIMLAMA ---
        self.img_path = "img" # Görsellerin olduğu klasör adı
        
        pygame.init()
        pygame.joystick.init()
        self.j = None
        self.fps_counter = 0

        # Map içindeki isimleri klasör yoluyla birleştiriyoruz
        self.button_map = {
            "btn_0": "x", "btn_1": "a", "btn_2": "b", "btn_3": "y",
            "btn_optins": "playstation4_button_options",
            "btn_start": "playstation3_button_start"
        }
        
        self.trigger_map = {
            "btn_4": "playstation_trigger_l1_alternative",
            "btn_5": "playstation_trigger_r1_alternative",
            "btn_6": "playstation_trigger_l2",
            "btn_7": "playstation_trigger_r2"
        }

        # Dosya isimlerini güncelledik (Klasör yapısına uygun)
        self.stick_img = os.path.join(self.img_path, "pngwing.com (5) (0_0).png")
        self.dpad_off = os.path.join(self.img_path, "pngwing.com (5) (0_0).png")
        self.dpad_on = os.path.join(self.img_path, "pngwing.com (5) (1_0).png")

        if not hasattr(self, "info_label"):
            self.info_label = QtWidgets.QLabel(self)
            self.info_label.setGeometry(0, 520, 800, 60) 
            self.info_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.setup_ui_visuals()
        self.find_joystick()

        for stick_name in ["stick_L", "stick_r"]:
            if hasattr(self, stick_name):
                obj = getattr(self, stick_name)
                obj.raise_() 
                obj.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.origin_L = QtCore.QPoint(0,0)
        self.origin_R = QtCore.QPoint(0,0)
        QtCore.QTimer.singleShot(1000, self.save_origins)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(10)

    # --- YARDIMCI METOD: Dosya yolunu oluşturur ---
    def get_img_url(self, filename):
        return os.path.join(self.img_path, filename).replace("\\", "/")

    def setup_ui_visuals(self):
        self.setStyleSheet("background-color: #121212;")
        for widget in self.findChildren((QtWidgets.QPushButton, QtWidgets.QLabel)):
            if widget.objectName() not in ["label", "base_L", "base_R", "info_label", "conn_status"]:
                widget.setText("")
                widget.setStyleSheet("background: transparent; border: none; outline: none;")
                widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.info_label.raise_()
        self.info_label.setStyleSheet("color: #FFFF00; font-family: 'Segoe UI'; font-size: 14px; font-weight: bold; background: transparent;")
        
        if hasattr(self, "conn_status"):
            # Bağlı değilken: Kırmızı
            self.conn_status.setStyleSheet("background: transparent; border: 3px solid #FF0000; border-radius: 40px;")

    def update_ui(self):
        pygame.event.pump()
        if self.fps_counter % 60 == 0:
            self.find_joystick()
        self.fps_counter += 1

        if not self.j:
            return

        for i in range(min(self.j.get_numbuttons(), 14)):
            name = f"btn_{i}"
            if i == 8: name = "btn_optins"
            if i == 9: name = "btn_start"
            if hasattr(self, name):
                pressed = self.j.get_button(i)
                btn_widget = getattr(self, name)
                
                if name in self.button_map:
                    state = "on" if pressed else "off"
                    if "button" in self.button_map[name]:
                        filename = f"{self.button_map[name]}{'.png' if pressed else '_outline.png'}"
                    else:
                        filename = f"{self.button_map[name]}_{state}.png.png"
                    
                    full_path = self.get_img_url(filename)
                    btn_widget.setStyleSheet(f"border-image: url('{full_path}'); background: transparent;")
                
                elif name in self.trigger_map:
                    filename = f"{self.trigger_map[name]}{'.png' if pressed else '_outline.png'}"
                    full_path = self.get_img_url(filename)
                    btn_widget.setStyleSheet(f"border-image: url('{full_path}'); background: transparent;")

        if self.j.get_numhats() > 0:
            hat = self.j.get_hat(0)
            dirs = {"btn_up": hat[1]==1, "btn_down": hat[1]==-1, "btn_left": hat[0]==-1, "btn_right": hat[0]==1}
            for d_name, is_on in dirs.items():
                if hasattr(self, d_name):
                    img_file = self.dpad_on if is_on else self.dpad_off
                    # Dpad yolları zaten joinlenmiş geliyor, sadece slashta düzenleme gerekebilir
                    getattr(self, d_name).setStyleSheet(f"border-image: url('{img_file.replace('\\','/')}'); background: transparent;")

        # ... (Joystick eksen kodları aynı kalıyor)
        num_axes = self.j.get_numaxes()
        lx, ly = self.j.get_axis(0), self.j.get_axis(1)
        if num_axes >= 6: rx, ry = self.j.get_axis(2), self.j.get_axis(5)
        elif num_axes >= 4: rx, ry = self.j.get_axis(3), self.j.get_axis(4)
        else: rx, ry = 0, 0
        
        limit = 35
        if hasattr(self, "stick_L") and not self.origin_L.isNull():
            cx, cy = self.get_circular_pos(lx, ly, limit)
            self.stick_L.move(self.origin_L.x() + cx, self.origin_L.y() + cy)
        if hasattr(self, "stick_r") and not self.origin_R.isNull():
            cxr, cyr = self.get_circular_pos(rx, ry, limit)
            self.stick_r.move(self.origin_R.x() + cxr, self.origin_R.y() + cyr)

    def find_joystick(self):
        pygame.joystick.quit()
        pygame.joystick.init()
        count = pygame.joystick.get_count()
        if count > 0:
            if self.j is None or pygame.joystick.get_count() > 0:
                self.j = pygame.joystick.Joystick(0)
                self.j.init()
            self.info_label.setText(f"DURUM: BAĞLANDI ✅ | CİHAZ: {self.j.get_name()}")
            if hasattr(self, "conn_status"):
                self.conn_status.setStyleSheet("background: transparent; border: 3px solid #00FF00; border-radius: 40px;")
        else:
            self.j = None
            self.info_label.setText("DURUM: CİHAZ BULUNAMADI ❌")
            if hasattr(self, "conn_status"):
                self.conn_status.setStyleSheet("background: transparent; border: 3px solid #FF0000; border-radius: 40px;")

    def get_circular_pos(self, x, y, limit):
        mag = math.sqrt(x*x + y*y)
        if mag < 0.12: return 0, 0
        if mag > 1.0: x, y = x/mag, y/mag
        return int(x * limit), int(y * limit)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = JWinTester()
    win.show()
    sys.exit(app.exec())
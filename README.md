🎮 Joystick Test Paneli

Bu proje, Python ve PyQt6 kullanılarak geliştirilmiş, oyun kollarını (joystick/gamepad) gerçek zamanlı olarak test etmenizi sağlayan görsel bir arayüzdür.

🚀 Özellikler

* **Gerçek Zamanlı Takip:** Tuş basışlarını ve analog hareketlerini anlık olarak izleyin.
* **Bağlantı Durumu Göstergesi:** * Cihaz bağlıyken: **Yeşil** yanan sinyal halkaları. ✅
  * Cihaz koptuğunda: **Kırmızı** yanan uyarı halkaları. ❌
* **Dairesel Analog Hareket:** Analog çubukların (L/R) fiziksel sınırlarına uygun dairesel hareket takibi.
* **Geniş Cihaz Desteği:** Generic USB Joystickler ve popüler oyun kollarıyla uyumlu eksen eşleştirmesi.

📂 Klasör Yapısı
joystick_test_paneli/
├── PadCheck.py       # Ana uygulama dosyası
├── tasarim.ui        # Qt Designer arayüz dosyası
├── img/              # Uygulama ikonları ve buton görselleri
└── README.md         # Proje açıklaması



🎮 Kullanım Notları
Uygulama açıldığında otomatik olarak bağlı cihazları tarar.

Eğer cihazınızın sağ analog çubuğu çalışmıyorsa, PadCheck.py içerisindeki eksen (axis) numaralarını cihazınıza göre güncelleyebilirsiniz.

Butonların görselleri img klasörü içinden dinamik olarak çekilir.

Geliştiren: Y1lmazz1
<img width="996" height="777" alt="Ekran görüntüsü 2026-02-04 022037" src="https://github.com/user-attachments/assets/f442b0b9-d9a2-4298-a2c3-149aa35b1993" />

<img width="993" height="782" alt="Ekran görüntüsü 2026-02-04 021950" src="https://github.com/user-attachments/assets/ebbb913f-4a5a-4f31-9af1-40d3c9b8f0c6" />

<img width="1000" height="755" alt="Ekran görüntüsü 2026-02-04 022005" src="https://github.com/user-attachments/assets/3eda0130-3d4a-4ad0-a205-97011c52f7a8" />

```text
🛠️ Kurulum
Python ve Gerekli Kütüphaneleri Yükleyin:

Bash
pip install PyQt6 pygame
Projeyi Klonlayın:

Bash
git clone [https://github.com/Y1lmazz1/joystick_test_paneli.git](https://github.com/Y1lmazz1/joystick_test_paneli.git)
cd joystick_test_paneli
Uygulamayı Çalıştırın:

Bash
python PadCheck.py


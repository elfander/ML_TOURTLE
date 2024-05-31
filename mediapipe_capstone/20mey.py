import cv2
import numpy as np

# Fungsi untuk menghitung sudut kamera relatif terhadap sumbu z
def calculate_camera_angle(translation_z, focal_length):
    angle_rad = np.arctan(translation_z / focal_length)
    return np.degrees(angle_rad)

# Inisialisasi video capture
cap = cv2.VideoCapture(0)

# Panjang fokus kamera (misalnya: 800 piksel)
focal_length = 800

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Ubah warna frame menjadi grayscale (untuk perhitungan yang lebih cepat)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Hitung sudut kamera relatif terhadap sumbu z (misalnya: translasi ke atas sebesar 10 unit)
    translation_z = 10
    angle_deg = calculate_camera_angle(translation_z, focal_length)

    # Tampilkan sudut kamera pada frame
    cv2.putText(frame, f'Camera Angle: {angle_deg:.2f} degrees', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Tampilkan frame
    cv2.imshow('Camera Angle Detection', frame)

    # Keluar dari loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bebaskan sumber daya
cap.release()
cv2.destroyAllWindows()


import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os

# ==========================================
# 1. Unduh Otomatis Model MediaPipe ke Laptop
# ==========================================
model_filename = "hand_landmarker.task"
model_url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

if not os.path.exists(model_filename):
    print("Sedang mengunduh file AI pendeteksi tangan dari Google (± 5 MB)...")
    print("Mohon tunggu sebentar...")
    urllib.request.urlretrieve(model_url, model_filename)
    print("Unduhan selesai dengan sukses!")

# ==========================================
# 2. Setup Detektor Tangan (Menggunakan File Lokal)
# ==========================================
options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=model_filename), # Menggunakan file yang sudah diunduh tadi
    running_mode=vision.RunningMode.IMAGE,
    num_hands=1
)
detector = vision.HandLandmarker.create_from_options(options)

# ==========================================
# 3. Inisialisasi Kamera menggunakan OpenCV
# ==========================================
cap = cv2.VideoCapture(0)
print("\nAplikasi MediaPipe Tasks Full-Blur Berjalan...")
print("Angkat tangan berbentuk 'Peace' (✌️) untuk memburamkan seluruh layar!")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Balik layar secara horizontal agar seperti cermin
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    # Konversi BGR ke RGB untuk MediaPipe
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    
    # Deteksi landmarks tangan
    detection_result = detector.detect(mp_image)
    peace_detected = False

    # Jika tangan terdeteksi
    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            
            # Logika deteksi jari (Y kecil berarti jari di atas/terbuka)
            f_telunjuk = hand_landmarks[8].y < hand_landmarks[6].y
            f_tengah = hand_landmarks[12].y < hand_landmarks[10].y
            f_manis = hand_landmarks[16].y < hand_landmarks[14].y
            f_kelingking = hand_landmarks[20].y < hand_landmarks[18].y

            # Visualisasi Manual Garis Tracking Sederhana (Jika tidak blur)
            for landmark in hand_landmarks:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            # Pola Simbol Peace (✌️)
            if f_telunjuk and f_tengah and not f_manis and not f_kelingking:
                peace_detected = True

    # ==========================================
    # 4. Logika Efek Full-Screen Blur
    # ==========================================
    if peace_detected:
        # Buramkan seluruh layar
        frame = cv2.GaussianBlur(frame, (199, 199), 0)
        cv2.putText(frame, "PEACE DETECTED: SCREEN BLURRED", (50, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

    cv2.imshow("MediaPipe Tasks - Peace Full Blur", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
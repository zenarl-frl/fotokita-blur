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
    urllib.request.urlretrieve(model_url, model_filename)
    print("Unduhan selesai dengan sukses!")

# ==========================================
# 2. Setup Detektor Tangan (MediaPipe Tasks API)
# ==========================================
options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=model_filename),
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)
# DEFINISI KONEKSI JARI (Menghubungkan 21 titik landmarks MediaPipe)
HAND_CONNECTIONS = [
    # Ibu Jari / Jempol
    (0, 1), (1, 2), (2, 3), (3, 4),
    # Jari Telunjuk
    (0, 5), (5, 6), (6, 7), (7, 8),
    # Jari Tengah
    (9, 10), (10, 11), (11, 12),
    # Jari Manis
    (13, 14), (14, 15), (15, 16),
    # Jari Kelingking
    (0, 17), (17, 18), (18, 19), (19, 20),
    # Telapak Tangan (Penghubung struktur bawah)
    (5, 9), (9, 13), (13, 17)
]

# ==========================================
# 3. Inisialisasi Kamera menggunakan OpenCV
# ==========================================
cap = cv2.VideoCapture(0)
print("\nAplikasi MediaPipe Tasks Kerangka Jari Berjalan...")
frame_timestamp_ms = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    
    frame_timestamp_ms += 33  # ~30 FPS
    detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)
    peace_detected = False

    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            
            # Logika deteksi jari terangkat
            f_telunjuk = hand_landmarks[8].y < hand_landmarks[6].y
            f_tengah = hand_landmarks[12].y < hand_landmarks[10].y
            f_manis = hand_landmarks[16].y < hand_landmarks[14].y
            f_kelingking = hand_landmarks[20].y < hand_landmarks[18].y

            # --- BARU: LOGIKA MENGGAMBAR GARIS HUBUNG JARI ---
            # 1. Gambar Garis Penghubung antar Sendi
            for connection in HAND_CONNECTIONS:
                start_idx = connection[0]
                end_idx = connection[1]
                
                # Ubah koordinat normalisasi (0.0 - 1.0) menjadi piksel layar asli
                start_pt = (int(hand_landmarks[start_idx].x * w), int(hand_landmarks[start_idx].y * h))
                end_pt = (int(hand_landmarks[end_idx].x * w), int(hand_landmarks[end_idx].y * h))
                
                # Menggambar garis putih tipis sebagai tulang jari
                cv2.line(frame, start_pt, end_pt, (255, 255, 255), 2)

            # 2. Gambar Bulatan Sendi di Atas Garis (Agar tertutup rapi)
            for landmark in hand_landmarks:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (255, 255,255), -1)

            # Pola Simbol Peace (✌️)
            if f_telunjuk and f_tengah and not f_manis and not f_kelingking:
                peace_detected = True

    # ==========================================
    # 4. Logika Efek Full-Screen Blur
    # ==========================================
    if peace_detected:
        frame = cv2.GaussianBlur(frame, (199, 199), 0)
        cv2.putText(frame, "PEACE DETECTED: SCREEN BLURRED", (50, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

    cv2.imshow("MediaPipe Tasks - Peace Full Blur", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
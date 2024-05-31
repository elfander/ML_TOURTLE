import cv2
import mediapipe as mp
import numpy as np

# Inisialisasi MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Fungsi untuk menggambar skeleton dari pose
def draw_skeleton(frame, landmarks):
    for connection in mp_pose.POSE_CONNECTIONS:
        start_landmark = landmarks[connection[0]]
        end_landmark = landmarks[connection[1]]

        # Periksa apakah landmark memiliki nilai yang valid
        if start_landmark and end_landmark:
            start_point = (int(start_landmark[0]), int(start_landmark[1]))
            end_point = (int(end_landmark[0]), int(end_landmark[1]))
            
            cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

# Fungsi untuk mendapatkan titik sudut kamera berdasarkan posisi tubuh
def get_camera_corners(landmarks, frame_width, frame_height):
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

    top_left = [0, 0]
    top_right = [frame_width, 0]
    bottom_left = [0, frame_height]
    bottom_right = [frame_width, frame_height]

    if all(left_shoulder) and all(right_shoulder) and all(left_hip) and all(right_hip):
        top_left[0] = min(left_shoulder[0], right_shoulder[0], left_hip[0], right_hip[0])
        top_left[1] = min(left_shoulder[1], right_shoulder[1], left_hip[1], right_hip[1])

        top_right[0] = max(left_shoulder[0], right_shoulder[0], left_hip[0], right_hip[0])
        top_right[1] = min(left_shoulder[1], right_shoulder[1], left_hip[1], right_hip[1])

        bottom_left[0] = min(left_shoulder[0], right_shoulder[0], left_hip[0], right_hip[0])
        bottom_left[1] = max(left_shoulder[1], right_shoulder[1], left_hip[1], right_hip[1])

        bottom_right[0] = max(left_shoulder[0], right_shoulder[0], left_hip[0], right_hip[0])
        bottom_right[1] = max(left_shoulder[1], right_shoulder[1], left_hip[1], right_hip[1])

    return [top_left, top_right, bottom_right, bottom_left]

# Inisialisasi video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Ubah warna frame menjadi RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Deteksi pose
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        # Ambil landmark pose
        landmarks = [(lm.x * frame.shape[1], lm.y * frame.shape[0]) for lm in results.pose_landmarks.landmark]

        # Gambar skeleton
        draw_skeleton(frame, landmarks)

        # Dapatkan sudut kamera berdasarkan posisi tubuh
        camera_corners = get_camera_corners(landmarks, frame.shape[1], frame.shape[0])

        # Gambar titik sudut kamera
        for corner in camera_corners:
            cv2.circle(frame, (int(corner[0]), int(corner[1])), 5, (0, 0, 255), -1)

        # Mencetak koordinat sudut-sudut kamera
        print("Sudut kamera:")
        for i, corner in enumerate(camera_corners):
            print(f"Sudut {i+1}: ({corner[0]}, {corner[1]})")

    cv2.imshow('Camera Perspective', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


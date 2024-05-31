import cv2
import mediapipe as mp
import time
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# Inisialisasi posisi awal berdiri
initial_ankle_position = None

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        success, image = cap.read()

        start = time.time()

        # Flip the image horizontally for a later selfie-view display
        # Convert the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
       
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False

        # Process the image and detect the pose
        results = pose.process(image)

        image.flags.writeable = True

        # Convert the image color back so it can be displayed
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw the pose annotation on the image.
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Contoh menghitung sudut kemiringan berdasarkan landmark kaki
        if results.pose_landmarks:
            # Mendapatkan koordinat landmark
            landmarks = results.pose_landmarks.landmark
            # Mendapatkan koordinat landmark kaki
            left_ankle = (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y)
            right_ankle = (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y)

            # Inisialisasi posisi awal berdiri
            if initial_ankle_position is None:
                initial_ankle_position = (left_ankle[0] + right_ankle[0]) / 2, (left_ankle[1] + right_ankle[1]) / 2
            
            # Menghitung sudut kemiringan berdasarkan perbedaan posisi saat ini dengan posisi awal
            current_ankle_position = (left_ankle[0] + right_ankle[0]) / 2, (left_ankle[1] + right_ankle[1]) / 2
            angle_rad = math.atan((current_ankle_position[1] - initial_ankle_position[1]) / (current_ankle_position[0] - initial_ankle_position[0]))
            angle_deg = math.degrees(angle_rad)

            # Menampilkan sudut kemiringan
            cv2.putText(image, f'Angle: {angle_deg:.2f} degrees', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        end = time.time()
        totalTime = end - start
        fps = 1 / totalTime

        # Display FPS
        cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

        cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()


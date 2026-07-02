from logging import root
from engineering_mode import open_engineering_mode
import cv2
import pickle
import csv
from datetime import datetime
import os
from scipy.spatial.distance import cosine
from insightface.app import FaceAnalysis
import time
import mediapipe as mp
import math
from email_utils import send_email
import numpy as np
import random
import requests
import sqlite3
import customtkinter as ctk
from tkinter import messagebox
DB_PATH = "database/chronosface.db"
engineering_icon = cv2.imread("assets/settings.png")
if engineering_icon is not None:
    engineering_icon = cv2.resize(
        engineering_icon,
        (55,55)
    )
def load_settings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        camera_index,
        recognition_threshold,
        ear_threshold
    FROM settings
    WHERE id=1
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        return row
    return (
        0,
        0.60,
        0.25
    )
def verify_admin():
    popup = ctk.CTk()
    popup.title("Admin Verification")
    popup.geometry("400x220")
    popup.resizable(False, False)
    popup.lift()
    popup.attributes("-topmost", True)
    popup.after(
        100,
        lambda: popup.attributes("-topmost", False)
    )
    ctk.CTkLabel(
        popup,
        text="Engineering Mode",
        font=("Segoe UI",22,"bold")
    ).pack(pady=20)
    username_entry = ctk.CTkEntry(
        popup,
        width=250,
        placeholder_text="Admin ID"
    )
    username_entry.pack(pady=8)
    password_entry = ctk.CTkEntry(
        popup,
        width=250,
        show="*",
        placeholder_text="Password"
    )
    password_entry.pack(pady=8)
    def check_password():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT
            admin_username,
            admin_password
        FROM settings
        WHERE id=1
        """)
        db_admin, db_password = cursor.fetchone()
        conn.close()
        if (
            username_entry.get() == db_admin
            and
            password_entry.get() == db_password
        ):
            popup.destroy()
            open_engineering_mode()
        else:
            messagebox.showerror(
                "Access Denied",
                "Incorrect Password"
            )
    ctk.CTkButton(
        popup,
        text="Verify",
        command=check_password
    ).pack(pady=15)
    popup.mainloop()
marked_names = set()
last_email_time = 0
last_unknown_save_time = 0
previous_face_area = 0
stable_face_count = 0
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True
)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
MOUTH_TOP = 13
MOUTH_BOTTOM = 14
def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )
def calculate_ear(eye_landmarks):
    vertical_1 = euclidean_distance(
        eye_landmarks[1],
        eye_landmarks[5]
    )
    vertical_2 = euclidean_distance(
        eye_landmarks[2],
        eye_landmarks[4]
    )
    horizontal = euclidean_distance(
        eye_landmarks[0],
        eye_landmarks[3]
    )
    ear = (
        vertical_1 + vertical_2
    ) / (2.0 * horizontal)
    return ear
def detect_smile(
    landmarks,
    frame_height
):
    top = landmarks[MOUTH_TOP]
    bottom = landmarks[MOUTH_BOTTOM]
    mouth_gap = abs(
        (bottom.y - top.y)
        * frame_height
    )
    print("Mouth Gap:", mouth_gap)
    return mouth_gap > 8
def detect_screen_spoof(face_crop):
    gray = cv2.cvtColor(
        face_crop,
        cv2.COLOR_BGR2GRAY
    )
    resized = cv2.resize(
        gray,
        (128, 128)
    )
    fft = np.fft.fft2(
        resized
    )
    fft_shift = np.fft.fftshift(
        fft
    )
    magnitude = np.abs(
        fft_shift
    )
    magnitude_log = np.log(
        magnitude + 1
    )
    high_frequency_energy = np.mean(
        magnitude_log[50:80, 50:80]
    )

    print(
        "FFT Energy:",
        high_frequency_energy
    )

    edges = cv2.Canny(
        gray,
        100,
        200
    )
    edge_ratio = np.mean(edges)
    if (
        high_frequency_energy > 8.5 or
        edge_ratio > 40
    ):
        return True
    return False
def detect_head_movement(
    landmarks,
    frame_width,
    challenge
):
    nose_tip = landmarks[1]
    nose_x = int(
        nose_tip.x * frame_width
    )
    center_x = frame_width // 2
    print(
        f"Challenge={challenge}, "
        f"Nose={nose_x}, "
        f"Center={center_x}"
    )
    if challenge == "LEFT":
        return abs(nose_x - center_x) > 50
    if challenge == "RIGHT":
        return abs(nose_x - center_x) > 50
    return False
def mark_attendance(name):
    file_path = "attendance/attendance.csv"
    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )
    current_date = datetime.now().strftime(
        "%Y-%m-%d"
    )
    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )
    if name in marked_names:
        return
    already_marked = False
    if not os.path.exists(file_path):
        with open(
            file_path,
            "w",
            newline=""
        ) as f:
            writer = csv.writer(f)
            writer.writerow([
                "Name",
                "Date",
                "Time"
            ])
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 1:
                if (
                    row[0] == name and
                    row[1] == current_date
                ):
                    already_marked = True
                    break
    if not already_marked:
        with open(
            file_path,
            "a",
            newline=""
        ) as f:
            writer = csv.writer(f)
            writer.writerow([
                name,
                current_date,
                current_time
            ])
        print(
            f"Attendance Marked for {name}"
        )
        marked_names.add(name)
recognition_counter = {}
camera_index, recognition_threshold, ear_threshold = load_settings()
def recognize_faces():
    global last_email_time
    global previous_face_area
    global stable_face_count
    embeddings_path = (
        "embeddings/face_embeddings.pkl"
    )
    if not os.path.exists(embeddings_path):
        raise FileNotFoundError(
            "No embeddings found."
        )
    app = FaceAnalysis(
        name="buffalo_l"
    )
    app.prepare(ctx_id=0)
    with open(
        embeddings_path,
        "rb"
    ) as f:
        employee_embeddings = pickle.load(f)
    print("Loaded Embeddings:", employee_embeddings)
    print("Count:", len(employee_embeddings))
    if not employee_embeddings:
        raise ValueError(
            "Embeddings file is empty."
        )
    print(
        "Embeddings Loaded Successfully!"
    )
    blink_counter = 0
    blink_verified = False
    challenge_sequence = [
        "BLINK",
        "LEFT",
        "RIGHT",
        "SMILE"
    ]
    random.shuffle(
        challenge_sequence
    )
    current_challenge_index = 0
    challenge_completed = False
    challenge_start_time = time.time()
    last_blink_time = 0
    liveness_reset_done = False
    button_clicked = False
    cap = cv2.VideoCapture(camera_index)
    def mouse_click(event, x, y, flags, param):
        nonlocal button_clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            if (
                button_x1 <= x <= button_x2
                and
                button_y1 <= y <= button_y2
            ):
                button_clicked = True
    cv2.namedWindow("ChronosFace Recognition")
    cv2.setMouseCallback(
        "ChronosFace Recognition",
        mouse_click
    )
    if not cap.isOpened():
        raise RuntimeError(
            "Could not open camera."
        )
    try:
        while True:
            frame_start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break
            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )
            mesh_results = face_mesh.process(
                rgb_frame
            )
            if mesh_results.multi_face_landmarks:
                for face_landmarks in (
                    mesh_results.multi_face_landmarks
                ):
                    h, w, _ = frame.shape
                    current_challenge = (
                        challenge_sequence[
                            current_challenge_index
                        ]
                    )
                    challenge_passed = False                           
                    eye_points = []
                    for index in LEFT_EYE:
                        landmark = (
                            face_landmarks.landmark[index]
                        )
                        x = int(landmark.x * w)
                        y = int(landmark.y * h)
                        eye_points.append((x, y))
                    ear = calculate_ear(
                        eye_points
                    )
                    print("EAR:", ear)
                    if current_challenge == "BLINK":
                        if blink_counter >= 2:
                            challenge_passed = True
                            blink_verified = True
                    elif current_challenge == "LEFT":
                        if detect_head_movement(
                            face_landmarks.landmark,
                            w,
                            "LEFT"
                        ):
                            challenge_passed = True
                    elif current_challenge == "RIGHT":
                        if detect_head_movement(
                            face_landmarks.landmark,
                            w,
                            "RIGHT"
                        ):
                            challenge_passed = True
                    elif current_challenge == "SMILE":
                        if detect_smile(
                            face_landmarks.landmark,
                            h
                        ):
                            challenge_passed = True
                    if challenge_passed:

                        print(f"{current_challenge} Passed")

                        current_challenge_index += 1

                        challenge_passed = False

                        challenge_start_time = time.time()

                        if current_challenge_index >= len(challenge_sequence):

                            challenge_completed = True

                            print("All Challenges Completed")
                    if ear < ear_threshold:
                        current_blink_time = time.time()
                        if (
                            current_blink_time -
                            last_blink_time
                        ) > 1:
                            blink_counter += 1
                            liveness_reset_done = False
                            last_blink_time = (
                                current_blink_time
                            )
                            print(
                                f"Blink Count: {blink_counter}"
                            )
            detection_start = time.time()
            faces = app.get(frame)
            for face in faces:
                bbox = face.bbox.astype(int)
                x1, y1, x2, y2 = bbox
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )
            detection_end = time.time()
            detection_time = (
                detection_end -
                detection_start
            )
            for face in faces:
                live_embedding = face.embedding
                best_match = "Unknown"
                best_similarity = -1
                bbox = face.bbox.astype(int)
                x1, y1, x2, y2 = bbox
                current_face_area = (
                    (x2 - x1) *
                    (y2 - y1)
                )
                if previous_face_area != 0:
                    difference = abs(
                        current_face_area -
                        previous_face_area
                    )
                    if difference < 500:
                        stable_face_count += 1
                    else:
                        stable_face_count = 0
                previous_face_area = current_face_area
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(frame.shape[1], x2)
                y2 = min(frame.shape[0], y2)
                face_crop = frame[
                    y1:y2,
                    x1:x2
                ]
                if face_crop.size == 0:
                    continue
                spoof_detected = False
                try:
                    spoof_detected = detect_screen_spoof(face_crop)
                except Exception as e:
                    print("FFT Error:", e)
                    spoof_detected = False
                for (
                    name,
                    stored_embedding
                ) in employee_embeddings.items():
                    similarity = 1 - cosine(
                        live_embedding,
                        stored_embedding
                    )
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = name
                if spoof_detected:
                    cv2.putText(
                        frame,
                        "SCREEN SPOOF DETECTED",
                        (20, 260),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )
                    best_match = "SPOOF BLOCKED"
                print("Best Match:", best_match)
                print("Similarity:", best_similarity)
                if best_similarity < recognition_threshold:
                    best_match = "Unknown"
                    global last_unknown_save_time
                    current_time = time.time()
                    if current_time - last_unknown_save_time > 30:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        os.makedirs(
                            "unknown_faces",
                            exist_ok=True
                        )
                        image_path = (
                            f"unknown_faces/"
                            f"unknown_{timestamp}.jpg"
                        )
                        cv2.imwrite(
                            image_path,
                            face_crop
                        )
                        print(
                            "Unknown Face Saved:",
                            image_path
                        )
                        last_unknown_save_time = current_time
                        if current_time - last_email_time > 30:
                            try:
                                send_email(
                                    "madichettysairuchita@gmail.com",
                                    "Unknown Face Detected",
                                    f"""
                ChronosFace AI detected an unknown person.
                Time: {timestamp}
                Image Saved:
                {image_path}
                """
                                )
                                last_email_time = current_time
                                print("Alert Email Sent")
                            except Exception as e:
                                print("Email Error:", e)
                else:
                    if best_match not in recognition_counter:
                        recognition_counter[best_match] = 0
                    recognition_counter[best_match] += 1
                    print("blink_verified =", blink_verified)
                    print("challenge_completed =", challenge_completed)
                    print("spoof_detected =", spoof_detected)
                    print("recognition_counter =", recognition_counter[best_match])
                    if (
                        blink_verified and
                        challenge_completed and
                        not spoof_detected and
                        recognition_counter[best_match] >= 3
                    ):
                        print("ATTENDANCE CONDITIONS PASSED")
                        try:
                            response = requests.post(
                                "http://127.0.0.1:5000/api/biometric/verify",
                                json={
                                    "employeeName": best_match
                                },
                                timeout=5
                            )
                            result = response.json()
                            if result.get("status") == "verified":
                                mark_attendance(best_match)
                                print(f"Attendance Marked for {best_match}")
                        except requests.exceptions.RequestException as e:
                            print("API Error:", e)
                        time.sleep(2)
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                    else:
                        best_match = (
                            f"{best_match} "
                            f"- Blink 2 Times"
                        )
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )
                if spoof_detected:
                    cv2.putText(
                        frame,
                        "REPLAY ATTACK",
                        (20,220),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,0,255),
                        3
                    )
                if (
                    blink_verified and
                    challenge_completed and
                    not spoof_detected
                ):
                    cv2.putText(
                        frame,
                        "Liveness Verified",
                        (20, 160),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        3
                    )
                else:
                    cv2.putText(
                        frame,
                        "Please Blink",
                        (20, 160),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 0),
                        3
                    )

                text = (
                    f"{best_match} "
                    f"({best_similarity:.2f})"
                )

                cv2.putText(
                    frame,
                    text,
                    (x1, y1 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )

            frame_end_time = time.time()

            total_time = (
                frame_end_time -
                frame_start_time
            )

            fps = 1 / total_time

            if (
                not challenge_completed
                and
                current_challenge_index
                < len(challenge_sequence)
            ):
                cv2.putText(
                    frame,
                    f"DO: {challenge_sequence[current_challenge_index]}",
                    (20,320),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,165,255),
                    3
                )
            else:
                cv2.putText(
                    frame,
                    "HEAD VERIFIED",
                    (20, 320),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )

            cv2.putText(
                frame,
                f"FPS: {fps:.2f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                3
            )
            cv2.putText(
                frame,
                f"Detection Time: "
                f"{detection_time:.3f}s",
                (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3
            )
            button_x1 = frame.shape[1] - 200
            button_y1 = 20
            button_x2 = frame.shape[1] - 20
            button_y2 = 70
            if engineering_icon is not None:
                button_x = frame.shape[1] - 65
                button_y = 15
                button_x1 = button_x
                button_y1 = button_y
                button_x2 = button_x + 55
                button_y2 = button_y + 55
                frame[
                    button_y1:button_y2,
                    button_x1:button_x2
                ] = engineering_icon
            if (
                time.time() -
                last_blink_time
            ) > 30 and not liveness_reset_done:
                blink_counter = 0
                blink_verified = False
                challenge_completed = False
                current_challenge_index = 0
                challenge_start_time = time.time()
                liveness_reset_done = True
                print("Liveness Reset")
            if button_clicked:
                button_clicked = False
                verify_admin()   
            cv2.imshow(
                "ChronosFace Recognition",
                frame
            )
            if cv2.waitKey(1) == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    recognize_faces()
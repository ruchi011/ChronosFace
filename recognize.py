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

marked_names = set()
last_email_time = 0
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
    return mouth_gap > 15
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
        high_frequency_energy > 7.9 or
        edge_ratio > 25
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

    if (
        challenge == "LEFT" and
        nose_x < center_x - 40
    ):

        return True

    if (
        challenge == "RIGHT" and
        nose_x > center_x + 40
    ):
        return True

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

    if not employee_embeddings:

        raise ValueError(
            "Embeddings file is empty."
        )

    print(
        "Embeddings Loaded Successfully!"
    )
    blink_counter = 0
    challenge = random.choice([
        "LEFT",
        "RIGHT",
        "SMILE"
    ])
    challenge_completed = False
    current_challenge = 0
    challenge_completed = False
    challenge_start_time = time.time()
    last_blink_time = 0
    liveness_reset_done = False
    cap = cv2.VideoCapture(0)
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
                    if (
                        not challenge_completed and
                        time.time() -
                        challenge_start_time < 5
                    ):
                        if detect_head_movement(
                            face_landmarks.landmark,
                            w,
                            challenge
                        ):
                            challenge_completed = True
                            print(
                                "Head Challenge Passed"
                            )
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
                    if challenge == "SMILE":
                        if detect_smile(
                            face_landmarks.landmark,
                            h
                        ):
                            challenge_completed = True
                            print(
                                "Smile Challenge Passed"
                            )
                    if ear < 0.25:

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

                    spoof_detected = (
                        detect_screen_spoof(
                            face_crop
                        )
                    )

                except Exception as e:

                    print(
                        "FFT Error:",
                        e
                    )

                for (
                    employee_name,
                    stored_embedding
                ) in employee_embeddings.items():
                    similarity = 1 - cosine(
                        live_embedding,
                        stored_embedding
                    )

                    if similarity > best_similarity:

                        best_similarity = similarity

                        best_match = employee_name

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

                if best_similarity < 0.70:

                    best_match = "Unknown"

                    timestamp = datetime.now().strftime(
                        "%Y%m%d_%H%M%S"
                    )

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
                        frame
                    )

                    print(
                        "Unknown Face Saved:",
                        image_path
                    )

                    if (
                        time.time() -
                        last_email_time
                    ) > 30:

                        try:

                            send_email(
                                "madichettysairuchita@gmail.com",
                                "Unknown Face Detected",
                                f"""
                                ChronosFace AI detected an unknown person.
                                Time: {timestamp}
                                Snapshot Saved:
                                {image_path}
                                """
                            )
                            last_email_time = time.time()
                            print(
                                "Alert Email Sent"
                            )
                        except Exception as e:
                            print(
                                "Email Error:",
                                e
                            )
                else:
                    if best_match not in recognition_counter:
                        recognition_counter[best_match] = 0
                    recognition_counter[best_match] += 1
                    if (
                        blink_counter >= 2 and
                        challenge_completed and
                        not spoof_detected and
                        recognition_counter[best_match] >= 15
                    ):
                        mark_attendance(best_match)
                        print(
                            f"Attendance Marked for {best_match}"
                        )
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
                if stable_face_count > 80:
                    spoof_detected = True
                    cv2.putText(
                        frame,
                        "REPLAY ATTACK",
                        (20, 220),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )
                if (
                    blink_counter >= 2 and
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
                not challenge_completed and
                time.time() -
                challenge_start_time < 5
            ):

                cv2.putText(
                    frame,
                    f"DO: {challenge}",
                    (20, 320),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 165, 255),
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

            if (
                time.time() -
                last_blink_time
            ) > 8 and not liveness_reset_done:

                blink_counter = 0

                challenge_completed = False

                challenge = random.choice(
                    ["LEFT", "RIGHT", "SMILE"]
                )
                current_challenge = 0
                challenge_start_time = time.time()
                liveness_reset_done = True
                print("Liveness Reset")
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
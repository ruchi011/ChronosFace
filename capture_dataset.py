import cv2
import os
import time
from flask import app
from insightface.app import FaceAnalysis
def capture_employee_dataset(employee_name):
    dataset_path = f"dataset/{employee_name}"
    os.makedirs(dataset_path, exist_ok=True)
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0)
    cap = cv2.VideoCapture(0)
    count = 0
    last_capture_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(
            frame,
            f"Images Captured: {count}/5",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            "Move Face Slightly",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )
        faces = app.get(frame)

        if len(faces) > 0:

            face = faces[0]

            bbox = face.bbox.astype(int)

            x1, y1, x2, y2 = bbox

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            current_time = time.time()

            if current_time - last_capture_time >= 1:

                face_crop = frame[
                    y1:y2,
                    x1:x2
                ]

                face_crop = cv2.resize(
                    face_crop,
                    (224, 224)
                )

                image_path = (
                    f"{dataset_path}/"
                    f"{employee_name}_{count}.jpg"
                )

                cv2.imwrite(
                    image_path,
                    face_crop
                )

                print(
                    f"Captured Image {count}"
                )

                count += 1

                last_capture_time = current_time
        cv2.imshow(
            "Capture Dataset",
            frame
        )
        if count >= 5:
            break
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print(f"Dataset captured for {employee_name}")
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        employee_name = sys.argv[1]
    else:
        employee_name = input("Enter Employee Name: ")
    capture_employee_dataset(employee_name)
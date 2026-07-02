import os
import cv2
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0)

for img_name in os.listdir("dataset/pooji"):
    img_path = os.path.join("dataset", "pooji", img_name)

    img = cv2.imread(img_path)

    if img is None:
        print(img_name, "NOT LOADED")
        continue

    faces = app.get(img)

    print(img_name, "Faces Found:", len(faces))
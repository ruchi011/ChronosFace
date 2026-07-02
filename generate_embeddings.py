import os
import cv2
import pickle
import numpy as np
from insightface.app import FaceAnalysis
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0)
dataset_path = "dataset"
employee_embeddings = {}
for name in os.listdir(dataset_path):
    employee_folder = os.path.join(
        dataset_path,
        name
    )
    embeddings_list = []
    for image_name in os.listdir(employee_folder):
        image_path = os.path.join(
            employee_folder,
            image_name
        )
        image = cv2.imread(image_path)
        faces = app.get(image)
        if len(faces) > 0:
            embedding = faces[0].embedding
            embeddings_list.append(embedding)
    if len(embeddings_list) > 0:
        average_embedding = np.mean(
            embeddings_list,
            axis=0
        )
        employee_embeddings[name] = average_embedding
with open("embeddings/face_embeddings.pkl", "wb") as f:
    pickle.dump(employee_embeddings, f)
print("Embeddings Generated Successfully!")
from tensorflow.keras.models import load_model
from process import process_nibabel
import numpy as np

# test_image = "/workspace/3DCNN_Version1/study_0946.nii.gz"

# model=load_model("/workspace/3DCNN_Version1/3d_image_classification.h5")
# preprocessed_volume = process_nibabel(test_image)
# prediction = model.predict(np.expand_dims(preprocessed_volume, axis=0))[0]
# scores = [1 - prediction[0], prediction[0]]

# class_names = ["Normal", "Abnormal"]
# for score, name in zip(scores, class_names):
#     print(
#         "This model is %.2f percent confident that CT scan is %s"
#         % ((100 * score), name)
#     )


def test_pnemonia(file_path):
    model=load_model("3d_image_classification.h5")
    preprocessed_volume = process_nibabel(file_path)
    prediction = model.predict(np.expand_dims(preprocessed_volume, axis=0))[0]
    return prediction[0]

# print(test_pnemonia(test_image))

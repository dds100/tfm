from sahi.utils.yolov8 import download_yolov8s_model
from sahi import AutoDetectionModel
from sahi.utils.cv import read_image
from sahi.utils.file import download_from_url
from sahi.predict import get_prediction, get_sliced_prediction, predict
from pathlib import Path
from IPython.display import Image

IMG_PATH = 'files\Captura de pantalla 2023-11-22 233153.png'
OUT_DIR = 'runs/sahi/prediction'
OUT_DIR_SLICE = 'runs/sahi/slice_prediction'

slice_kwargs = {
    'slice_height': 300,
    'slice_width': 300,
    'overlap_height_ratio': 0.2,
    'overlap_width_ratio': 0.2
}

# Download YOLOv8 model
yolov8_model_path = "models/yolov8n.pt"
download_yolov8s_model(yolov8_model_path)

detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolov8',
    model_path=yolov8_model_path,
    confidence_threshold=0.3,
    device="cpu",  # or 'cuda:0'
)

# With an image path
result = get_prediction(IMG_PATH, detection_model, verbose=2)

result.export_visuals(export_dir=OUT_DIR)
Image(OUT_DIR + "prediction_visual.png")

slice_result = get_sliced_prediction(
    IMG_PATH,
    detection_model,
    **slice_kwargs,
    verbose=2,

)

slice_result.export_visuals(export_dir=OUT_DIR_SLICE, text_size=.5)
Image(OUT_DIR + "slice_prediction_visual.png")



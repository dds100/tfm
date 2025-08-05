from ultralytics import YOLO

model = YOLO(model=r'models\best_v2_n.pt')
file_path = r'files\videos\simulado.mp4'
model.predict(file_path, save=True)
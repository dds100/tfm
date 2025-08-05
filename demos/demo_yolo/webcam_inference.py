import cv2
from ultralytics import YOLO
import time

# Cargar el modelo YOLO preentrenado (puede ser 'yolov8n', 'yolov8s', 'yolov8m', etc.)
model = YOLO(model=r'models\best_v2_n.pt')
# model = YOLO("yolov8n.pt")  # Usa el modelo más liviano por defecto

# Inicializar la captura desde la webcam (índice 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error al abrir la webcam.")
    exit()

print("Presiona 'q' para salir...")

while True:

    inicio = time.time()

    ret, frame = cap.read()
    if not ret:
        break

    # Hacer inferencia
    results = model(frame, verbose=False)

    # Dibujar los resultados sobre el frame
    annotated_frame = results[0].plot()
    cycle_time = time.time() - inicio
    cv2.putText(annotated_frame, f'FPS:{1/cycle_time:.2f}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    # Mostrar el frame con resultados
    cv2.imshow("YOLOv8 - Webcam", annotated_frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

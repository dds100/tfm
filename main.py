import cv2
import time
from ultralytics import YOLO
# from pyfirmata import Arduino, util
import serial


# Cargar el modelo YOLO preentrenado (puede ser 'yolov8n', 'yolov8s', 'yolov8m', etc.)
model = YOLO(model=r'models\best_v2_n.pt')
# model = YOLO("yolov8n.pt")  # Usa el modelo más liviano por defecto

# # Cargar el Arduino por puerto serie
# arduino_path = 'COM3'
# arduino = serial.Serial(arduino_path)

# # Ruta al archivo de video grabado
# video_path = r"files\videos\simulado.mp4"

# Inicializar la captura desde la webcam (índice 0)
cap = cv2.VideoCapture(1)
# cap = cv2.VideoCapture(video_path)

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

    # # Listar las detecciones
    # class_names = results[0].names
    # for resultado in results:
    #     cajas = resultado.boxes  # ultralytics.engine.results.Boxes

    #     for box in cajas:
    #         cls_id = int(box.cls[0])            # ID de la clase
    #         cls_name = class_names[cls_id]
    #         conf = float(box.conf[0])           # Confianza
    #         xyxy = box.xyxy[0].tolist()         # Coordenadas (x1, y1, x2, y2)

    #         print(f"Clase: {cls_id} ({cls_name}), Confianza: {conf:.2f}, Caja: {xyxy}")



    # Dibujar los resultados sobre el frame
    annotated_frame = results[0].plot()
    cycle_time = time.time() - inicio
    cv2.putText(annotated_frame, f'FPS:{1/cycle_time:.2f}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    # print(f'FPS: {1/cycle_time:.2f}')

    # # Dar señal al Arduino de encender un LED si hay una persona
    # class_names = results[0].names
    # detections = []
    # for box in results[0].boxes:
    #     class_id = int(box.cls[0])
    #     detections.append(class_names[class_id])
    # detections = set(detections)
    # print('Detections:', detections, 'cell phone' in detections)
    
    # if 'pipa' in detections:
    #     arduino.write(b'1')
    # else:
    #     arduino.write(b'0')

    # # Mostrar el frame con resultados
    # cv2.imshow("YOLOv8 - Webcam", annotated_frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

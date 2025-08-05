import cv2
import time
from ultralytics import YOLO
# from pyfirmata import Arduino, util
import serial


# Cargar el modelo YOLO preentrenado (puede ser 'yolov8n', 'yolov8s', 'yolov8m', etc.)
model = YOLO(model=r'models\best_v2_n.pt')

# Inicializar la captura desde la webcam (índice 0)
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error al abrir la webcam.")
    exit()
print("Presiona 'q' para salir...")

ret, frame = cap.read()
if not ret:
    print('Error abriendo cámara.')
    exit()
image_shape = frame.shape

# Inicialización de variables
detections = []
already_crossed = []
margin = 15

while True:

    # Tiempo de inicio de ciclo
    inicio = time.time()

    # Obtener un nuevo frame
    ret, frame = cap.read()
    if not ret:
        break
    # print(frame.shape)

    # Hacer inferencia
    results = model.predict(frame, verbose=False)

    # Dibujar los resultados sobre el frame
    annotated_frame = results[0].plot()
    cycle_time = time.time() - inicio
    cv2.putText(annotated_frame, f'FPS:{1/cycle_time:.2f}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    # print(f'FPS: {1/cycle_time:.2f}')

    # Dibujar línea arbitraria de cruce
    signal_line = 120
    cv2.line(annotated_frame, (0, signal_line), (image_shape[1], signal_line), (0, 0, 255), 2)

    # Generar una lista con clase y centro (o punto)
    for box in results[0].boxes:
        cx, cy = box.xywh[0][:2]
        class_name = results[0].names[int(box.cls[0])]
        detections.append({'cx': cx, 'cy': cy, 'class_name': class_name})

        if abs(cy - signal_line) < margin:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        # cv2.circle(annotated_frame, (int(cx), int(cy)), 3, color, -1)
        cv2.line(annotated_frame, (int(cx), int(cy-margin)), (int(cx), int(cy+margin)), color, 2)
        
        

    # Activar señal de pipa cruzando


    # # Mostrar el frame con resultados
    cv2.imshow("YOLOv8 - Webcam", annotated_frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

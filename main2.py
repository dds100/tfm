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
y_margin = 25
x_margin = 15

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

    # Dibujar línea arbitraria de cruce
    signal_line = 120
    cv2.line(annotated_frame, (0, signal_line), (image_shape[1], signal_line), (0, 0, 255), 2)

    # Generar una lista con clase y centro (o punto)
    crossing_detections = []
    for box in results[0].boxes:
        cx, cy = box.xywh[0][:2]
        class_name = results[0].names[int(box.cls[0])]
        detection = {'cx': cx, 'cy': cy, 'class_name': class_name}

        is_crossing_line = abs(cy - signal_line) < y_margin
        is_in_already_crossed = any([abs(cx-cx_crossed) < x_margin for cx_crossed in already_crossed])
        if is_crossing_line:
            color = (0, 255, 0)
            crossing_detections.append(detection)
            already_crossed.append(int(cx))
            if not is_in_already_crossed:
                signal = True
                print(f'Ha cruzado {detection["class_name"]}.')
        else:
            color = (0, 0, 255)
        cv2.line(annotated_frame, (int(cx), int(cy-y_margin)), (int(cx), int(cy+y_margin)), color, 2)
        
    # Pintar de más oscuro las zonas ya cruzadas
    for x in already_crossed:
        cv2.line(annotated_frame, (x-x_margin, signal_line), (x+x_margin, signal_line), (0, 0, 100), 2)

    # Eliminar las que ya no estén cruzando
    new_already_crossed = []
    for x_coord in already_crossed:
        crossing_now = False
        for detection in crossing_detections:
            if abs(detection['cx']-x_coord) < x_margin:
                crossing_now = True
        if crossing_now:
            new_already_crossed.append(x_coord)
    already_crossed = new_already_crossed
        

    # Activar señal de pipa cruzando


    # # Mostrar el frame con resultados
    cv2.imshow("YOLOv8 - Webcam", annotated_frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

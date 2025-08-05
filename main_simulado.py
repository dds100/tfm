import cv2
import time

# # Ruta al archivo de video grabado
# video_path = r"files\videos\simulado.mp4"

# Cargar el video
# cap = cv2.VideoCapture(video_path)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("No se pudo abrir el archivo de video.")
    exit()

while True:
    ret, frame = cap.read()
    
    # Ejecutar en bucle
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Aquí puedes aplicar tu inferencia, por ejemplo:
    # resultado = tu_modelo.detect(frame)
    # Procesar frame o dibujar resultados...

    cv2.imshow("Video simulado como webcam", frame)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Para respetar la velocidad del vídeo original (aproximadamente)
    time.sleep(.01)

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

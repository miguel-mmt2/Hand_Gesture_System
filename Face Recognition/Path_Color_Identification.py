import cv2

# Carregando o classificador pré-treinado para detecção facial
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicializando a câmera
cap = cv2.VideoCapture(1)

while True:
    # Capturando frame a frame
    ret, frame = cap.read()
    
    # Convertendo o frame para escala de cinza para facilitar o processamento
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectando faces no frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Desenhando retângulos ao redor das faces detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Mostrando o frame com as faces detectadas
    cv2.imshow('Face Detection', frame)
    
    # Checando se o usuário pressionou a tecla 'q' para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberando os recursos
cap.release()
cv2.destroyAllWindows()

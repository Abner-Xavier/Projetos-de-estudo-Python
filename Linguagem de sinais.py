import cv2
import mediapipe as mp

# Inicializa o MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Captura de vídeo
cap = cv2.VideoCapture(1)  # Usa a câmera frontal (tente 0 se não funcionar)

# Função para detectar o gesto "Eu te amo"
def detect_gesture(landmarks):
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]

    thumb_up = thumb_tip.y < landmarks[mp_hands.HandLandmark.THUMB_IP].y
    index_up = index_tip.y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_down = middle_tip.y > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_down = ring_tip.y > landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_up = pinky_tip.y < landmarks[mp_hands.HandLandmark.PINKY_PIP].y

    if thumb_up and index_up and pinky_up and middle_down and ring_down:
        return "Eu te amo"
    return None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Converte o frame para RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detecta mãos
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Desenha as landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Verifica o gesto e exibe o nome
            gesture = detect_gesture(hand_landmarks.landmark)
            if gesture:
                cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Exibe o resultado
    cv2.imshow("Detecção de Gestos", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

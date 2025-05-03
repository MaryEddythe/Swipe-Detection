import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_x = 0
prev_y = 0
last_gesture_time = time.time()

horizontal_threshold = 10
vertical_threshold = 10

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * img.shape[1])
            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * img.shape[0])

            dx = x - prev_x
            dy = y - prev_y

            if time.time() - last_gesture_time:
                if dx > horizontal_threshold:
                    pyautogui.hotkey('ctrl', 'pagedown')
                    print("Next Slide")
                    last_gesture_time = time.time()
                elif dx < -horizontal_threshold:
                    pyautogui.hotkey('ctrl', 'pageup')
                    print("Previous Slide")
                    last_gesture_time = time.time()
                elif dy > vertical_threshold:
                    pyautogui.scroll(500)
                    print("Scroll Up")
                    last_gesture_time = time.time()
                elif dy < -vertical_threshold:
                    pyautogui.scroll(-500)
                    print("Scroll Down")
                    last_gesture_time = time.time()

            if abs(dx) > horizontal_threshold or abs(dy) > vertical_threshold:
                prev_x = x
                prev_y = y

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

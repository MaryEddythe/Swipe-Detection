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
gesture_delay = 1
last_gesture_time = time.time()

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

            if time.time() - last_gesture_time > gesture_delay:
                # Left/Right gestures
                if x - prev_x > 100:
                    pyautogui.hotkey('ctrl', 'pagedown')  # Next page
                    print("Next Slide")
                    last_gesture_time = time.time()
                elif prev_x - x > 100:
                    pyautogui.hotkey('ctrl', 'pageup')  # Previous page
                    print("Previous Slide")
                    last_gesture_time = time.time()
                # Up/Down gestures
                elif y - prev_y > 100:
                    pyautogui.scroll(500)  # Scroll up
                    print("Scroll Up")
                    last_gesture_time = time.time()
                elif prev_y - y > 100:
                    pyautogui.scroll(-500)  # Scroll down
                    print("Scroll Down")
                    last_gesture_time = time.time()

            prev_x = x
            prev_y = y

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()

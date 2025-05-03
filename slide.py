import cv2
import mediapipe as mp
import pyautogui
import time
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x = 0
prev_y = 0
last_gesture_time = time.time()
zoom_cooldown = 0.1
previous_pinch_distance = None

horizontal_threshold = 5
vertical_threshold = 5
pinch_threshold = 50 

def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

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

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_x = int(thumb_tip.x * img.shape[1])
            thumb_y = int(thumb_tip.y * img.shape[0])
            index_x = int(index_tip.x * img.shape[1])
            index_y = int(index_tip.y * img.shape[0])

            pinch_dist = distance(thumb_x, thumb_y, index_x, index_y)

            dx = x - prev_x
            dy = y - prev_y

            if time.time() - last_gesture_time > 0.3:
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

            if pinch_dist < pinch_threshold and time.time() - last_gesture_time > zoom_cooldown:
                if previous_pinch_distance is not None:
                    if pinch_dist > previous_pinch_distance + 5:
                        pyautogui.hotkey('ctrl', '+')
                        print("Zoom In")
                        last_gesture_time = time.time()
                    elif pinch_dist < previous_pinch_distance - 5:
                        pyautogui.hotkey('ctrl', '-')
                        print("Zoom Out")
                        last_gesture_time = time.time()
                previous_pinch_distance = pinch_dist
            else:
                previous_pinch_distance = None

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()

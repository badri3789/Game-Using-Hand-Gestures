"""Game Using Hand Gestures

Refactored main script to a runnable module with clearer structure.

Usage:
    python src/main.py

This script uses the webcam to detect hand landmarks and translate finger
gestures into mouse and keyboard actions. See README.md for installation
and usage details.
"""

import cv2
import mediapipe as mp
import numpy as np
import autopy
import pydirectinput as p1
import time

# Configuration
SMOOTHING = 7  # Higher value = smoother cursor movement
DETECTION_CONFIDENCE = 0.8
TRACKING_CONFIDENCE = 0.8
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def get_landmarks(hand_module, image):
    """Return list of landmarks [[id, x, y], ...] for the first detected hand.

    Coordinates x, y are pixel values relative to the provided image.
    """
    landmarks = []
    result = hand_module.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    multi_hand = result.multi_hand_landmarks
    if multi_hand:
        # Use the first detected hand
        hand = multi_hand[0]
        h, w, _ = image.shape
        for idx, lm in enumerate(hand.landmark):
            x_px, y_px = int(lm.x * w), int(lm.y * h)
            landmarks.append([idx, x_px, y_px])
            mp_draw.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
    return landmarks


def fingers_up(landmarks):
    """Return a list of 5 integers (1 for up, 0 for down) for thumb->pinky.

    This logic is simple and works for typical frontal hand poses.
    """
    tips = [4, 8, 12, 16, 20]
    states = []

    if not landmarks or len(landmarks) < 21:
        return [0, 0, 0, 0, 0]

    # Thumb: compare x of tip with previous joint (works for right hand orientation)
    states.append(1 if landmarks[tips[0]][1] > landmarks[tips[0] - 1][1] else 0)

    # Other fingers: tip y lower than pip y means finger is up
    for i in range(1, 5):
        states.append(1 if landmarks[tips[i]][2] < landmarks[tips[i] - 3][2] else 0)

    return states


def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    w_scr, h_scr = autopy.screen.size()
    p_x = p_y = 0
    c_x = c_y = 0

    with mp_hands.Hands(min_detection_confidence=DETECTION_CONFIDENCE,
                        min_tracking_confidence=TRACKING_CONFIDENCE) as hands:
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read from webcam")
                    break

                lm_list = get_landmarks(hands, frame)

                if lm_list:
                    # Index and middle finger tips
                    x1, y1 = lm_list[8][1:]
                    x2, y2 = lm_list[12][1:]
                    finger_states = fingers_up(lm_list)

                    # Move mode: index finger up only
                    if finger_states[1] == 1 and finger_states[2] == 0 and finger_states[4] == 0:
                        x3 = np.interp(x1, (75, FRAME_WIDTH - 75), (0, w_scr))
                        y3 = np.interp(y1, (75, FRAME_HEIGHT - 75), (0, h_scr))

                        c_x = p_x + (x3 - p_x) / SMOOTHING
                        c_y = p_y + (y3 - p_y) / SMOOTHING

                        autopy.mouse.move(int(w_scr - c_x), int(c_y))
                        p_x, p_y = c_x, c_y

                    # Left click: thumb up, index down
                    if finger_states[1] == 0 and finger_states[0] == 1:
                        p1.click(button='left')

                    # Move right/left with all fingers up or none up
                    if sum(finger_states) == 5:
                        p1.keyDown("right")
                        p1.keyUp("left")
                    elif sum(finger_states) == 0:
                        p1.keyDown("left")
                        p1.keyUp("right")
                    elif finger_states[1] == 1 and finger_states[2] == 1 and finger_states[3] == 1:
                        p1.press("space")
                    elif finger_states[1] == 1:
                        p1.keyUp("right")
                        p1.keyUp("left")

                cv2.imshow("Game Using Hand Gestures", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

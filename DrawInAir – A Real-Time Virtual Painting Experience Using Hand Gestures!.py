import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Video Capture
cap = cv2.VideoCapture(0)
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

# Define Colors and Toolbar
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
color_names = ["Blue", "Green", "Red", "Yellow", "Pink"]
tool_selected = None
current_color = None  # User must select a tool first
drawing = False
prev_x, prev_y = None, None  # Store previous position for smooth drawing
shape_start = None  # Store shape start point
shape_drawing = False  # Ensures only one shape per selection
eraser_size = 20  # Default eraser size

# Define Toolbar Positions
toolbar_y = 10
tool_size = 40
toolbar_buttons = {
    "colors": [(50 + i * (tool_size + 10), toolbar_y, tool_size, tool_size, colors[i]) for i in range(len(colors))],
    "eraser": [(320, toolbar_y, tool_size, tool_size, (255, 255, 255), "Eraser")],
    "rectangle": [(380, toolbar_y, tool_size, tool_size, (200, 200, 200), "Rectangle")],
    "circle": [(440, toolbar_y, tool_size, tool_size, (200, 200, 200), "Circle")]
}

# Function to Draw Toolbar
def draw_toolbar(img):
    for button in toolbar_buttons["colors"]:
        x, y, w, h, color = button
        cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
    
    for key in ["eraser", "rectangle", "circle"]:
        x, y, w, h, color, text = toolbar_buttons[key][0]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
        cv2.putText(img, text, (x + 5, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

# Function to Check Selection
def check_selection(x, y):
    global tool_selected, current_color, shape_start, shape_drawing
    for button in toolbar_buttons["colors"]:
        bx, by, bw, bh, color = button
        if bx < x < bx + bw and by < y < by + bh:
            tool_selected = "color"
            current_color = color
            shape_start = None
            shape_drawing = False
            return
    
    for key in ["eraser", "rectangle", "circle"]:
        bx, by, bw, bh, _, text = toolbar_buttons[key][0]
        if bx < x < bx + bw and by < y < by + bh:
            tool_selected = text.lower()
            shape_start = None
            shape_drawing = False
            return

# Main Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    draw_toolbar(img)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_finger = (int(hand_landmarks.landmark[8].x * img.shape[1]), int(hand_landmarks.landmark[8].y * img.shape[0]))
            middle_finger = (int(hand_landmarks.landmark[12].x * img.shape[1]), int(hand_landmarks.landmark[12].y * img.shape[0]))
            thumb_finger = (int(hand_landmarks.landmark[4].x * img.shape[1]), int(hand_landmarks.landmark[4].y * img.shape[0]))
            
            index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
            middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
            
            # Selection Gesture: Index + Middle Finger Raised
            if index_up and middle_up:
                check_selection(index_finger[0], index_finger[1])
                drawing = False
                shape_drawing = False
                shape_start = None
            
            # Writing Gesture: Only Index Finger Raised
            elif index_up and not middle_up and tool_selected:
                drawing = True
            else:
                drawing = False
            
            # Drawing Logic
            if drawing:
                if tool_selected == "eraser":
                    cv2.circle(canvas, index_finger, eraser_size, (0, 0, 0), -1)
                elif tool_selected == "rectangle" and not shape_drawing:
                    shape_start = index_finger
                    shape_drawing = True
                elif tool_selected == "rectangle" and shape_start:
                    cv2.rectangle(canvas, shape_start, index_finger, current_color, 2)  # Only border
                elif tool_selected == "circle" and not shape_drawing:
                    shape_start = index_finger
                    shape_drawing = True
                elif tool_selected == "circle" and shape_start:
                    radius = int(((index_finger[0] - shape_start[0]) ** 2 + (index_finger[1] - shape_start[1]) ** 2) ** 0.5)
                    cv2.circle(canvas, shape_start, radius, current_color, 2)  # Only border
                else:
                    if prev_x is not None and prev_y is not None:
                        cv2.line(canvas, (prev_x, prev_y), index_finger, current_color, 5)
                    prev_x, prev_y = index_finger
            else:
                prev_x, prev_y = None, None
            
            mp_draw.draw_landmarks(img, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
    
    img = cv2.addWeighted(img, 0.5, canvas, 0.5, 0)
    cv2.imshow("Virtual Painter", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
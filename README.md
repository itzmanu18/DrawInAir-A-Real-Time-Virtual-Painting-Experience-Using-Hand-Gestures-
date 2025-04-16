# 🖌️ Draw In Air – A Real-Time Virtual Painting Experience Using Hand Gestures by Manoj! 🖐💡

This project lets you draw in the air using just your hand gestures, and the output appears live on the screen — no physical contact needed! 🚀

---

## 🔍 What It Does

- Tracks your hand in real time using MediaPipe's hand landmark model  
- Recognizes different finger gestures to perform actions:
  - ✌️ Index + Middle finger up → Select tool or color  
  - ☝️ Only Index finger up → Start drawing  
- Offers multiple tools through an interactive on-screen toolbar:
  - 🎨 Color palette (Blue, Green, Red, Yellow, Pink)  
  - 🧽 Eraser tool  
  - 📏 Rectangle and Circle shape tools  
- Everything drawn is layered on a virtual canvas and blended with the live video feed

---

## ⚙️ Technologies & Libraries Used

- 🐍 **Python** – The backbone of the entire application  
- 📷 **OpenCV** – For real-time video processing, shape rendering, and UI overlay  
- 🖐️ **MediaPipe** – For high-performance real-time hand detection and finger tracking  
- 📊 **NumPy** – For canvas array manipulations and drawing logic

---

## 🧠 How It Works Under the Hood

1. Webcam feed is captured using `cv2.VideoCapture()` and flipped for a mirror view  
2. Each frame is passed through MediaPipe’s hand detector to extract 21 hand landmarks  
3. Gestures are detected by checking which fingers are up  
4. A custom OpenCV-based toolbar allows tool/color selection by hovering over buttons  
5. Drawing/erasing actions are triggered depending on the selected tool and gesture  
6. A virtual canvas (NumPy array) holds all drawings  
7. The canvas is blended with the webcam feed for a seamless augmented drawing experience

---



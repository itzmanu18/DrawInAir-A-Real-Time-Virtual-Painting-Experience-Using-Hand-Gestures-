Draw In Air – A Real-Time Virtual Painting Experience Using Hand Gestures! 🖐💡

This project lets you draw in the air using just your hand gestures, and the output appears live on the screen — no physical contact needed!🚀

🔍 What It Does:
Tracks your hand in real time using MediaPipe's hand landmark model.
Recognizes different finger gestures to perform actions:
Index + Middle finger up → Select tool or color.
Only Index finger up → Start drawing.
Offers multiple tools through an interactive on-screen toolbar:
🎨 Color palette (Blue, Green, Red, Yellow, Pink)
🧽 Eraser tool
📏 Rectangle and Circle shape tools
Everything drawn is layered on a virtual canvas and blended with the live video feed.

⚙️ Technologies & Libraries Used:
Python – The backbone of the entire application
OpenCV – For real-time video processing, shape rendering, and user interface overlay
MediaPipe – For high-performance real-time hand detection and finger landmark tracking
NumPy – For canvas array manipulations and drawing logic

🧠 How It Works Under the Hood:
A webcam feed is captured using cv2.VideoCapture(), flipped for mirror view, and passed through MediaPipe's hand detector.
Hand landmarks (21 points per hand) are used to identify fingers and determine gestures.
A custom toolbar is drawn using OpenCV where users can select tools/colors based on finger position.
Drawing or erasing is triggered depending on the selected tool and current gesture.
The virtual canvas is stored as a NumPy array and continuously updated as the user interacts.
The canvas is then blended with the live camera frame for a real-time augmented experience.
This was a fun way to combine computer vision with interactive design. Planning to take it a step further with gesture-based UI controls soon!

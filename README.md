# 🎮 Augmented Shuiit

**Augmented Shuiit** is a real-time, AI-powered **Rock-Paper-Scissors** game that uses your **hand gestures via webcam** to play against an AI opponent.

This was my **personal project from 2022**, built when I was in **10th grade**. I was curious about **machine learning**, so I challenged myself to combine it with game development. I used **Python**, **KivyMD** for the UI, and **TensorFlow + OpenCV** for gesture recognition.

I'm uploading this as a form of **documentation** of my early journey into AI and computer vision. Since it was a beginner project, it might contain bugs — but that's all part of the learning experience!

---

## 🧠 Features

- ✋ Real-time hand detection using webcam (via OpenCV & cvzone)  
- 🧠 AI-based gesture recognition using a trained TensorFlow model  
- 🎮 Classic Rock-Paper-Scissors game logic  
- 🎵 Background music with adjustable volume  
- 🏆 High score tracking system  
- 🎨 Clean, mobile-friendly UI built with KivyMD  

---

## 📸 Preview

*(Add screenshots or gameplay GIFs here)*

---

## 💻 Requirements

- **OS**: Windows  
- **Python**: 3.11.x  
- **Processor**: Intel i5 / AMD Ryzen 5 or better  
- **GPU**: GTX 1080 or equivalent  
- **RAM**: 8 GB  
- **Storage**: 3 GB available space  
- **Webcam**: Required  

---

## 🧰 How It Works

1. The webcam captures your hand movements.  
2. `cvzone.HandDetector` detects your hand.  
3. A pre-trained **TensorFlow** model (exported from **Teachable Machine**) classifies your gesture (Rock, Paper, or Scissor).  
4. The AI (NPC) randomly picks a move.  
5. The game compares both choices and determines the winner.

---

## 🚀 Getting Started

See [INSTALLATION.md](INSTALLATION.md) for step-by-step instructions on setting up and running the game.

---

## 🧑‍🎨 Credits

- 👨‍💻 **Developer**: Zeaaa  
- 🎨 **UI/UX**: [KivyMD](https://github.com/kivymd/KivyMD)  
- 🧠 **Hand Detection & CV**: [cvzone](https://github.com/cvzone/cvzone), [OpenCV](https://opencv.org/)  
- 🧪 **Model Training**: [Teachable Machine by Google](https://teachablemachine.withgoogle.com/)  
- 🧠 **Model Inference**: [TensorFlow](https://www.tensorflow.org/)

---

*Give me a star if you like it!*

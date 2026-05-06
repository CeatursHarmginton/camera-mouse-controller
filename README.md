<div align="center">

# 🖐️ Camera Mouse Controller

**Control your computer with hand gestures — no mouse needed!**

A webcam-based virtual gesture mouse powered by MediaPipe hand tracking.

[![GitHub stars](https://img.shields.io/github/stars/CeatursHarmginton/camera-mouse-controller?style=for-the-badge&color=00ff88&labelColor=1a1a2e)](https://github.com/CeatursHarmginton/camera-mouse-controller/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/CeatursHarmginton/camera-mouse-controller?style=for-the-badge&color=00d4ff&labelColor=1a1a2e)](https://github.com/CeatursHarmginton/camera-mouse-controller/network)
[![GitHub issues](https://img.shields.io/github/issues/CeatursHarmginton/camera-mouse-controller?style=for-the-badge&color=ff6b6b&labelColor=1a1a2e)](https://github.com/CeatursHarmginton/camera-mouse-controller/issues)
[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e)](https://python.org)

</div>

---

## ✨ Features

- 🖐️ **Hand gesture control** — Move cursor, click, scroll, zoom with natural hand movements
- 📷 **Webcam only** — No special hardware needed, works with any webcam
- ⌨️ **CapsLock toggle** — Activate/deactivate tracking without interfering with your workflow
- 🎯 **Adjustable sensitivity** — Fine-tune cursor speed to your preference
- 📐 **Multiple camera positions** — Normal, Above, or Behind placement
- 📖 **Built-in gesture guide** — Interactive visual guide in the setup window
- 🎬 **Real-time overlay** — See your actions displayed in a floating overlay
- 🔍 **Pinch zoom** — Zoom in/out with thumb-index pinch gestures
- 📜 **Momentum scrolling** — Swipe to scroll with natural momentum

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/CeatursHarmginton/camera-mouse-controller.git
cd camera-mouse-controller
```

### 2. Run

**Windows** — Just double-click `run.bat`!

The script will automatically:
- ✅ Check Python installation (3.8+ required)
- ✅ Create virtual environment
- ✅ Install all dependencies (mediapipe, opencv, numpy, etc.)
- ✅ Launch the application

**Manual run (all platforms):**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m nonmouse
```

---

## 🖐️ Hand Gestures

| Gesture | Action | How To | Visual Indicator |
|---------|--------|--------|-----------------|
| ☝️ **Move Cursor** | Move mouse | Point with index finger | 🔵 Blue dot |
| ✌️ **Stop Cursor** | Freeze cursor | Touch index + middle tips | No dot |
| 👍 **Left Click** | Click | Thumb to index 2nd joint | 🟡 Yellow circle |
| ✊ **Right Click** | Right click | Hold click for 1.5s | 🔴 Red circle |
| 👆 **Scroll** | Scroll page | Fold index + move up/down | ⚫ Black circle |
| 🤏 **Zoom Out** | Zoom out | Pinch thumb + index | 🟣 Purple circle |
| 🖐️ **Zoom In** | Zoom in | Spread thumb + index | 🔵 Cyan circle |

### Gesture Images

<table>
<tr>
<td align="center"><strong>Move Cursor</strong><br><img width="200" src="images/gesture_move_cursor_1769252514204.png"></td>
<td align="center"><strong>Left Click</strong><br><img width="200" src="images/gesture_left_click_1769252530545.png"></td>
<td align="center"><strong>Scroll</strong><br><img width="200" src="images/gesture_scroll_1769252544618.png"></td>
<td align="center"><strong>Pinch Zoom</strong><br><img width="200" src="images/gesture_pinch_zoom_1769252559440.png"></td>
</tr>
</table>

---

## 📷 Camera Placement

| Mode | Description |
|------|-------------|
| 🖥️ **Normal** | Webcam facing you (laptop built-in camera) |
| ⬆️ **Above** | Camera above your hand, pointing down |
| 🔙 **Behind** | Camera behind you, pointing at the display |

---

## ⚙️ Settings

When you launch the app, a setup window appears with two panels:

- **Left panel** — Camera device, position, sensitivity, and options
- **Right panel** — Interactive hand gesture guide with images and instructions

| Setting | Description |
|---------|-------------|
| 📷 Camera | Select camera device (0-3) |
| 📍 Position | Normal / Above / Behind |
| 🎯 Sensitivity | 1-100 (Low=precise, High=fast) |
| ⏭️ Skip setup | Remember settings for next time |

---

## 💡 Tips

1. **Good lighting** — Keep your hand well-lit for better tracking
2. **Steady hand** — Keep hand parallel to the camera
3. **Distance** — Not too close, not too far from the camera
4. **CapsLock ON** = Tracking active, **CapsLock OFF** = Tracking paused
5. **Press ESC** or close the camera window to quit

---

## 🎯 Sensitivity Guide

| Range | Mode | Best For |
|-------|------|----------|
| 1-30 | Precise | Detailed work, small movements |
| 30-60 | Balanced | General use |
| 60-100 | Fast | Quick navigation, large screens |

---

## 🛠️ Tech Stack

- **[MediaPipe](https://mediapipe.dev/)** — Hand landmark detection (21 points)
- **[OpenCV](https://opencv.org/)** — Camera capture & image processing
- **[pynput](https://pynput.readthedocs.io/)** — Mouse control
- **[Pillow](https://pillow.readthedocs.io/)** — Gesture guide images
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)** — Setup UI & overlay

---

## 📁 Project Structure

```
camera-mouse-controller/
├── nonmouse/
│   ├── __init__.py        # Package metadata
│   ├── __main__.py        # Main application loop
│   ├── args.py            # Setup UI with gesture guide
│   ├── config.py          # Configuration management
│   ├── overlay.py         # Floating action overlay
│   └── utils.py           # Utility functions
├── images/                # Gesture guide images
├── config/                # PyInstaller specs
├── config.json            # User settings
├── requirements.txt       # Python dependencies
├── run.bat                # Auto-setup & run script (Windows)
└── setup.py               # Package setup
```

---

## 📝 License

This project is based on [NonMouse](https://github.com/takeyamayuki/NonMouse) by Yuki Takeyama.

---

<div align="center">

**Made with ❤️ by [CeatursHarmginton](https://github.com/CeatursHarmginton)**

⭐ Star this repo if you find it useful!

</div>

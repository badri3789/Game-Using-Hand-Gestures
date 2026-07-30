# Game Using Hand Gestures

This project demonstrates controlling mouse and keyboard actions using hand gestures detected from a webcam. It uses MediaPipe for hand landmark detection, OpenCV for camera capture and display, and Autopy / PyDirectInput to control the cursor and keyboard.

## Features

- Move the mouse by pointing with your index finger.
- Left click by raising the thumb while the index finger is down.
- Press left/right arrow keys when all fingers are down or up (example mappings).
- Press space when index, middle and ring fingers are up.

## Installation

1. Clone the repository:

   git clone https://github.com/badri3789/Game-Using-Hand-Gestures.git
   cd Game-Using-Hand-Gestures

2. Create a virtual environment (recommended) and install dependencies:

   python -m venv venv
   source venv/bin/activate  # macOS / Linux
   venv\Scripts\activate     # Windows

   pip install -r requirements.txt

3. Run:

   python src/main.py

## Requirements

- Python 3.8+
- A webcam
- OS-specific permissions to control the mouse/keyboard (Windows/macOS may require additional settings)

Dependencies are listed in requirements.txt.

## Project structure

- src/main.py — refactored main script (recommended entrypoint)
- Game using Hand Gestures.py — original script (left as a legacy file)
- README.md — this file
- requirements.txt — Python dependencies

## Notes & Safety

- Be careful when running code that controls mouse and keyboard: have an easy way to stop the script (press `q` in the OpenCV window or use your OS to kill the process).
- Gesture detection can be sensitive to lighting and camera angle. Tune camera position and confidence thresholds in `src/main.py` if detection is unstable.

## Contributing

Contributions welcome: file an issue or open a PR with improvements such as packaging, tests, or gesture calibration.

## License

You can add a license file if you want to make this project open source.

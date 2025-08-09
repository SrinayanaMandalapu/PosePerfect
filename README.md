# PosePerfect: AI Fitness Coach & Performance Analyzer

A real-time AI-powered trainer that uses your webcam to analyze your exercise form, provide instant corrective feedback.

## ## About The Project

In the world of home fitness, one of the biggest challenges is maintaining proper form without the guidance of a personal trainer. Poor form not only leads to ineffective workouts but can also cause serious injuries.

**PosePerfect** solves this problem by acting as a virtual coach. It uses computer vision to watch your movements, analyze your body angles in real-time, and provide immediate, actionable feedback—both visually and audibly—to help you perfect your form and maximize your workout potential.


## ## Key Features

* **Real-time Pose Correction:** Utilizes a webcam to analyze body landmarks and provide instant feedback on form for over 10 different exercises.
* **Multi-Exercise Support:** Easily switch between exercises like Squats, Lunges, Push-ups, and Planks with a single key press.
* **Repetition Counting:** Automatically counts valid repetitions for dynamic exercises.
* **Voice-Enabled Feedback:** Provides instructional audio cues, allowing you to focus on your workout instead of the screen.

## ## Tech Stack

* **Python 3.9+**
* **OpenCV:** For real-time video capture and image processing.
* **MediaPipe:** For high-fidelity body landmark detection.
* **NumPy:** For numerical operations and angle calculations.
* **pyttsx3:** For generating offline voice feedback.

## ## Installation & Usage

To get a local copy up and running, follow these simple steps.

### ### Prerequisites

Make sure you have Python 3.9 or higher installed on your system.

### ### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your_username/PosePerfect.git](https://github.com/your_username/PosePerfect.git)
    cd PosePerfect
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### ### Running the Application

1.  Execute the main script:
    ```sh
    python pose_detector.py
    ```

2.  Once the application window appears, use your keyboard to select an exercise and start your workout!

    * `s` - Squat
    * `p` - Plank
    * `b` - Bicep Curl
    * `l` - Lunge
    * `u` - Push-up
    * `d` - Tricep dip
    * `r` - Barbell row
    * `g` - Leg raise
    * `c` - Crunch
    * `h` - High knees
    * `q` - Quit


## ## How It Works

The application operates on a two-stage pipeline for each frame captured from the webcam:

1.  **Pose Estimation:** The high-performance MediaPipe Pose model is used to detect the 33 key 3D landmarks of the body from the image.

2.  **Analysis & Feedback Engine:** The detected landmark coordinates are fed into a logic module specific to the selected exercise. This module calculates relevant joint angles and compares them against a set of rules to determine the correctness of the form. Based on this analysis, instructional feedback is generated and delivered to the user.

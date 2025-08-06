import cv2
import mediapipe as mp
import numpy as np

def calculate_angle(a, b, c):
    a, b, c = np.array([a.x, a.y]), np.array([b.x, b.y]), np.array([c.x, c.y])
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return angle if angle <= 180.0 else 360 - angle

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("FATAL ERROR: Could not open camera.")
    exit()

# --- SETUP VARIABLES ---
stage = None
feedback = None
counter = 0
current_exercise = 'squat' # Default exercise

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
        landmarks = results.pose_landmarks.landmark
        shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]

        # --- EXERCISE LOGIC ROUTER ---
        if current_exercise == 'squat':
            knee_angle = calculate_angle(hip, knee, ankle)
            hip_angle = calculate_angle(shoulder, hip, knee)
            if knee_angle < 100: stage = "DOWN"
            if knee_angle > 160 and stage == 'DOWN':
                stage = "UP"
                counter += 1
            feedback = "CORRECT" if stage == "DOWN" and hip_angle > 90 else "INCORRECT" if stage == "DOWN" else "Ready"

        elif current_exercise == 'plank':
            stage = "HOLDING"
            hip_angle = calculate_angle(shoulder, hip, knee)
            knee_angle = calculate_angle(hip, knee, ankle)
            if hip_angle > 165 and knee_angle > 165: feedback = "GOOD FORM"
            elif hip_angle < 150: feedback = "LOWER YOUR HIPS"
            else: feedback = "STRAIGHTEN BACK"

        elif current_exercise == 'bicep_curl':
            elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
            elbow_angle = calculate_angle(shoulder, elbow, wrist)
            if elbow_angle > 160: stage = "DOWN"
            if elbow_angle < 40 and stage == 'DOWN':
                stage = "UP"
                counter += 1
            feedback = "UP" if stage == "UP" else "DOWN"

    except Exception as e:
        print(f"Error processing frame: {e}")
        pass

    # --- RENDER STATUS BOX ---
    box_color = (0,0,0)
    text_color = (255,255,255)
    feedback_color = (0,255,0) if feedback in ["CORRECT", "GOOD FORM", "UP"] else (0,0,255)

    cv2.rectangle(image, (0,0), (640, 60), box_color, -1)
    cv2.putText(image, 'EXERCISE', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
    cv2.putText(image, current_exercise.upper(), (10,45), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
    cv2.putText(image, 'REPS' if current_exercise != 'plank' else 'STATE', (200,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
    cv2.putText(image, str(counter) if current_exercise != 'plank' else stage, (195,45), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
    cv2.putText(image, 'FEEDBACK', (400,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
    cv2.putText(image, feedback, (395,45), cv2.FONT_HERSHEY_SIMPLEX, 1, feedback_color, 2, cv2.LINE_AA)

    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('Pose Correction Trainer', image)

    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'): break
    elif key == ord('s'): current_exercise, counter, stage = 'squat', 0, 'UP'
    elif key == ord('p'): current_exercise, counter, stage = 'plank', 0, 'HOLDING'
    elif key == ord('b'): current_exercise, counter, stage = 'bicep_curl', 0, 'DOWN'

cap.release()
cv2.destroyAllWindows()
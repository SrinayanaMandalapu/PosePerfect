import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import threading

def speak(text):
    if text: threading.Thread(target=pyttsx3.speak, args=(text,), daemon=True).start()

def calculate_angle(a, b, c):
    a, b, c = np.array([a.x, a.y]), np.array([b.x, b.y]), np.array([c.x, c.y])
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return angle if angle <= 180.0 else 360 - angle

# --- Exercise Processing Functions ---
def process_squat(landmarks, stage, counter):
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    knee_angle = calculate_angle(hip, knee, ankle)
    hip_angle = calculate_angle(shoulder, hip, knee)
    
    if knee_angle < 100: stage = "DOWN"
    if knee_angle > 160 and stage == 'DOWN':
        stage = "UP"
        counter += 1
    
    feedback = "Squat Down" if stage == "UP" else ("Go Up" if hip_angle > 90 else "Fix Form & Go Up")
    return feedback, stage, counter

def process_plank(landmarks, stage, counter):
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    hip_angle = calculate_angle(shoulder, hip, knee)
    knee_angle = calculate_angle(hip, knee, ankle)
    
    if hip_angle > 165 and knee_angle > 165: feedback = "GOOD FORM"
    elif hip_angle < 150: feedback = "LOWER YOUR HIPS"
    else: feedback = "STRAIGHTEN BACK"
    return feedback, "HOLDING", counter

def process_bicep_curl(landmarks, stage, counter):
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    
    if elbow_angle > 160: stage = "DOWN"
    if elbow_angle < 40 and stage == 'DOWN':
        stage = "UP"
        counter += 1
    
    feedback = "Curl Up" if stage == "DOWN" else "Go Down" if stage == "UP" else None
    return feedback, stage, counter

def process_lunge(landmarks, stage, counter):
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
    left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
    right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
    
    if left_knee_angle < 100 and right_knee_angle < 100: stage = "DOWN"
    if (left_knee_angle > 160 or right_knee_angle > 160) and stage == 'DOWN':
        stage = "UP"
        counter += 1
    
    feedback = "Lunge Down" if stage == "UP" else "Good Form, Go Up"
    return feedback, stage, counter

def process_overhead_press(landmarks, stage, counter):
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    
    if elbow_angle < 100: stage = "DOWN"
    if elbow_angle > 160 and stage == 'DOWN':
        stage = "UP"
        counter += 1
    
    feedback = "Press Up" if stage == "DOWN" else "Go Down" if stage == "UP" else None
    return feedback, stage, counter

def process_pushup(landmarks, stage, counter):
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]

    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    hip_angle = calculate_angle(shoulder, hip, knee)

    feedback = None
    # Check form first: back should be straight
    if hip_angle < 160:
        feedback = "Keep Back Straight"
    else:
        # Logic for push-up stages
        if elbow_angle > 160:
            stage = "UP"
            feedback = "Go Down"
        if elbow_angle < 90 and stage == 'UP':
            stage = "DOWN"
            counter += 1
            feedback = "Push Up"
            
    return feedback, stage, counter

def process_tricep_dip(landmarks, stage, counter):
    """Processes the tricep dip exercise."""
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    
    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    
    feedback = None
    if elbow_angle > 160:
        stage = "UP"
        feedback = "Go Down"
    if elbow_angle < 90 and stage == 'UP':
        stage = "DOWN"
        counter += 1
        feedback = "Push Up"
        
    return feedback, stage, counter

def process_barbell_row(landmarks, stage, counter):
    """Processes the barbell row exercise."""
    # Posture landmarks
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    # Arm landmarks
    elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]

    # Calculate angles
    hip_angle = calculate_angle(shoulder, hip, knee)
    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    
    feedback = None
    # Form check: ensure user is bent over
    if hip_angle > 150:
        feedback = "Hinge At Hips More"
    elif hip_angle < 90:
        feedback = "Back Too Low"
    else:
        # Repetition logic
        if elbow_angle > 160:
            stage = "DOWN"
            feedback = "Pull"
        if elbow_angle < 90 and stage == 'DOWN':
            stage = "UP"
            counter += 1
            feedback = "Release"

    return feedback, stage, counter

def process_leg_raise(landmarks, stage, counter):
    """Processes the leg raise exercise."""
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]

    # Calculate angles
    knee_angle = calculate_angle(hip, knee, ankle)
    hip_angle = calculate_angle(shoulder, hip, ankle) # Angle between torso and legs
    
    feedback = None
    # Form check: keep legs straight
    if knee_angle < 160:
        feedback = "Keep Legs Straight"
    else:
        # Repetition logic
        if hip_angle > 150: # Legs are down
            stage = "DOWN"
            feedback = "Legs Up"
        if hip_angle < 90 and stage == 'DOWN': # Legs are up
            stage = "UP"
            counter += 1
            feedback = "Legs Down"
            
    return feedback, stage, counter

def process_crunch(landmarks, stage, counter):
    """Processes the crunch exercise."""
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]

    # Angle of the torso relative to the thigh
    torso_angle = calculate_angle(shoulder, hip, knee)
    
    feedback = None
    # Repetition logic
    if torso_angle > 140:
        stage = "DOWN"
        feedback = "Crunch Up"
    if torso_angle < 120 and stage == 'DOWN':
        stage = "UP"
        counter += 1
        feedback = "Go Down"
        
    return feedback, stage, counter

def process_high_knees(landmarks, stage, counter):
    """Processes the high knees exercise."""
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
    
    feedback = "Knees Higher!"
    # Check if left knee is raised above the hip
    if stage != 'LEFT_UP' and left_knee.y < left_hip.y:
        stage = 'LEFT_UP'
        counter += 1
    # Check if right knee is raised above the hip
    elif stage != 'RIGHT_UP' and right_knee.y < right_hip.y:
        stage = 'RIGHT_UP'
        counter += 1
        
    return feedback, stage, counter
# --- Main Application Setup ---
EXERCISE_FUNCTIONS = {
    'squat': process_squat,
    'plank': process_plank,
    'bicep_curl': process_bicep_curl,
    'lunge': process_lunge,
    'overhead_press': process_overhead_press,
    'push-up':process_pushup,
    'tricep_dip':process_tricep_dip,
    'barbell-row':process_barbell_row,
    'leg-raise':process_leg_raise,
    'high-knees':process_high_knees,
    'crunch':process_crunch,

}

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("FATAL ERROR: Could not open camera.")
    exit()

stage, feedback, counter, current_exercise, last_feedback = None, None, 0, 'squat', None

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
        landmarks = results.pose_landmarks.landmark
        exercise_function = EXERCISE_FUNCTIONS[current_exercise]
        feedback, stage, counter = exercise_function(landmarks, stage, counter)
    except Exception as e:
        feedback = "No person detected"
        pass

    if feedback and feedback != last_feedback:
        speak(feedback)
        last_feedback = feedback

    # --- Render UI ---
    # (Same rendering code as before)
    box_color = (0,0,0)
    text_color = (255,255,255)
    feedback_text = feedback if feedback else "CHOOSE EXERCISE"
    feedback_color = (0,255,0) if "Good" in feedback_text else (0,0,255) if feedback_text not in ["CHOOSE EXERCISE", "Lunge Down", "Press Up", "Go Down", "Curl Up"] else text_color

    cv2.rectangle(image, (0,0), (640, 60), box_color, -1)
    cv2.putText(image, 'EXERCISE', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
    cv2.putText(image, current_exercise.upper(), (10,45), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
    cv2.putText(image, 'REPS' if current_exercise not in ['plank'] else 'STATE', (200,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
    cv2.putText(image, str(counter) if current_exercise not in ['plank'] else (stage if stage else ""), (195,45), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
    cv2.putText(image, 'FEEDBACK', (400,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
    cv2.putText(image, feedback_text, (395,45), cv2.FONT_HERSHEY_SIMPLEX, 1, feedback_color, 2, cv2.LINE_AA)
    
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('Pose Correction Trainer', image)

    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'): break
    # Reset state when changing exercise
    # squat
    if key == ord('s'): current_exercise, counter, stage, feedback = 'squat', 0, 'UP', "Squat Down"
    # plank
    elif key == ord('p'): current_exercise, counter, stage, feedback = 'plank', 0, 'HOLDING', "STRAIGHTEN BACK"
    # bicep-curl
    elif key == ord('b'): current_exercise, counter, stage, feedback = 'bicep_curl', 0, 'DOWN', "Curl Up"
    # lunge
    elif key == ord('l'): current_exercise, counter, stage, feedback = 'lunge', 0, 'UP', "Lunge Down"
    # overhead shoulder press
    elif key == ord('o'): current_exercise, counter, stage, feedback = 'overhead_press', 0, 'DOWN', "Press Up"
    # push up
    elif key == ord('u'): current_exercise, counter, stage, feedback = 'pushup', 0, 'UP', "Go Down"
    # Tricep Dips
    elif key == ord('d'): current_exercise, counter, stage, feedback = 'tricep_dip', 0, 'UP', "Go Down"  
    # Barbell Rows
    elif key == ord('r'): current_exercise, counter, stage, feedback = 'barbell_row', 0, 'DOWN', "Pull" 
    # Leg Raises
    elif key == ord('g'): current_exercise, counter, stage, feedback = 'leg_raise', 0, 'DOWN', "Legs Up"  
    # Crunches
    elif key == ord('c'): current_exercise, counter, stage, feedback = 'crunch', 0, 'DOWN', "Crunch Up"
    # High Knees
    elif key == ord('h'): current_exercise, counter, stage, feedback = 'high_knees', 0, None, "Knees Higher!"

cap.release()
cv2.destroyAllWindows()
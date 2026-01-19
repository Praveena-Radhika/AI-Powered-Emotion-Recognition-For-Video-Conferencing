import cv2
import numpy as np
from deepface import DeepFace
import time
from collections import deque

class SimpleEmotionDetectionSystem:
    def __init__(self):
        self.emotion_responses = {
            'neutral': {
                'message': 'Student appears neutral',
                'action': 'Consider introducing interactive elements',
                'color': (255, 255, 255)  # White
            },
            'angry': {
                'message': 'Student appears frustrated',
                'color': (0, 0, 255)  # Red
            },
            'disgust': {
                'message': 'Student appears not interested',
                'action': 'Add fun activities, use real-world examples',
                'color': (0, 128, 128)  # Brown
            },
            'fear': {
                'message': 'Student appears anxious/nervous',
                'action': 'Create supportive environment',
                'color': (147, 20, 255)  # Purple
            },
            'happy': {
                'message': 'Student appears excited',
                'action': 'Keep up the energy, encourage participation',
                'color': (0, 255, 0)  # Green
            },
            'sad': {
                'message': 'Student appears overwhelmed',
                'action': 'Break down concepts, provide guidance',
                'color': (255, 0, 0)  # Blue
            },
            'surprise': {
                'message': 'Student appears curious',
                'action': 'Provide challenging problems',
                'color': (0, 255, 255)  # Yellow
            }
        }
        
        # Initialize emotion history for smoothing
        self.emotion_history = deque(maxlen=5)
        
        # Initialize font settings
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.thickness = 2

    def add_overlay_box(self, frame, start_y):
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, start_y), (590, start_y + 80), 
                     (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame

    def detect_emotion(self, frame):
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], 
                                    enforce_detection=False)
            emotions = result[0]['emotion']
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
            
            # Add to history for smoothing
            self.emotion_history.append(dominant_emotion)
            
            # Return most common emotion from recent history
            return max(set(self.emotion_history), key=self.emotion_history.count)
        except Exception as e:
            print(f"Error in emotion detection: {str(e)}")
            return None

    def draw_text(self, frame, text, position, color):
        # Add black outline
        cv2.putText(frame, text, position, self.font, self.font_scale, 
                    (0, 0, 0), self.thickness + 2)
        # Add colored text
        cv2.putText(frame, text, position, self.font, self.font_scale, 
                    color, self.thickness)

    def run_detection(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        last_detection_time = time.time()
        detection_interval = 1.5  # Increased interval for better performance
        current_emotion = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame for faster processing
            frame = cv2.resize(frame, (600, 400))
            
            current_time = time.time()
            if current_time - last_detection_time >= detection_interval:
                detected_emotion = self.detect_emotion(frame)
                if detected_emotion:
                    current_emotion = detected_emotion
                last_detection_time = current_time

            if current_emotion and current_emotion in self.emotion_responses:
                response = self.emotion_responses[current_emotion]
                
                # Add background overlay
                frame = self.add_overlay_box(frame, 300)
                
                # Draw emotion and recommendations
                self.draw_text(frame, f"Emotion: {current_emotion.upper()}", 
                             (20, 330), response['color'])
                self.draw_text(frame, f"Message: {response['message']}", 
                             (20, 355), response['color'])
                self.draw_text(frame, f"Action: {response['action']}", 
                             (20, 380), response['color'])

            # Add instructions
            self.draw_text(frame, "Press 'q' to quit", 
                         (20, 30), (255, 255, 255))

            cv2.imshow('Student Emotion Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    emotion_system = SimpleEmotionDetectionSystem()
    emotion_system.run_detection()
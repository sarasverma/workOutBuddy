import cv2
import mediapipe as mp
import numpy as np

class poseDetect:
    def __init__(self, typeOfExercise):
        self.mp_drawing = mp.solutions.drawing_utils  # drawing utility
        self.mp_pose = mp.solutions.pose  # pose estimating model
        self.typeOfExercise = typeOfExercise

        # counter variables
        self.count = 0
        self.stage = None

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle
        return angle

    def exerciseParameter(self):
        if self.typeOfExercise == "curl":
            landmarks = self.results.pose_landmarks.landmark

            # get coordinates [x, y]
            shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # return angle b/w coordinates
            return self.calculate_angle(shoulder, elbow, wrist)
        pass

    def counter(self):
        # extract landmarks based on visibility
        try:
            angle = self.exerciseParameter()

            # angle parameter
            if angle > 160:
                self.stage = "Down"
            if angle < 30 and self.stage == "Down":
                self.stage = "Up"
                self.count += 1

            # display rep and stage data
            cv2.rectangle(self.image, (0, 0), (225, 73), (255, 194, 66), -1)
            cv2.putText(self.image, str(self.count), (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(self.image, self.stage, (60, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        except:
            pass

    def poseFeed(self):
        cap = cv2.VideoCapture(0) # video feed

        # setup mediapipe instance
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, frame = cap.read()

                # opencv BGR, mediapipe RGB
                self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.image.flags.writeable = False  # saves memory

                self.results = pose.process(self.image) # pose detection

                self.image.flags.writeable = True
                self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

                # render counter
                self.counter()

                # render detections
                self.mp_drawing.draw_landmarks(self.image, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                          self.mp_drawing.DrawingSpec(color=(255, 194, 66), thickness=2, circle_radius=2),
                                          self.mp_drawing.DrawingSpec(color=(255, 244, 133), thickness=2, circle_radius=2))

                # cv2.flip(image, 1) front camera
                cv2.imshow('Mediapipe Feed', self.image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    pd = poseDetect("curl")
    pd.poseFeed()

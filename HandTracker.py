import cv2
import mediapipe as mp


class HandTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def hands_finder(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def position_finder(self, image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(image, (cx, cy), 5, (10, 0, 255), cv2.FILLED)

        return lmlist
    def get_position_of_hand(self) -> list:
        cap = cv2.VideoCapture(0)
        success, image = cap.read()
        image = self.hands_finder(image)
        lmList = self.position_finder(image)
        return lmList

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()

    while True:
        success,image = cap.read()
        image = tracker.hands_finder(image)
        lmList = tracker.position_finder(image)
        if len(lmList) != 0:
            print(lmList)
        # if user clicks q, break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("DUMBASS CAM",image)

if __name__ == "__main__":
    main()
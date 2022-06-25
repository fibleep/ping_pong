import cv2
import mediapipe as mp
import numpy as np
import tensorflow


class HandTracker():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.model = tensorflow.keras.models.load_model('mp_hand_gesture')
        self.class_names = open('gesture.names', 'r').read().split('\n')
        self.mpDraw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)

    def hands_finder(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def position_finder(self, image) -> list:
        """
        Finds the position of the hand.
        :param image: current frame
        :return: list of coordinates of the hand
        """
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(Hand.landmark):
                x, y, c = image.shape
                cx, cy = int(lm.x * x), int(lm.y * y)
                lmlist.append([cx, cy])
        return lmlist

    def get_position_of_hand(self) -> list:
        success, image = self.cap.read()
        image = cv2.flip(image, 1)
        image = self.hands_finder(image)
        lmList = self.position_finder(image)
        # for entry in lmList:
        #     lmList[entry]=lmList[entry][1:]
        return lmList

    def get_gesture(self, lmList):
        if len(lmList) == 0: return 'None'
        prediction = self.model.predict([lmList])
        return self.class_names[np.argmax(prediction)]


def main():
    tracker = HandTracker()
    max_x = 0
    max_y = 0
    while True:
        success, image = tracker.cap.read()
        image = cv2.flip(image, 1)
        image = tracker.hands_finder(image)
        lmList = tracker.position_finder(image)
        print(tracker.get_gesture(lmList))

        for entry in lmList:
            if entry[0] > max_x:
                max_x = entry[0]
            if entry[1] > max_y:
                max_y = entry[1]
        print(max_x, max_y)

        # if len(lmList) != 0:
        #     print(lmList)
        # if user clicks q, break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("DUMBASS CAM", image)


if __name__ == "__main__":
    main()

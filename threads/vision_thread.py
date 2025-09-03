import cv2
from modules.short_term_memory import ShortTermMem
import mediapipe as mp
from modules.logger import logger
import mediapipe.python.solutions.hands as mphands
from google.protobuf.json_format import MessageToDict

model = mphands.Hands()


def vision_thread():
    cap = cv2.VideoCapture(0)
    has_img, img = cap.read()

    while has_img:
        has_img, img = cap.read()

        res = model.process(img)
        # logger.info(res.multi_hand_landmarks)
        if res.multi_handedness:
            output = [
                MessageToDict(c)["classification"][0]["label"]
                for c in res.multi_handedness
            ]
            logger.info(res.multi_handedness)
            ShortTermMem.set_vision_output(output)

        cv2.imshow("poulet", img)
        # ShortTermMem.set_vision_output(output)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break


if __name__ == "__main__":  # for debugging
    vision_thread()

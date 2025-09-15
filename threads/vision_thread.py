import cv2
from modules.short_term_memory import ShortTermMem
import mediapipe as mp
from modules.logger import logger
import mediapipe.python.solutions.hands as mphands
import mediapipe.python.solutions.face_detection as mpface
from google.protobuf.json_format import MessageToDict

model_hands = mphands.Hands()
model_face = mpface.FaceDetection()


def run_hand_detection(img):
    res = model_hands.process(img)
    # logger.info(res.multi_hand_landmarks)
    logger.info(res.detections)
    # if res.multi_handedness:
    #     output = [
    #         MessageToDict(c)["classification"][0]["label"]
    #         for c in res.multi_handedness
    #     ]
    #     logger.info(res.multi_handedness)
    #     ShortTermMem.set_vision_output(output)
    
def run_face_detection(img):
    res = model_face.process(img)
    # logger.info(res.multi_hand_landmarks)
    if res.multi_handedness:
        output = [
            MessageToDict(c)["classification"][0]["label"]
            for c in res.multi_handedness
        ]
        logger.info(res.multi_handedness)
        ShortTermMem.set_vision_output(output)
    

def vision_thread():
    cap = cv2.VideoCapture(0)
    has_img, img = cap.read()
    model_turn = 0 # we alternate which model is predicting at each frame
    
    while has_img:
        model_turn+=1
        has_img, img = cap.read()
        
        match model_turn%2:
            case 0:
                break
                run_hand_detection(img)
        
            case 1:
                run_face_detection(img)
        

        cv2.imshow("poulet", img)
        # ShortTermMem.set_vision_output(output)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break


if __name__ == "__main__":  # for debugging
    vision_thread()

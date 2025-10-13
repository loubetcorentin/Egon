import cv2
from egon.modules.memory import ShortTermMem, CrowdPosition
from egon.modules.logger import logger
import mediapipe.python.solutions.hands as mphands
import mediapipe.python.solutions.face_detection as mpface
import egon.config as ec
import mediapipe as mp
from egon.modules.emotional_state import EmotionalState
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
from egon.modules.utils_visual import visualize_detection
from egon.modules.console_utils import ConsoleTable
from threading import Thread
model_face = mpface.FaceDetection()
BRAIN = EmotionalState.SM


class HandModel:
    def __init__(self):
        self.detection_result_list = []
        model_file = open(ec.path_hand_gesture, "rb")
        buff = model_file.read()
        model_file.close()

        base_options = python.BaseOptions(model_asset_buffer=buff)
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def process(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        result = self.recognizer.recognize(mp_image)
        # print(result)
        for ges in result.gestures:
            for gestures in ges:
                ShortTermMem.add(f"hand_{gestures.category_name}")


class ObjectDetectionModel:

    def result_callback2(
            self,
            result: vision.ObjectDetectorResult,
            output_image: mp.Image,
            timestamp_ms: int,
        ):
            result.timestamp_ms = timestamp_ms
            self.detection_result_list.append(result)
            people_detections = []

            for detection in result.detections:
                cat_name = detection.categories[0].category_name
                ShortTermMem.add(cat_name)
                if cat_name == "person":
                    people_detections.append(detection.bounding_box)

            with CrowdPosition.lock:
                CrowdPosition.bb_list = people_detections
                CrowdPosition.img_width = output_image.width
            logger.debug(f"DELTA rot {CrowdPosition.get_delta_rot()}")


    def __init__(self):
        self.detection_result_list = []


        model_file = open(ec.path_obj_detection, "rb")
        buff = model_file.read()
        model_file.close()

        base_options = python.BaseOptions(model_asset_buffer=buff)
        options = vision.ObjectDetectorOptions(
            base_options=base_options,
            # running_mode=vision.RunningMode.LIVE_STREAM,
            score_threshold=0.5,
            # result_callback=result_callback,
        )
        self.detector = vision.ObjectDetector.create_from_options(options)

    def process(self, image, counter):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        # self.detector.detect_async(mp_image, counter)
        res = self.detector.detect(mp_image)
        
        self.result_callback2(res, output_image=mp_image,timestamp_ms=0)
        

def run_face_detection(img):
    res = model_face.process(img)
    # logger.info(res.multi_hand_landmarks)
    if res.detections:
        output = [
            {
                d.label_id[0],
                d.score[0],
                d.location_data.relative_bounding_box.xmin,

            }
            for d in res.detections
        ]
        # logger.info(output)
        for f in output:
            ShortTermMem.add(key="face")


def preprocess(img):
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return img

class VideoCapture:
    def capture_thread(self):
        while True:
            ret, self.frame = self.cap.read() 

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE,0)
        self.frame=None
        t = Thread(target=self.capture_thread, daemon=True)
        t.start()


    
        

def vision_thread():

    ct = ConsoleTable("👁️ 👁️", index=5)
    ct.d["."] = "line 96"
    fps_avg_frame_count = 10

    model_obj = ObjectDetectionModel()
    model_hand = HandModel()
    ct.d["."] = "line 114"
    cap = VideoCapture()
    try:

        ct.d["."] = "line 116"
        
        cv2.destroyAllWindows()
        cv2.namedWindow("poule")

        while False and BRAIN.current_state == BRAIN.waking:
            time.sleep(1)

        logger.info("[#55FF88][r]👁️ start vision [/r][/#55FF88]")
        ct.d["."] = "line 109"

        counter = 0
        start_time = time.time()
        frame = cap.frame
        while cap.frame is None:
            time.sleep(1)
            logger.info("cap.frame is None => sleep")
        while True:
            
            counter += 1
            ct.d["counter"] = f"{counter}"

            # Calculate the FPS
            if counter % fps_avg_frame_count == 0:
                end_time = time.time()
                fps = fps_avg_frame_count / (end_time - start_time)
                start_time = time.time()
                ct.d["FPS"] = f"{fps: 5.02f}"

            img = cap.frame.copy()
        
            img = preprocess(img)
            model_hand.process(img)
            model_obj.process(img, counter)
            img = visualize_detection(img, model_obj.detection_result_list)
            # img = visualize_detection(img, model_obj.detection_result_list)

            cv2.imshow("poule", img)
            model_obj.detection_result_list.clear()

            key = cv2.waitKey(20)
            if key == 27:  # exit on ESC
                break

    except Exception as e:
        logger.info
        raise e
    
    finally:
        cap.cap.release()
        cv2.destroyAllWindows()
        logger.warning("vison failed")


if __name__ == "__main__":
    vision_thread()

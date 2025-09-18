import cv2
from egon.modules.memory import ShortTermMem
from egon.modules.logger import logger
import mediapipe.python.solutions.hands as mphands
import mediapipe.python.solutions.face_detection as mpface
from google.protobuf.json_format import MessageToDict
import egon.config as ec
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class ObjectDetectionModel:
    def __init__(self):
        self.detection_result_list = []

        def result_callback(
            result: vision.ObjectDetectorResult,
            output_image: mp.Image,
            timestamp_ms: int,
        ):

            result.timestamp_ms = timestamp_ms
            self.detection_result_list.append(result)
            for detection in result.detections:
                ShortTermMem.add(detection.categories[0].category_name)

        model_file = open(ec.path_obj_detection, "rb")
        buff = model_file.read()
        model_file.close()

        base_options = python.BaseOptions(model_asset_buffer=buff)
        # base_options = python.BaseOptions(model_asset_path=ec.path_obj_detection, model_asset_buffer = buff)
        options = vision.ObjectDetectorOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            score_threshold=0.5,
            result_callback=result_callback,
        )
        self.detector = vision.ObjectDetector.create_from_options(options)

    def process(self, image, counter):
        # image = cv2.flip(image, 1)

        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Run object detection using the model.
        self.detector.detect_async(mp_image, counter)


# model_hands = mphands.Hands()
# model_face = mpface.FaceDetection()
from egon.modules.utils_visual import visualize_detection

model_obj = ObjectDetectionModel()


def run_hand_detection(img):
    res = model_hands.process(img)
    # logger.info(res.multi_hand_landmarks)
    # logger.info(res.multi_handedness)
    if res.multi_handedness:
        output = [
            MessageToDict(c)["classification"][0]["label"] for c in res.multi_handedness
        ]
        # logger.info(output)
        for h in output:
            ShortTermMem.add(key=f"hand {h}")


def run_face_detection(img):
    res = model_face.process(img)
    # logger.info(res.multi_hand_landmarks)
    if res.detections:
        output = [
            {
                d.label_id[0],
                d.score[0],
                d.location_data.relative_bounding_box.xmin,
                # d.location_data.relative_bounding_box.ymin,
                # d.location_data.relative_bounding_box.width,
                # d.location_data.relative_bounding_box.height,
            }
            for d in res.detections
        ]
        # logger.info(output)
        for f in output:
            ShortTermMem.add(key="face")


def vision_thread():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("poule")

    counter = 0
    rval, frame = cap.read()
    while rval:
        counter += 1
        rval, img = cap.read()

        model_obj.process(img, counter)

        cv2.imshow("poule", visualize_detection(img, model_obj.detection_result_list))

        model_obj.detection_result_list.clear()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    vision_thread()

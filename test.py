import cv2
from egon.modules.logger import logger
import time
from threading import Thread
import time

from scipy.io.wavfile import write
import sounddevice as sd
import time



def preprocess(img):
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return img

class VideoCapture:
    def capture_thread(self):
        while True:
            ret, self.frame = self.cap.read() 

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
        self.frame=None
        t = Thread(target=self.capture_thread,daemon=True)
        t.start()



def audioth():

    fs = 32000
    duration = 0.05
    while True:

        live_rec = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait(ignore_errors=False)  # Wait until recording is finished
        logger.info(live_rec)
        start_time = time.time()
        write("rec.wav", fs, live_rec)  # Save as WAV file

        inference_time = time.time() - start_time

        logger.info(inference_time)


def vision_thread():

    cap = VideoCapture()
    try:
    
        cv2.destroyAllWindows()
        cv2.namedWindow("poule")
        counter = 0
        start_time = time.time()
        frame = cap.frame
        while cap.frame is None:
            time.sleep(1)
            logger.info("cap.frame is None => sleep")

        t2 = Thread(target=audioth,daemon=True)
        t2.start()
        while True:
            
            counter += 1

            img = cap.frame.copy()
        
            img = preprocess(img)

            cv2.imshow("poule", img)

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

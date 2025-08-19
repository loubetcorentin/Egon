

import cv2
import mediapipe as mp
import time
from scipy.stats import bernoulli
import numpy as np
import random
import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
from sympy import quadratic_congruence
from glob import glob
from speechbrain.pretrained import EncoderASR
from onnx import numpy_helper
from PIL import Image
from matplotlib.pyplot import imshow
import onnxruntime as rt
from scipy import special
import math
from pydub import AudioSegment
from pydub.playback import play

from pyfirmata import Arduino,SERVO,util# Importer pyFirmata

from parameters import *
from yolofunctions import *

while True:
    try:

        """-----------------------------------------------------------------------
                                    ARDUINO 1
        -----------------------------------------------------------------------"""

        port = '/dev/ttyACM0'
        pin=9
        board=Arduino(port)
        board.digital[pin].mode=SERVO

        """
        sudo chmod a+rw /dev/ttyACM0
        """

        inMemory=False
        currentState="calm"

        with open('state.txt', 'w') as f:
            f.write(str([currentState,inMemory]))

        """-----------------------------------------------------------------------
                                    NEURAL NETWORKS
        -----------------------------------------------------------------------"""


        def hands_analysis(imgRGB):
            res=hands.process(imgRGB)
            if res.multi_hand_landmarks:#si on a detecte des choses
                if len(res.multi_handedness)==2 :#s'il y a deux mains
                    return "left_and_right"
                else :#s'il n'y en a qu'une, laquelle
                    if res.multi_handedness[0].classification[0].label=="Left":
                        return "left"
                    else :
                        return "right"
            else :
                return "none"
            
            
        def face_analysis(imgRGB):
            res=face_detection.process(imgRGB)
            if res.detections:
                
                return "face"
            else:
                return "none"


        def speech_analysis(duration):
            myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
            sd.wait()  # Wait until recording is finished
            write('real_voice.wav', fs, myrecording)  # Save as WAV file 

            wav = read_audio_vad('real_voice.wav', sampling_rate=16000)

            try:

                speech_timestamps = get_speech_timestamps_vad(wav, model_vad, sampling_rate=16000)

                save_audio_vad('real_voice.wav',
                        collect_chunks_vad(speech_timestamps, wav), sampling_rate=16000)
            except:
                print("empty sound sample")
            
            final_text = str(model_stt.transcribe_file("real_voice.wav"))
            final_text = final_text.lower()
            
            listOfWords = get_relevant_lemma(nlp(final_text))
            
            for i in listOfWords:
                if i in words:
                    return i

            return "none"



        def object_analysis(img):
        
            input_size = 416

            
            original_image = img
            original_image_size = original_image.shape[:2]

            image_data = image_preprocess(np.copy(original_image), [input_size, input_size])
            image_data = image_data[np.newaxis, ...].astype(np.float32)

            sess = rt.InferenceSession("yolov4.onnx")

            outputs = sess.get_outputs()
            output_names = list(map(lambda output: output.name, outputs))
            input_name = sess.get_inputs()[0].name

            detections = sess.run(output_names, {input_name: image_data})

            ANCHORS = "./yolov4_anchors.txt"
            STRIDES = [8, 16, 32]
            XYSCALE = [1.2, 1.1, 1.05]

            ANCHORS = get_anchors(ANCHORS)
            STRIDES = np.array(STRIDES)

            pred_bbox = postprocess_bbbox(detections, ANCHORS, STRIDES, XYSCALE)
            bboxes = postprocess_boxes(pred_bbox, original_image_size, input_size, 0.25)
            bboxes = nms(bboxes, 0.213, method='nms')
            
            return predict(original_image, bboxes)

        
        """-----------------------------------------------------------------------
                                    FUNCTIONS
        -----------------------------------------------------------------------"""
            

            
        def random_detection(startTime,duration):

            idx = random.choice([0,0,0,0,1,1,1,1,2,2])
            
            if idx == 0:
                print("waiting for hands")
                while time.time()-startTime<duration:
                    success, img = cap.read()
                    imgRGB=mini_image_processing(img)

                    det = hands_analysis(imgRGB)
                    if det != "none":
                        return det
                return "none"

            if idx == 1:
                print("waiting for object")
                while time.time()-startTime<duration:
                    success, img = cap.read()
                    imgRGB=mini_image_processing(img)
                    det = object_analysis(imgRGB)
                    if det != "none":
                        return det
                return "none"

            if idx == 2:
                res = speech_analysis(duration/2)
                if res == "none":
                    res = speech_analysis(duration/2)
                    return res
                else:
                    return res

            

        def random_forgetting(dur,step):#une fois sur 300 on enlève un element random au brain
            global inMemory
            global brain
            if len(brain)>0 and bernoulli.rvs((step*2/(dur)), size=1)[0] == 1:
                idx = random.randint(0,len(brain)-1)
                if brain[idx]=="face":
                    inMemory=False
                del brain[idx]
                
                
        def mini_image_processing(img):
            img=cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            img=cv2.flip(img, 1)
            #img.flags.writeable = False
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return imgRGB
            

        """-----------------------------------------------------------------------
                                    ONOMATOPEES
        -----------------------------------------------------------------------"""

        def get_relevant_lemma(tokens):
            return [token.lemma_ for token in tokens if not token.is_stop and not token.is_punct]


        def get_excited_ono():

            text1 = ""
            text2 = ""
            text3 = ""

            for i in range(random.randint(3, 5)):

                text1 = text1 + ("pi"*random.randint(1,5) + " ")*random.randint(0,1) 
                text1 = text1 + ("ta"*random.randint(1,5) + " ")*random.randint(0,1)
                text1 = text1 + ("ko"*random.randint(1,5) + " ")
                
            for i in range(random.randint(2, 3)):

                text2 = text2 + ("zwi"*random.randint(2,5) + " ")*random.randint(0,1) 
                text2 = text2 + ("yia"*random.randint(1,3) + " ")
                
            
            for i in range(random.randint(4,5)):
                text3 = text3 + ("ki"*random.randint(1,3) + " " + "qa"*random.randint(1,3) + " ")
                
                
            return [text1, text2, text3][random.randint(0,2)]


        def get_interested_ono():

            text = ""
            text2 = ""

            for i in range(random.randint(2, 5)):

                text = text + ("w"*random.randint(0,2) + "i"*random.randint(0,5) + " ")*random.randint(0,1)*random.randint(0,1) 
                text = text + ("z"*random.randint(0,2) + "o"*random.randint(0,5) + "u"*random.randint(0,5) + " ")*random.randint(0,1) 
                text = text + ("y"*random.randint(0,2) + "e"*random.randint(0,5) + "a"*random.randint(0,5) + " ")*random.randint(0,1)
                text = text + ("b"*random.randint(1,1) + "e"*random.randint(0,5) + "p"*random.randint(0,5) + " ")
                
            for i in range(random.randint(2,4)):
                #ergherghergh oooooo aaaaaaaaaaa
                text2 = text2 + ("ergh"*random.randint(1,3) + " ")*random.randint(0,1)
                text2 = text2 + ("o"*random.randint(3,5) + " " + "a"*random.randint(3,5) + " ")

            return [text, text2][random.randint(0,1)]


        def get_bored_ono():

            text1 = ""
            text2 = ""
            text3 = ""
            text4 = ""
            text5 = ""

            for i in range(random.randint(2, 3)):

                text1 = text1 + ("m"*random.randint(1,1) + "a"*random.randint(1,3) + "h"*random.randint(2,5) + ","*random.randint(1,2) + " ")*random.randint(0,1) 
                text1 = text1 + ("m"*random.randint(5,15) + " ")*random.randint(0,1)
                text1 = text1 + ("m"*random.randint(1,1) + "u"*random.randint(1,3) + "h"*random.randint(2,5) + ","*random.randint(1,2) + " ")*random.randint(0,1)
                text1 = text1 + ("m"*random.randint(1,1) + "o"*random.randint(1,3) + "h"*random.randint(2,5) + ","*random.randint(1,2) + " ")*random.randint(0,1)
                text1 = text1 + ("n"*random.randint(5,15) + " ")
            

            for i in range(random.randint(2, 3)):

                text2 = text2 + ("tick"*random.randint(1,1) + "."*random.randint(1,2) + " " + "tock"*random.randint(1,1) + "."*random.randint(1,2) + " ")
                
            for i in range(random.randint(3, 5)):

                text3 = text3 + ("m"*random.randint(5,10) + " ")*random.randint(0,1)
                text3 = text3 + ("n"*random.randint(5,10) + " ")
                
            for i in range(random.randint(3, 5)):
                text4 = text4 + ("f"*random.randint(5,10) + " ")*random.randint(0,1)
                text4 = text4 + ("v"*random.randint(5,10) + " ")
                
            for i in range(random.randint(3, 5)):
                
                text5 = text5 + ("k"*random.randint(5,10) + " ")*random.randint(0,1)
                text5 = text5 + ("r"*random.randint(5,10) + " ")
                
            return [text1, text2, text3, text4, text5][random.randint(0,4)]


        def outloud(text):
            audio_paths = model_tts.save_wav(text=text,
                                        speaker=speaker,
                                        sample_rate=sample_rate)

                
            song = AudioSegment.from_wav("test.wav")
            play(song)




        """-----------------------------------------------------------------------
                                        MOTOR
        -----------------------------------------------------------------------"""


        def rotateservo(pin,angle):
            board.digital[pin].write(angle)

        def rotate_one_degree():
        
            global rotation_direction
            global rotation_angle
            print(rotation_angle,rotation_direction)
            if rotation_direction == "left":
                if rotation_angle < 170 :#bord gauche non atteint
                    rotation_angle += 1#on continue vers la gauche
                    rotateservo(pin,rotation_angle)
                    
                else :#changement de direction
                    rotation_angle -= 1
                    rotateservo(pin,rotation_angle)
                    rotation_direction = "right"
                    
            else :#vers la droite
                if rotation_angle > 10 :#bord droit non atteint
                    rotation_angle -= 1#on continue vers la droite
                    rotateservo(pin,rotation_angle)
                    
                else :#changement de direction
                    rotation_angle += 1
                    rotateservo(pin,rotation_angle)
                    rotation_direction = "left"




        def excited_movement(movement_amplitude):
            print("excited movement")
            global rotation_angle

            quickstep=0.03
            for i in range(0,int(movement_amplitude/2)):#gauche
                rotation_angle += 1
                rotateservo(pin,rotation_angle)
                time.sleep(quickstep)
            for i in range(0,movement_amplitude):#droite
                rotation_angle -= 1
                rotateservo(pin,rotation_angle)
                time.sleep(quickstep)
            for i in range(0,movement_amplitude):#gauche
                rotation_angle += 1
                rotateservo(pin,rotation_angle)
                time.sleep(quickstep)
            for i in range(0,movement_amplitude):#droite
                rotation_angle -= 1
                rotateservo(pin,rotation_angle)
                time.sleep(quickstep)
            for i in range(0,movement_amplitude):#gauche
                rotation_angle += 1
                rotateservo(pin,rotation_angle)
                time.sleep(quickstep)
            for i in range(0,movement_amplitude):#droite
                rotation_angle -= 1
                rotateservo(pin,rotation_angle)
                time.sleep(quickstep)
            for i in range(0,movement_amplitude):#gauche
                rotation_angle += 1
                rotateservo(pin,rotation_angle)
                time.sleep(quickstep)
            for i in range(0,int(movement_amplitude/2)):#droite
                rotation_angle -= 1
                rotateservo(pin,rotation_angle)
                time.sleep(quickstep)


            
        """-----------------------------------------------------------------------
                                        MAIN LOOP
        -----------------------------------------------------------------------"""
        cap = cv2.VideoCapture(2)
        #ret,frame=cap.read()
        #cv2.imshow("frame",frame)
        person_detected = False
        step=0.1

        while True:
            print(brain)
            #Calm mode
            currentState="calm"
            with open('state.txt', 'w') as f:
                #print("on ecrit qu'on est calme ?")
                f.write(str([currentState,inMemory]))

            startRotation = time.time()
            duration_min=random.randint(3, 7)
            
        
            #Pendant un certain temps duration_min, on tourne sans rien scanner
            while(time.time()-startRotation < duration_min):
                print(brain)
                rotate_one_degree()
                random_forgetting(duration_min,step)
                if bernoulli.rvs(step/(duration_min*2), size=1)[0] == 1:
                    outloud(get_bored_ono())
                time.sleep(step)

                    
            

        
            while person_detected == False:
                print(brain)
                rotate_one_degree()
                
                #new frame
                success, img = cap.read()
                imgRGB=mini_image_processing(img)
                
                #nouvelle analyse de visage pour voir s'il y a une personne
                before_detection=time.time()
                detection = face_analysis(imgRGB)
                detection_time=time.time()-before_detection

                #customStep=step*500-detection_time

                if detection == "face":
                    
                    if bernoulli.rvs(1/5, size=1)[0] == 1:
                        print("INTERESTED")
                        currentState="interested"
                        inMemory=True
                        print(currentState)
                        with open('state.txt', 'w') as f:
                            f.write(str([currentState,inMemory]))
                        
                        outloud(get_interested_ono())
                    
                        person_detected = True

                
            

            detection_trials=0
            while detection_trials < 3:
            
                #Une personne est détectée, on capture une image et on lance des ia random
                detection=random_detection(time.time(),duration_min)

                if detection != "none":#il y a une detection
                    
                    if detection in brain:#si on l'a deja vue
                        print(detection," BORED")#on reste encore un peu devant
                        currentState="calm"
                        with open('state.txt', 'w') as f:
                            f.write(str([currentState,inMemory]))
                        
                        outloud(get_bored_ono())
                        person_detected = False #on sort de la boucle
                        
                    else:#nouvelle detection, on l'ajoute au brain
                        print(detection," EXCITED")
                        currentState="excited"
                        with open('state.txt', 'w') as f:
                            f.write(str([currentState,inMemory]))
                        
                        excited_movement(10)
                        brain.append(detection)
                        outloud(get_excited_ono())

                        time.sleep(3)#on se laisse du temps avant de scanner a nouveau
                detection_trials+=1
            
            

            #cv2.imshow("Image", img)
            if cv2.waitKey(1) == ord("q"):
                break
                
                
                
        cap.release()
        cv2.destroyAllWindows()
    
    except:

        print("error loop")






















'''
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        
        for handLms in results.multi_hand_landmarks:
            print(hands_analysis(results.multi_handedness))
            for id, lm in enumerate(handLms.landmark):
                
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    '''



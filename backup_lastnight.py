

import cv2
import mediapipe as mp
import time
import scipy
from scipy.stats import bernoulli
import numpy as np
import random
import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
from sympy import quadratic_congruence
import torch
import zipfile
import torchaudio
from glob import glob
from speechbrain.pretrained import EncoderASR
import onnx
from onnx import numpy_helper
import spacy
import fr_core_news_sm
import os
from PIL import Image
from matplotlib.pyplot import imshow
import onnxruntime as rt
from scipy import special
import colorsys
import math
from pydub import AudioSegment
from pydub.playback import play

from pyfirmata import Arduino,SERVO,util# Importer pyFirmata

"""-----------------------------------------------------------------------
                               ARDUINO
-----------------------------------------------------------------------"""

port = '/dev/ttyACM0'
pin=9
board=Arduino(port)
board.digital[pin].mode=SERVO

"""
sudo chmod a+rw /dev/ttyACM0
"""

port2 = '/dev/ttyACM1'
board2 = Arduino(port2)
pin1 = [board2.get_pin('d:10:p'),board2.get_pin('d:9:p'),board2.get_pin('d:11:p')]
pin2 = [board2.get_pin('d:5:p'),board2.get_pin('d:6:p'),board2.get_pin('d:3:p')]
currentState = "transition"
breathTime = 180
oxygen = 0.0
breathing = True
heartbeatTime = 0
bloodPressure = 0.0
excitement = 1.0
thinkTime = 0
cognitiveLoad = 0
inMemory = True
transitionTime = 0
memory = 0.0
nextState = "excited"
excitedTime = 0

"""-----------------------------------------------------------------------
                             GLOBAL PARAMETERS
-----------------------------------------------------------------------"""

# SYSTEM PARAMETERS
brain = []
rotation_angle = 0 #more like angle
rotation_direction = "left"


# HANDS PARAMETERS
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0


# FACE PARAMETERS
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5)

# VOICE ACTIVATED DETECTION
model_vad, utils_vad = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True,
                              onnx=True)

(get_speech_timestamps_vad,
 save_audio_vad,
 read_audio_vad,
 VADIterator_vad,
 collect_chunks_vad) = utils_vad

# SPEECH TO TEXT PARAMETERS
words=['abject',
 'abominable',
 'affreux',
 'affété',
 'agacement',
 'agréable',
 'allégresse',
 'alors',
 'amertume',
 'art',
 'artificiel',
 'astronomique',
 'atroce',
 'attractif',
 'baisage',
 'baise',
 'baiser',
 'beau',
 'beauté',
 'beaux-arts',
 'belle',
 'bien',
 'bien de consommation courante',
 'bon',
 'bon mot',
 'bonheur',
 'calculateur',
 'calomnier',
 'caméra',
 'cher',
 'colère',
 'complètement',
 'connaissance',
 'content',
 'contenu',
 'convenable',
 'cool',
 'correct',
 'coupon',
 'coûteux',
 'craindre',
 'crainte',
 'création artistique',
 'curieux',
 'denrée',
 'diffamer',
 'difficile',
 'directement',
 'droit',
 'drôle',
 'décent',
 'détestable',
 'efficace',
 'effroi',
 'empirer',
 'emprunté',
 'en forme',
 'en même temps',
 'entier',
 'entièrement',
 'estimable',
 'euphorique',
 'exposition',
 'fameux',
 'fin',
 'foutre',
 'frais',
 'frisquet',
 'fureur',
 'félicité',
 'féroce',
 'gai',
 'galactique',
 'gigantesque',
 'grand',
 'graphique',
 'graphisme',
 'généreux',
 'heureux',
 'hideux',
 'honnir',
 'horrible',
 'humour',
 'illustration',
 'indignation',
 'infâme',
 'inintéressant',
 'insulter',
 'intelligence',
 'intégralement',
 'intéressant',
 'intérêt',
 'ira',
 'ire',
 'irritation',
 'irréel',
 'joie',
 'juste',
 'justement',
 'laid',
 'largement',
 'larme',
 'lisse',
 'machine',
 'machine simple',
 'magnifique',
 'mal',
 'malheur',
 'marchandise',
 'mauvais',
 'meilleur',
 'merde',
 'moche',
 'mot',
 "mot d'esprit",
 'notoire',
 'nul',
 'odieux',
 'ordinateur',
 'ordinateur portable',
 'parfaitement',
 'perspective',
 'peur',
 'plaisant',
 'plaisir',
 'plein',
 'pleinement',
 'pleur',
 'pleurer',
 'portable',
 'positif',
 'produit',
 'profond',
 'profondément',
 'propice',
 'propriété',
 'précieux',
 'puissant',
 'putain',
 'rancune',
 'rancœur',
 'redouter',
 'repoussant',
 'ressentiment',
 'riche',
 'richement',
 'risqué',
 'robuste',
 'répugnant',
 'sage',
 'sain',
 'satisfaisant',
 'satisfait',
 'sentiment',
 'service de renseignement',
 'service de renseignements',
 'singulier',
 'soucier',
 'spéculatif',
 'strictement positif',
 'suffisant',
 'sérieux',
 'sûr',
 'tard',
 'ticket-restaurant',
 'tort',
 'totalement',
 'toucher',
 'tout',
 'tout à fait',
 'tranchée',
 'tristesse',
 'vertueux',
 'viril',
 'vis',
 'vision',
 'vraiment',
 'vue',
 'zéro',
 'éminent',
 'émotion',
 'énorme',
 'épine',
 'épouvantable',
 'épouvante',
 "test",
 "tourner",
 "joli",
 "beau",
 "entendre",
 "bonjour",
 "salut",
 "art",
 "paris",
 "mot",
 "magnifique",
 "gallerie"]
fs = 16000  # Sample rate
device = torch.device('cpu')
model_stt = EncoderASR.from_hparams(source="speechbrain/asr-wav2vec2-commonvoice-fr", savedir="pretrained_models/asr-wav2vec2-commonvoice-fr")
nlp = fr_core_news_sm.load()
spacy.require_cpu() 


# TEXT TO SPEECH PARAMETERS
language = 'en'
model_id = 'v3_en'
sample_rate = 48000
speaker = 'en_1'
model_tts, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)                            
model_tts.to(device)  # gpu or cpu



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
    
def outloud(text):
    audio_paths = model_tts.save_wav(text=text,
                                 speaker=speaker,
                                 sample_rate=sample_rate)

        
    song = AudioSegment.from_wav("test.wav")
    play(song)



    
    
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
        print("waiting for speech")
        res = speech_analysis(duration/2)
        if res == "none":
            res = speech_analysis(duration/2)
            return res
        else:
            return res

    

def random_forgetting(dur,step):#une fois sur 300 on enlève un element random au brain
    global brain
    if len(brain)>0 and bernoulli.rvs((1/50), size=1)[0] == 1:
        idx = random.randint(0,len(brain)-1)
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


"""-----------------------------------------------------------------------
                              LED FUNCTIONS
-----------------------------------------------------------------------"""


def think():
    global thinkTime, excitement
    if thinkTime == 0:
        thinkTime = 160
    thinkTime -= 1
    interest = (excitement + math.sin(2.0*math.pi/80.0*float(thinkTime))*excitement)
    interest2 = (excitement + math.sin(math.pi/2.0+2.0*math.pi/80.0*float(thinkTime))*excitement)
    cognitiveLoad = interest
    pin2[0].write((cognitiveLoad+interest2)/2.0)
    pin2[1].write(cognitiveLoad)
    pin2[2].write(interest2/2.0)
    #analogWrite(PIN_LED_1[0], (int)(cognitiveLoad+interest2)/2.0);
    #analogWrite(PIN_LED_1[1], cognitiveLoad);
    #analogWrite(PIN_LED_1[2], interest2);

def transition(pin, duration, t):
    global transitionTime, currentState
    if (t <= duration):
        v = .5+(.5/(t*0.1))*math.sin(math.pi/10.0*float(t))
        pin.write(v)
    else:
        transitionTime = 1
        currentState = nextState

def breathe():
    global oxygen, excitement, breathTime, breathing
    if breathTime == 0:
        breathTime = random.randint(int(180-excitement*200), int(200-excitement*200))
        breathing = not breathing
    if breathing:
        oxygen = constrain(oxygen + 0.01,0,1) #+excitement/2000.0
    else:
        oxygen = constrain(oxygen - 0.02,0,1) 
    breathTime-=1
    pin1[2].write(constrain(oxygen,0,1))

def beat():
    global heartbeatTime, excitement, bloodPressure
    if (heartbeatTime == 20 - int(excitement*5)): 
        bloodPressure = 20
    if (heartbeatTime == 0):
        heartbeatTime = 150-int(excitement*10)
        bloodPressure = 100
    heartbeatTime-=1
    bloodPressure = bloodPressure * 0.8
    pin1[0].write(constrain(bloodPressure, 0, 255)/255.0)

def goLoco():
    global excitedTime

    v1 = constrain(math.sin(float(excitedTime)*.2*excitement),0,1)*.5
    v2 = constrain(math.sin(math.pi/3.0+float(excitedTime)*.2*excitement),0,1)*.5
    blue = .5*constrain(math.sin(float(excitedTime)*.5*excitement),0.0,1.0)*constrain(math.sin(float(excitedTime)*.04*excitement),0.0,1.0)
    yellow = constrain(excitedTime/10000,0.0,1.0)*.5
    pin1[0].write(v2+yellow)
    pin1[1].write(yellow)
    pin1[2].write(v2+blue)
    pin2[0].write(v1+yellow)
    pin2[1].write(yellow)
    pin2[2].write(v1+blue)



def constrain(v, mini, maxi):
    return max(min(v,maxi),mini)


def lights():
    global excitement,currentState,pin1,pin2,transitionTime,excitedTime,memory,inMemory
    
    if currentState == "transition":
        transitionTime += 1
        transition(pin2[0], 80, transitionTime);
        transition(pin2[1], 80, transitionTime);
        transition(pin2[2], 80, transitionTime);

    elif currentState == "calm":
        excitement = constrain(excitement-0.001,0,1)
        breathe()
        beat()
        think()

    elif currentState == "interested":
        excitement = constrain(excitement + 0.001, 0, .5)
        think()
        breathe()
        beat()
        if (inMemory):
            memory = constrain(memory+.01,0,1)
        else:
            memory = constrain(memory-.01,0,1)
        pin1[1].write(memory)

    elif currentState == "excited":
        excitement = constrain(excitement + 0.01, 0, 1.0)
        excitedTime+=1
        goLoco()
"""-----------------------------------------------------------------------
                             YOLO FUNCTIONS
-----------------------------------------------------------------------"""




def image_preprocess(image, target_size, gt_boxes=None):

    ih, iw = target_size
    h, w, _ = image.shape

    scale = min(iw/w, ih/h)
    nw, nh = int(scale * w), int(scale * h)
    image_resized = cv2.resize(image, (nw, nh))

    image_padded = np.full(shape=[ih, iw, 3], fill_value=128.0)
    dw, dh = (iw - nw) // 2, (ih-nh) // 2
    image_padded[dh:nh+dh, dw:nw+dw, :] = image_resized
    image_padded = image_padded / 255.

    if gt_boxes is None:
        return image_padded

    else:
        gt_boxes[:, [0, 2]] = gt_boxes[:, [0, 2]] * scale + dw
        gt_boxes[:, [1, 3]] = gt_boxes[:, [1, 3]] * scale + dh
        return image_padded, gt_boxes

def get_anchors(anchors_path, tiny=False):
    '''loads the anchors from a file'''
    with open(anchors_path) as f:
        anchors = f.readline()
    anchors = np.array(anchors.split(','), dtype=np.float32)
    return anchors.reshape(3, 3, 2)

def postprocess_bbbox(pred_bbox, ANCHORS, STRIDES, XYSCALE=[1,1,1]):
    '''define anchor boxes'''
    for i, pred in enumerate(pred_bbox):
        conv_shape = pred.shape
        output_size = conv_shape[1]
        conv_raw_dxdy = pred[:, :, :, :, 0:2]
        conv_raw_dwdh = pred[:, :, :, :, 2:4]
        xy_grid = np.meshgrid(np.arange(output_size), np.arange(output_size))
        xy_grid = np.expand_dims(np.stack(xy_grid, axis=-1), axis=2)

        xy_grid = np.tile(np.expand_dims(xy_grid, axis=0), [1, 1, 1, 3, 1])
        xy_grid = xy_grid.astype(float)

        pred_xy = ((special.expit(conv_raw_dxdy) * XYSCALE[i]) - 0.5 * (XYSCALE[i] - 1) + xy_grid) * STRIDES[i]
        pred_wh = (np.exp(conv_raw_dwdh) * ANCHORS[i])
        pred[:, :, :, :, 0:4] = np.concatenate([pred_xy, pred_wh], axis=-1)

    pred_bbox = [np.reshape(x, (-1, np.shape(x)[-1])) for x in pred_bbox]
    pred_bbox = np.concatenate(pred_bbox, axis=0)
    return pred_bbox

def postprocess_boxes(pred_bbox, org_img_shape, input_size, score_threshold):
    '''remove boundary boxs with a low detection probability'''
    valid_scale=[0, np.inf]
    pred_bbox = np.array(pred_bbox)

    pred_xywh = pred_bbox[:, 0:4]
    pred_conf = pred_bbox[:, 4]
    pred_prob = pred_bbox[:, 5:]

    # # (1) (x, y, w, h) --> (xmin, ymin, xmax, ymax)
    pred_coor = np.concatenate([pred_xywh[:, :2] - pred_xywh[:, 2:] * 0.5,
                                pred_xywh[:, :2] + pred_xywh[:, 2:] * 0.5], axis=-1)
    # # (2) (xmin, ymin, xmax, ymax) -> (xmin_org, ymin_org, xmax_org, ymax_org)
    org_h, org_w = org_img_shape
    resize_ratio = min(input_size / org_w, input_size / org_h)

    dw = (input_size - resize_ratio * org_w) / 2
    dh = (input_size - resize_ratio * org_h) / 2

    pred_coor[:, 0::2] = 1.0 * (pred_coor[:, 0::2] - dw) / resize_ratio
    pred_coor[:, 1::2] = 1.0 * (pred_coor[:, 1::2] - dh) / resize_ratio

    # # (3) clip some boxes that are out of range
    pred_coor = np.concatenate([np.maximum(pred_coor[:, :2], [0, 0]),
                                np.minimum(pred_coor[:, 2:], [org_w - 1, org_h - 1])], axis=-1)
    invalid_mask = np.logical_or((pred_coor[:, 0] > pred_coor[:, 2]), (pred_coor[:, 1] > pred_coor[:, 3]))
    pred_coor[invalid_mask] = 0

    # # (4) discard some invalid boxes
    bboxes_scale = np.sqrt(np.multiply.reduce(pred_coor[:, 2:4] - pred_coor[:, 0:2], axis=-1))
    scale_mask = np.logical_and((valid_scale[0] < bboxes_scale), (bboxes_scale < valid_scale[1]))

    # # (5) discard some boxes with low scores
    classes = np.argmax(pred_prob, axis=-1)
    scores = pred_conf * pred_prob[np.arange(len(pred_coor)), classes]
    score_mask = scores > score_threshold
    mask = np.logical_and(scale_mask, score_mask)
    coors, scores, classes = pred_coor[mask], scores[mask], classes[mask]

    return np.concatenate([coors, scores[:, np.newaxis], classes[:, np.newaxis]], axis=-1)

def bboxes_iou(boxes1, boxes2):
    '''calculate the Intersection Over Union value'''
    boxes1 = np.array(boxes1)
    boxes2 = np.array(boxes2)

    boxes1_area = (boxes1[..., 2] - boxes1[..., 0]) * (boxes1[..., 3] - boxes1[..., 1])
    boxes2_area = (boxes2[..., 2] - boxes2[..., 0]) * (boxes2[..., 3] - boxes2[..., 1])

    left_up       = np.maximum(boxes1[..., :2], boxes2[..., :2])
    right_down    = np.minimum(boxes1[..., 2:], boxes2[..., 2:])

    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area    = inter_section[..., 0] * inter_section[..., 1]
    union_area    = boxes1_area + boxes2_area - inter_area
    ious          = np.maximum(1.0 * inter_area / union_area, np.finfo(np.float32).eps)

    return ious

def nms(bboxes, iou_threshold, sigma=0.3, method='nms'):
    """
    :param bboxes: (xmin, ymin, xmax, ymax, score, class)

    Note: soft-nms, https://arxiv.org/pdf/1704.04503.pdf
          https://github.com/bharatsingh430/soft-nms
    """
    classes_in_img = list(set(bboxes[:, 5]))
    best_bboxes = []

    for cls in classes_in_img:
        cls_mask = (bboxes[:, 5] == cls)
        cls_bboxes = bboxes[cls_mask]

        while len(cls_bboxes) > 0:
            max_ind = np.argmax(cls_bboxes[:, 4])
            best_bbox = cls_bboxes[max_ind]
            best_bboxes.append(best_bbox)
            cls_bboxes = np.concatenate([cls_bboxes[: max_ind], cls_bboxes[max_ind + 1:]])
            iou = bboxes_iou(best_bbox[np.newaxis, :4], cls_bboxes[:, :4])
            weight = np.ones((len(iou),), dtype=np.float32)

            assert method in ['nms', 'soft-nms']

            if method == 'nms':
                iou_mask = iou > iou_threshold
                weight[iou_mask] = 0.0

            if method == 'soft-nms':
                weight = np.exp(-(1.0 * iou ** 2 / sigma))

            cls_bboxes[:, 4] = cls_bboxes[:, 4] * weight
            score_mask = cls_bboxes[:, 4] > 0.
            cls_bboxes = cls_bboxes[score_mask]

    return best_bboxes


def read_class_names(class_file_name):
    '''loads class name from a file'''
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names






def predict(image, bboxes, classes=read_class_names("coco.names"), show_label=True):
    """
    bboxes: [x_min, y_min, x_max, y_max, probability, cls_id] format coordinates.
    """
    
    final_classes = list()

    num_classes = len(classes)
    image_h, image_w, _ = image.shape
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

    random.seed(0)
    random.shuffle(colors)
    random.seed(None)

    for i, bbox in enumerate(bboxes):
        coor = np.array(bbox[:4], dtype=np.int32)
        fontScale = 0.5
        score = bbox[4]
        class_ind = int(bbox[5])
        bbox_color = colors[class_ind]
        bbox_thick = int(0.6 * (image_h + image_w) / 600)
        c1, c2 = (coor[0], coor[1]), (coor[2], coor[3])
        cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)

        if show_label:
            bbox_mess = '%s: %.2f' % (classes[class_ind], score)
            t_size = cv2.getTextSize(bbox_mess, 0, fontScale, thickness=bbox_thick//2)[0]
            cv2.rectangle(image, c1, (c1[0] + t_size[0], c1[1] - t_size[1] - 3), bbox_color, -1)
            cv2.putText(image, bbox_mess, (c1[0], c1[1]-2), cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale, (0, 0, 0), bbox_thick//2, lineType=cv2.LINE_AA)
            
        if classes[class_ind] in ["tie", "handbag", "cell phone", "backpack", "bottle", "wine glass", "cup", "tie"
, "suitcase"]:
            final_classes.append(classes[class_ind])
    
    if len(final_classes)>0:
        return final_classes[random.randint(0, len(final_classes)-1)]
    else:
        return "none"


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
        if rotation_angle > 0 :#bord droit non atteint
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
cap = cv2.VideoCapture(0)

person_detected = False
step=0.1

while True:
    
    #Calm mode
    currentState="calm"
    lights()
    time.sleep(10)

    startRotation = time.time()
    duration_min=random.randint(3, 7)
    
    
    #Pendant un certain temps duration_min, on tourne sans rien scanner
    while(time.time()-startRotation < duration_min):
        rotate_one_degree()
        
        random_forgetting(duration_min,step)
        if bernoulli.rvs(step/(duration_min*2), size=1)[0] == 1:
            outloud(get_bored_ono())
        time.sleep(step)


    while person_detected == False:
        
        rotate_one_degree()
        

        #new frame
        success, img = cap.read()
        imgRGB=mini_image_processing(img)
        
        #nouvelle analyse de visage pour voir s'il y a une personne
        before_detection=time.time()
        detection = face_analysis(imgRGB)
        detection_time=time.time()-before_detection

        customStep=step-detection_time

        if detection == "face":
            if bernoulli.rvs(1/5, size=1)[0] == 1:
                print("INTERESTED")
                currentState="interested"
                lights()
                time.sleep(10)
                outloud(get_interested_ono())
                person_detected = True
        time.sleep(customStep)

   

    detection_trials=[]
        
    while len(detection_trials) < 3:
            
        #Une personne est détectée, on capture une image et on lance des ia random
        detection=random_detection(time.time(),duration_min)
        
        detection_trials.append(detection)

        if detection != "none":#il y a une detection
            
            if detection in brain:#si on l'a deja vue
                print(detection," BORED")#on reste encore un peu devant
                currentState="calm"
                lights()
                time.sleep(10)
                outloud(get_bored_ono())
                person_detected = False #on sort de la boucle
                
            else:#nouvelle detection, on l'ajoute au brain
                print(detection," EXCITED")
                currentState="excited"
                lights()
                time.sleep(10)
                excited_movement(14)
                brain.append(detection)
                outloud(get_excited_ono())

                time.sleep(3)#on se laisse du temps avant de scanner a nouveau
            
    
    #cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("q"):
        break
        
        
        
cap.release()
cv2.destroyAllWindows()






















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




import mediapipe as mp
from scipy.stats import bernoulli
import numpy as np
import random
import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
from sympy import quadratic_congruence
import torch
from glob import glob
from speechbrain.pretrained import EncoderASR
from onnx import numpy_helper
import spacy
import fr_core_news_sm
from PIL import Image
from matplotlib.pyplot import imshow
import onnxruntime as rt
from scipy import special
from pydub import AudioSegment
from pydub.playback import play

from pyfirmata import Arduino,SERVO,util# Importer pyFirmata






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
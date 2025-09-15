"""
The Voice of Egon
The Voice class is responsible for generating and playing audio output.
the generation is done using snakers4/silero-models that is downloaded once and then stored in cache on the computer.
Generated voicelines are saved as .wav files in the audio_files folder. That way repeated lines do not need to be generated multiple times.
I used the pygame library to play the sounds. Probably overkill but better than the other libraries I tried.
"""

from pygame.mixer import Sound, init
import torch
from modules.logger import logger
import os.path

import random
class Voice:

    MODEL = None

    language = "en"
    model_id = "v3_en"
    sample_rate = 48000
    speaker = "en_1"
    device = torch.device("cpu")

    @classmethod
    def init_voice(cls):
        init()

        cls.MODEL, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-models",
            model="silero_tts",
            language=cls.language,
            speaker=cls.model_id,
        )
        cls.MODEL.to(cls.device)

    @classmethod
    def play_wav(cls, path="test.wav"):
        Sound(path).play()

    @classmethod
    def say(cls, str):
        logger.info(f"💅👁️👄👁️ 💅 💬 {str}")

        audio_path = f"audio_files/{str}.wav"

        if not os.path.isfile(audio_path):
            logger.info("creating new .wav")
            cls.MODEL.save_wav(
                text=str,
                audio_path=audio_path,
                speaker=cls.speaker,
                sample_rate=cls.sample_rate,
            )

        cls.play_wav(audio_path)


Voice.init_voice()


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


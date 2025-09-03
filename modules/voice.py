""" """

from pygame.mixer import Sound, init
import torch
from modules.logger import logger
import os.path


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

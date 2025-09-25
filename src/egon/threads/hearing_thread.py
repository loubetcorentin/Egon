import time
from egon.modules.console_utils import ConsoleTable
from egon.modules.emotional_state import EmotionalState
from egon.modules.logger import logger

BRAIN = EmotionalState.SM
from speechbrain.inference.ASR import EncoderASR
from speechbrain.inference import LocalStrategy

from scipy.io.wavfile import write
import sounddevice as sd
import time
import torch

logger.info(f"torch.cuda.is_available() : {torch.cuda.is_available()}")

asr_model = EncoderASR.from_hparams(
    source="speechbrain/asr-wav2vec2-commonvoice-fr",
    savedir="models/speechbrainASR",
    # huggingface_cache_dir="models/speechbrainASR/cache",
    local_strategy=LocalStrategy.COPY,
    
)


def hearing_thread():

    ct = ConsoleTable("👂👂", index=7)
    ct.d["rec"] = "init"
    logger.debug(ct.d)

    fs = 16000
    duration = 2

    ct.d["fs"] = f"{fs}"
    ct.d["duration"] = f"{duration}"
    ct.d["rec"] = "off"
    ct.d["heard"] = ""
    logger.debug(ct.d)

    while BRAIN.current_state == BRAIN.waking and __name__ != "__main__":
        time.sleep(1)

    logger.debug(ct.d)
    while True:
        
        ct.d["rec"] = "listening"
        live_rec = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        ct.d["rec"] = "infering"
        start_time = time.time()
        write("rec.wav", fs, live_rec)  # Save as WAV file
        res = asr_model.transcribe_file("rec.wav")
        ct.d["heard"] = f"{ct.d["heard"]} {res}"[-35:]
        logger.info(f"👂🥚👂 : {res}")
        inference_time = time.time() - start_time
        ct.d["T inference"] = f"{inference_time: 5.02f}s"


if __name__ == "__main__":
    hearing_thread()

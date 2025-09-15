"""This thread manages the actual decision making of Egon.
It links the outputs of the sensors in the Short Term Memory to the emotional state and actions.
"""

from modules.short_term_memory import ShortTermMem
from modules.emotional_state import EmotionalState
from modules.voice import Voice, get_excited_ono , get_bored_ono
from modules.logger import logger
from time import sleep
from random import randint


def brain_thread():

    brain = EmotionalState.SM

    while True:
        sleep(0.4)
        # logger.info(f"🧠 {brain.current_state}")

        match brain.current_state:
            case brain.waking:
                if randint(0, 100) < 30:
                    brain.drink_coffe()
                    Voice.say("aah coffee. What a treat")

            case brain.searching:
                if ShortTermMem.get_vision_output():
                    # Voice.say("oh")
                    ono = get_excited_ono()
                    Voice.say(ono)
                    brain.see_someone()
                else:
                    if randint(0, 100) < 30:
                        pass

            case brain.excited:
                if randint(0, 100) < 15:
                    ono = get_bored_ono()
                    Voice.say(ono)
                    
                    # Voice.say("meh")
                    brain.get_bored()


if __name__ == "__main__":  # for debugging
    brain_thread()

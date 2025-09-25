"""This thread manages the actual decision making of Egon.
It links the outputs of the sensors in the Short Term Memory to the emotional state and actions.
"""

from egon.modules.memory import ShortTermMem, LongTermMem
from egon.modules.emotional_state import EmotionalState
from egon.modules.voice import Voice, get_excited_ono, get_bored_ono
from egon.modules.motor_control import Neck
from egon.modules.logger import logger
from time import sleep
from random import randint, sample


BRAIN = EmotionalState.SM


def do_I_like(key):
    long_mem = LongTermMem.get_long_term_mem()

    if key in long_mem:
        # bad ending
        logger.info("nul")
        BRAIN.get_disapointed()
        ono = get_bored_ono()
        Voice.say(ono)
        sleep(10)
    else:
        # new this is good
        logger.info("coool")
        LongTermMem.add(key)
        ShortTermMem.remove(key)
        BRAIN.get_excited()
        ono = get_excited_ono()
        Voice.say(ono)


def search():
    mem = ShortTermMem.get_short_term_mem()

    # someone is there
    if "person" in mem.keys() and mem["person"] > 20:
        selected_key = sample(sorted(mem.keys()), 1)[0]
        if mem[selected_key] > 20:
            do_I_like(selected_key)


def brain_thread():

    Voice.init_voice()
    Neck.init_neck()

    while True:
        sleep(0.4)

        match BRAIN.current_state:
            case BRAIN.waking:
                sleep(1)
                Voice.say("I'M UP BITCH")
                Neck.act_no()
                BRAIN.drink_coffe()
                # if randint(0, 100) < 30:
                #     BRAIN.drink_coffe()
                #     Voice.say("aah coffee. What a treat")
                #     Neck.act_no()

            case BRAIN.searching:

                search()

            case BRAIN.excited:
                if randint(0, 100) < 15:

                    # Voice.say("meh")
                    BRAIN.get_bored()

            case BRAIN.disapointed:
                Neck.act_no()
                BRAIN.try_again()


if __name__ == "__main__":  # for debugging
    brain_thread()

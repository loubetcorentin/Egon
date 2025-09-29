"""This thread manages the actual decision making of Egon.
It links the outputs of the sensors in the Short Term Memory to the emotional state and actions.
"""

from egon.modules.memory import ShortTermMem, LongTermMem
from egon.modules.emotional_state import EmotionalState as BRAIN
from egon.modules.voice import Voice, get_excited_ono, get_bored_ono
from egon.modules.motor_control import Neck
from egon.modules.logger import logger
from time import sleep
from random import randint, sample




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


    while True:
        sleep(0.4)

        match BRAIN.SM.current_state:
            case BRAIN.SM.waking:
                sleep(1)
                Voice.say("I'M UP BITCH")
                # Neck.act_no()
                BRAIN.drink_coffe()
                
                # if randint(0, 100) < 30:
                #     BRAIN.drink_coffe()
                #     Voice.say("aah coffee. What a treat")
                #     Neck.act_no()

            case BRAIN.SM.searching:

                search()

            case BRAIN.SM.excited:
                sleep(2)
                if randint(0, 100) < 15:

                    # Voice.say("meh")
                    BRAIN.get_bored()

            case BRAIN.SM.disapointed:
                sleep(5)
                # Neck.act_no()
                BRAIN.try_again()


if __name__ == "__main__":  # for debugging
    brain_thread()

    while True:
        sleep(3)
        fns = [
            BRAIN.drink_coffe,
            BRAIN.get_excited,
            BRAIN.get_disapointed,
            BRAIN.try_again,
            BRAIN.get_bored,
        ]
        i = randint(0,len(fns))
        fns[i]()


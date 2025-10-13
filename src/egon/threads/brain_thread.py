"""This thread manages the actual decision making of Egon.
It links the outputs of the sensors in the Short Term Memory to the emotional state and actions.
"""

from egon.modules.memory import ShortTermMem, LongTermMem
from egon.modules.emotional_state import EmotionalState as BRAIN
from egon.modules.voice import Voice, get_excited_ono, get_bored_ono
from egon.modules.motor_control import Neck
from egon.modules.logger import logger
from time import sleep
from random import randint, sample, choice

from egon.modules.console_utils import ConsoleTable

CT = ConsoleTable("🧠brain🧠", index=9)


def do_I_like_something(stuff_seen):
    long_mem = LongTermMem.get_long_term_mem()
    new_thing = None
    for key in stuff_seen:
        if key not in long_mem:
            new_thing = key
            break
    if new_thing is None:
        # bad ending
        logger.info("🧠 old stuff disapointed")
        BRAIN.get_disapointed()
        BRAIN.next_now.set()
        # ono = get_bored_ono()
        # Voice.say(ono)
        Voice.say_bored_sound()

    else:
        # new this is good
        logger.info(f"🧠 {new_thing} is exciting")
        LongTermMem.add(new_thing)
        ShortTermMem.remove(new_thing)
        BRAIN.get_excited()
        BRAIN.next_now.set()
        ono = get_excited_ono()
        # Voice.say(ono)
        # Voice.say(ono)
        Voice.say_happy_sound()


def search():
    mem = ShortTermMem.get_short_term_mem()

    # someone is there
    if (
        "person" in mem.keys() and mem["person"] > 10
    ):  # only think when people are present
        stuff_seen = set(mem.keys())
        stuff_seen.remove("person")
        for key in list(mem.keys()):
            if mem[key] < 6:
                stuff_seen.remove(key)  # remove object below a certainty treshold
        CT.d["seen"] = f"{stuff_seen}"

        if len(stuff_seen) == 0:
            return  # found nothing. continue search.

        do_I_like_something(stuff_seen)


def brain_thread():

    Voice.init_voice()

    disapointment_buffer = False
    CT.d["disa buff"] = f"{disapointment_buffer}"

    while True:
        sleep(0.1)

        match BRAIN.SM.current_state:
            case BRAIN.SM.waking:
                sleep(1)
                Voice.say("BOOOONJOUUUUUUUR!!!!! ")
                # Neck.act_no()
                BRAIN.drink_coffe()


            case BRAIN.SM.searching:
                if disapointment_buffer:
                    disapointment_buffer = False
                    sleep(randint(15,20))

                search()

            case BRAIN.SM.excited:
                BRAIN.has_finished_acting.wait(timeout=6)
                disapointment_buffer = True
                if randint(0, 100) < 15:

                    BRAIN.get_bored()

            case BRAIN.SM.disapointed:
                BRAIN.has_finished_acting.wait(timeout=6)
                disapointment_buffer = True
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
        i = randint(0, len(fns))
        fns[i]()

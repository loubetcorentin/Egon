from egon.modules.emotional_state import EmotionalState as BRAIN
from egon.modules.motor_control import Neck
from egon.modules.console_utils import ConsoleTable
from egon.modules.logger import logger
from threading import Event, Timer

next_now = Event()

steps_search = [
    ["absolute", 0, 0.2, 8],
    ["absolute", 180, 0.2, 8],
    "repeat",
]

steps_wake = [
    ["absolute", 0, 0.1, 10],
    ["absolute", 20, 0.1, 10],
    "repeat",
]

steps_no = [
    ["make_place", 20, 0.4, 0.1],
    ["relative", -20, 0.4, 0.5],
    ["relative", +20, 0.4, 0.5],
    ["relative", -20, 0.4, 0.5],
    ["relative", +20, 0.4, 0.5],
    ["relative", -20, 0.4, 0.5],
    ["relative", +20, 0.4, 0.5],
]

steps_yes = [
    ["make_place", 20, 1, 0.1],
    ["relative", -40, 1, 0.1],
    ["relative", +40, 1, 0.1],
    ["make_place", 20, 1, 0.1],
    ["relative", -40, 1, 0.1],
    ["relative", +40, 1, 0.1],
    ["make_place", 20, 1, 0.1],
    ["relative", -40, 1, 0.1],
    ["relative", +40, 1, 0.1],
    ["make_place", 20, 1, 0.1],
    ["relative", -40, 1, 0.1],
    ["relative", +40, 1, 0.1],
]

act_from_state = {
    BRAIN.SM.waking: steps_wake,
    BRAIN.SM.searching: steps_search,
    BRAIN.SM.excited: steps_yes,
    BRAIN.SM.disapointed: steps_no,
}


fn_dict = {
    "make_place": Neck.make_space,
    "absolute": Neck.move_to,
    "relative": Neck.move_by,
    "freeze": Neck.freeze,
}


def play_movement(args):
    fn_name, angle, speed_ratio, sleep_time = args
    fn = fn_dict[fn_name]
    fn(angle, speed_ratio)
    next_now.clear()
    t = Timer(sleep_time, next_now.set)
    t.start()
    next_now.wait()
    t.cancel()
    # sleep(sleep_time)


def neck_thread():

    Neck.init_neck()

    current_act = [["make_place", 20, 0.2, 1]]
    CT = ConsoleTable("neck thread", index=8)

    def queue_act(state, current_act: list):
        logger.info(f'motor queue {str(state)}')
        CT.d["state"] = f"{str(state):^15}"

        current_act.clear()
        for step in act_from_state[state]:
            current_act.append(step)

        next_now.set()

    CT.d["state"] = "nothing"
    current_state = None

    while True:

        CT.d["nextnow"] = f"{next_now.is_set()}"
        CT.d["brain update"] = f"{BRAIN.is_updated.is_set()}"
        CT.d["current act len"] = f"{len(current_act)}"
        if BRAIN.is_updated.is_set():  # brain thread ahs changed emotional state
            current_state = BRAIN.SM.current_state
            BRAIN.is_updated.clear()
            queue_act(current_state, current_act)

        if len(current_act) == 0:  # the current act is finished
            BRAIN.has_finished_acting.set()
            BRAIN.is_updated.wait()

        else:

            move = current_act.pop(0)
            if move == "repeat":
                queue_act(current_state, current_act)
            else:
                CT.d["move"] = f"{move}"
                CT.d["nextnow"] = f"{next_now.is_set()}"
                play_movement(move)

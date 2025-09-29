from egon.modules.emotional_state import EmotionalState as BRAIN
from egon.modules.motor_control import Neck
from time import sleep
from egon.modules.console_utils import ConsoleTable

from threading import Event, Timer

next_now = Event()

steps_search = [
    ["absolute",0,0.6,5],
    ["absolute",180,0.6,5],
    
]

steps_wake = [
    ["absolute",0,0.1,10],
    ["absolute",20,0.1,10],
]

steps_no = [
    ["make_place",20,0.4,0.1],
    ["relative",-20,0.4,0.5],
    ["relative",+20,0.4,0.5],
    ["relative",-20,0.4,0.5],
    ["relative",+20,0.4,0.5],
    ["relative",-20,0.4,0.5],
    ["relative",+20,0.4,0.5],
]

steps_yes = [
    ["make_place",20,1,0.1],
    ["relative",-40,1,0.1],
    ["relative",+40,1,0.1],
    ["make_place",20,1,0.1],
    ["relative",-40,1,0.1],
    ["relative",+40,1,0.1],
    ["make_place",20,1,0.1],
    ["relative",-40,1,0.1],
    ["relative",+40,1,0.1],
    ["make_place",20,1,0.1],
    ["relative",-40,1,0.1],
    ["relative",+40,1,0.1],
    
]

act_from_state = {
    BRAIN.SM.waking : steps_wake,
    BRAIN.SM.searching : steps_search,
    BRAIN.SM.excited : steps_yes,
    BRAIN.SM.disapointed : steps_no,
    
}


fn_dict = {
    "make_place": Neck.make_space,
    "absolute" : Neck.move_to,
    "relative" : Neck.move_by,  
    "freeze": Neck.freeze
}

def play_movement(args):
    fn_name, angle, speed_ratio, sleep_time = args
    fn = fn_dict[fn_name]
    fn(angle,speed_ratio)
    t=Timer(sleep_time,next_now.set)
    t.start()
    next_now.wait()
    t.cancel()
    sleep(sleep_time)
    

def neck_thread():
    CT = ConsoleTable("neck thread",index=8)

    Neck.init_neck()

    current_act = [["make_place",20,0.2,1]]

    while True:

        CT.d["nextnow"] = f"{next_now.is_set()}"
        CT.d["brain update"] = f"{BRAIN.is_updated.is_set()}"
        if BRAIN.is_updated.is_set():
            state = BRAIN.SM.current_state
            CT.d["state"] = f"{str(state):^15}"
            current_act = act_from_state[state].copy()
            BRAIN.is_updated.clear()
            next_now.set()

        if len(current_act)==0:
            CT.d["state"] = f"default search"
            current_act = steps_search.copy()

        move = current_act.pop(0)
        CT.d["move"] = f"{move}"
        play_movement(move)
        
        




from egon.modules.emotional_state import EmotionalState as BRAIN
from egon.modules.motor_control import Neck
from egon.modules.console_utils import ConsoleTable
from egon.modules.logger import logger
from threading import Event, Timer
from time import sleep
from egon.modules.memory import CrowdPosition

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
    BRAIN.next_now.clear()
    t = Timer(sleep_time, BRAIN.next_now.set)
    t.start()
    BRAIN.next_now.wait()
    t.cancel()
    # sleep(sleep_time)


def neck_thread():
    CT = ConsoleTable("neck thread", index=8)

    Neck.init_neck()




    current_state = BRAIN.SM.current_state

    act = "look_at_people"
    iteration = 0

    

    def look_at_public():
        if CrowdPosition.has_public():
            angle = CrowdPosition.get_delta_rot()
            speed = min((abs(angle) /60)**3,1) 
            
            # CT.d["people deg"] = f"{angle: 3.2f}"
            # CT.d["people speed"] = f"{speed:.2f}"
            # CT.d["look public"] = "[#55FF88]True[/#55FF88]"

            Neck.move_by(angle,speed)


    to_the_left = True
    while True:

        
        iteration +=1
        current_state = BRAIN.SM.current_state

        if to_the_left and Neck.BS.current_value >175:
            to_the_left = False
        elif not to_the_left and Neck.BS.current_value < 5:
            to_the_left = True
        
        if current_state == BRAIN.SM.searching: 
            if CrowdPosition.has_public() :
                act = "look_at_people"
            elif to_the_left:
                act = "search_left"
            else: 
                act = "search_right"     

  

        elif current_state == BRAIN.SM.excited:
            act = "crazzyyy"
        elif current_state == BRAIN.SM.disapointed:
            act = "meh"
        else:
            act = "nothing"

            

        CT.d = {
                "brain state" : str(current_state),
                "case" : act,
                "iter" : str(iteration),
                "to "
                "nxtnow": "[#55FF88]True[/#55FF88]" if BRAIN.next_now.is_set() else "[#DD3311]False[/#DD3311]"
            }

        t = Timer(0.4, BRAIN.next_now.set)
        match act:
            case "search_left":
                Neck.move_to(180,0.4)
                t = Timer(0.1, BRAIN.next_now.set)
                t.start()
 
                
            case "search_right":
                Neck.move_to(0,0.4)
                t = Timer(0.1, BRAIN.next_now.set)
                t.start()


            case "look_at_people":
                look_at_public()
                t = Timer(0.1, BRAIN.next_now.set)
                t.start()

            case "crazzyyy":
                Neck.move_to(0,1)
                sleep(0.2)
                Neck.move_to(180,1)
                sleep(0.2)
                Neck.move_to(0,1)
                sleep(0.2)
                Neck.move_to(180,1)
                sleep(0.2)
                Neck.move_to(0,1)
                sleep(0.2)
                Neck.move_to(180,1)
                sleep(0.2)
                BRAIN.next_now.set()
                BRAIN.has_finished_acting.set()
            case "meh":
                if Neck.BS.current_value <90:
                    Neck.move_by(80,1)
                else:
                    Neck.move_by(-80,1)

                sleep(4)

                BRAIN.next_now.set()
                BRAIN.has_finished_acting.set()
                
        BRAIN.next_now.wait(timeout=15)
        BRAIN.next_now.clear()
        t.cancel()
    

        
        


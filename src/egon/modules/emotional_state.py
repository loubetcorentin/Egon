from statemachine import StateMachine, State
from egon.modules.console_utils import ConsoleTable
from threading import Event


event_new_state = Event()
event_finished_acting = Event()
next_now = Event()

def callback_change():
    event_new_state.set()
        


class EmotionalJourneySM(StateMachine):

    # states
    waking = State("waking", initial=True)
    searching = State("searching")
    excited = State("excited")
    disapointed = State("disapointed")

    # transitions
    drink_coffe = waking.to(searching, on = callback_change)
    get_excited = searching.to(excited, on = callback_change)
    get_disapointed = searching.to(disapointed, on = callback_change)
    try_again = disapointed.to(searching, on = callback_change)
    get_bored = excited.to(searching, on = callback_change)


class EmotionalState:
    is_updated = event_new_state
    has_finished_acting = event_finished_acting
    next_now = next_now
    SM = EmotionalJourneySM()



    drink_coffe = SM.drink_coffe
    get_excited = SM.get_excited
    get_disapointed = SM.get_disapointed
    try_again = SM.try_again
    get_bored = SM.get_bored







    

def update_brain_ct():
    return {
        "Emotional State": f"{str(EmotionalState.SM.current_state):^15}",
    }

CT = ConsoleTable("emotion", update_brain_ct, index=1)



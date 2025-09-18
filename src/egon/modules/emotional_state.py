from statemachine import StateMachine, State
from egon.modules.console_utils import ConsoleTable


class EmotionalJourneySM(StateMachine):

    # states
    waking = State("waking", initial=True)
    searching = State("searching")
    excited = State("excited")
    disapointed = State("disapointed")

    # transitions
    drink_coffe = waking.to(searching)
    get_excited = searching.to(excited)
    get_disapointed = searching.to(disapointed)
    try_again = disapointed.to(searching)
    get_bored = excited.to(searching)


class EmotionalState:
    SM = EmotionalJourneySM()


def update_brain_ct():
    return {
        "Emotional State": f"{str(EmotionalState.SM.current_state):^15}",
    }

CT = ConsoleTable("🧠🧠🧠🧠 brain", update_brain_ct, index=1)

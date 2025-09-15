from statemachine import StateMachine, State


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
    try_again  = disapointed.to(searching)
    get_bored = excited.to(searching)


class EmotionalState:
    SM = EmotionalJourneySM()

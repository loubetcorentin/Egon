from statemachine import StateMachine, State


class EmotionalJourneySM(StateMachine):

    #states
    waking = State("waking", initial=True)
    searching = State(
        "searching",
    )
    excited = State(
        "excited",
    )

    #transitions
    drink_coffe = waking.to(searching)
    see_someone = searching.to(excited)
    get_bored = excited.to(searching)


class EmotionalState:
    SM = EmotionalJourneySM()
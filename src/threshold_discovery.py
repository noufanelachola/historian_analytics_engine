import pandas as pd

def generate_threshold_report(
    actuator,
    process_variable,
    rise_stats,
    fall_stats
):

    report = pd.DataFrame([
        {
            "Actuator": actuator,
            "Process Variable": process_variable,

            "Rise Median": rise_stats["median"],
            "Rise Q25": rise_stats["q25"],
            "Rise Q75": rise_stats["q75"],

            "Fall Median": fall_stats["median"],
            "Fall Q25": fall_stats["q25"],
            "Fall Q75": fall_stats["q75"]
        }
    ])

    return report


def find_state_transitions(df, asset):

    states = df[asset]

    previous_states = states.shift(1)

    transitions = states != previous_states

    transition_data = df.loc[
        transitions,
        [asset]
    ].copy()

    transition_data["previous_state"] = previous_states[transitions]
    transition_data["new_state"] = states[transitions]

    return transition_data

def find_transition_conditions(df, actuator, process_variable):
    states = df[actuator]

    previous_states = states.shift(1)

    transitions = states != previous_states

    transition_data = df.loc[
        transitions,
        [actuator, process_variable]
    ].copy()

    transition_data["previous_state"] = previous_states[transitions]

    transition_data["new_state"] = states[transitions]

    return transition_data

def get_transition_values(df, actuator, process_variable):
    transitions = find_transition_conditions(
        df,
        actuator,
        process_variable
    )

    transitions = transitions.dropna()

    return transitions

def split_transitions(transitions):

    rise = transitions[
        (transitions["previous_state"] == 1) &
        (transitions["new_state"] == 2)
    ]

    fall = transitions[
        (transitions["previous_state"] == 2) &
        (transitions["new_state"] == 1)
    ]

    return rise, fall

def estimate_threshold(values):

    return {
        "median": values.median(),
        "min": values.min(),
        "max": values.max(),
        "q25": values.quantile(0.25),
        "q75": values.quantile(0.75)
    }
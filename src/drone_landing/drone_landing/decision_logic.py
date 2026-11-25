def landing_decision(marker_detected, marker_displacement,
                     altitude, descent_velocity,
                     state, recovery_complete, landed):

    displacement_limit = 0.20
    reaction_time = 0.20
    braking_acceleration = 2.0
    safety_margin = 0.10

    reaction_distance = descent_velocity * reaction_time

    braking_distance = (
        descent_velocity ** 2
        / (2 * braking_acceleration)
    )

    required_altitude = (
        reaction_distance
        + braking_distance
        + safety_margin
    )

    target_safe = (
        marker_detected
        and marker_displacement <= displacement_limit
    )

    if state == "LANDED":
        return "LANDED"

    elif state == "FAILSAFE":
        return "FAILSAFE"

    elif state == "LANDING":

        if landed:
            return "LANDED"

        elif target_safe:
            return "CONTINUE"

        elif altitude >= required_altitude:
            return "ABORT"

        else:
            return "FAILSAFE"

    elif state == "RECOVERING":

        if recovery_complete and target_safe:
            return "RETRY"

        else:
            return "HOLD"

    else:
        return "FAILSAFE"


def update_state(state, decision):

    if decision == "ABORT":
        return "RECOVERING"

    elif decision == "RETRY":
        return "LANDING"

    elif decision == "FAILSAFE":
        return "FAILSAFE"

    elif decision == "LANDED":
        return "LANDED"

    else:
        return state


def run_simulation(title, events):

    state = "LANDING"

    print("=" * 40)
    print(title)
    print("=" * 40)

    for event in events:

        name, detected, displacement, altitude, velocity, recovered, landed = event

        decision = landing_decision(
            detected,
            displacement,
            altitude,
            velocity,
            state,
            recovered,
            landed
        )

        print(f"Event: {name}")
        print(f"Previous state: {state}")
        print(f"Decision: {decision}")

        state = update_state(state, decision)

        print(f"New state: {state}")
        print("-" * 40)

        if state in ("LANDED", "FAILSAFE"):
            break

    print(f"Final state: {state}")
    print()

    return state


if __name__ == "__main__":

    successful_recovery = [
        ("Initial descent", True, 0.10, 3.0, 1.0, False, False),
        ("Platform moves", True, 0.40, 2.0, 1.0, False, False),
        ("Recovery begins", True, 0.40, 1.8, 0.0, False, False),
        ("Recovery complete", True, 0.40, 3.0, 0.0, True, False),
        ("Target realigned", True, 0.05, 3.0, 0.0, True, False),
        ("Descent resumes", True, 0.05, 2.5, 1.0, False, False),
        ("Touchdown", True, 0.02, 0.0, 0.0, False, True)
    ]

    late_disturbance = [
        ("Initial descent", True, 0.10, 3.0, 1.0, False, False),
        ("Approaching surface", True, 0.05, 0.40, 1.0, False, False),
        ("Platform moves too late", True, 0.40, 0.40, 1.0, False, False),
        ("Target realigned", True, 0.05, 0.30, 0.0, True, False)
    ]

    run_simulation(
        "TEST 1: Successful recovery",
        successful_recovery
    )

    run_simulation(
        "TEST 2: Late disturbance",
        late_disturbance
    )

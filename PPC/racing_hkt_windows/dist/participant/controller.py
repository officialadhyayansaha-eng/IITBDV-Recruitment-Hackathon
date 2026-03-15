
'''
PPC Hackathon — Participant Boilerplate
You must implement two functions: plan() and control()
'''

# ─── TYPES (for reference) ────────────────────────────────────────────────────

# Path: list of waypoints [{"x": float, "y": float}, ...]
# State: {"x", "y", "yaw", "vx", "vy", "yaw_rate"}
# CmdFeedback: {"throttle", "steer"}

# ─── CONTROLLER ───────────────────────────────────────────────────────────────
import numpy as np

target_index = 0

def steering(path: list[dict], state: dict):

    length_of_car = 2.6
    const=0.5
    gain=0.7
    # Calculate steering angle based on path and vehicle state
    global target_index
    d=length_of_car+const*state["vx"]
    while target_index < len(path)-1:
        dx=path[target_index]["x"]-state["x"]
        dy=path[target_index]["y"]-state["y"]
        distance=np.sqrt(dx*dx+dy*dy)
        if distance<d:
            target_index=target_index+1
        else:
            break
    target=path[target_index]
    delta_x=target["x"]-state["x"]
    delta_y=target["y"]-state["y"]
    approach_angle=np.arctan2(delta_y,delta_x)
    normalized_angle=np.arctan2(np.sin(approach_angle-state["yaw"]),np.cos(approach_angle-state["yaw"]))

    steer = 0.0 # Default steer value
    # 0.5 in the max steering angle in radians (about 28.6 degrees)
    steer=gain*normalized_angle
    return np.clip(steer, -0.5, 0.5)


def throttle_algorithm(target_speed, current_speed, dt):
    c4=0.5
    c5=-0.6
    throttle=0.0
    brake=0.0
    if current_speed < target_speed:
        throttle=c4*(target_speed-current_speed)
    else:
        brake=c5*(target_speed-current_speed)
    return np.clip(throttle, 0.0, 1.0), np.clip(brake, 0.0, 1.0)

def control(
    path: list[dict],
    state: dict,
    cmd_feedback: dict,
    step: int,
) -> tuple[float, float, float]:
    """
    Generate throttle, steer, brake for the current timestep.
    Called every 50ms during simulation.

    Args:
        path:         Your planned path (waypoints)
        state:        Noisy vehicle state observation
                        x, y        : position (m)
                        yaw         : heading (rad)
                        vx, vy      : velocity in body frame (m/s)
                        yaw_rate    : (rad/s)
        cmd_feedback: Last applied command with noise
                        throttle, steer, brake
        step:         Current simulation timestep index

    Returns:
        throttle  : float in [0.0, 1.0]   — 0=none, 1=full
        steer     : float in [-0.5, 0.5]  — rad, neg=left
        brake     : float in [0.0, 1.0]   — 0=none, 1=full

    Note: throttle and brake cannot both be > 0 simultaneously.
    """
    throttle = 0.0
    steer    = 0.0
    brake = 0.0

    # TODO: implement your controller here
    steer = steering(path, state)
    target_speed = 6*(1-0.75*abs(steer))# m/s, adjust as needed
    global integral
    throttle, brake = throttle_algorithm(target_speed, state["vx"], 0.05)

    return throttle, steer, brake

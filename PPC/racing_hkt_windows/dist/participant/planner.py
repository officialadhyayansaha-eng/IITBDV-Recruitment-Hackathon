
'''
PPC Hackathon — Participant Boilerplate
You must implement two functions: plan() and control()
'''

# ─── TYPES (for reference) ────────────────────────────────────────────────────

# Cone: {"x": float, "y": float, "side": "left" | "right", "index": int}
# State: {"x", "y", "yaw", "vx", "vy", "yaw_rate"}  
# CmdFeedback: {"throttle", "steer"}        

# ─── PLANNER ──────────────────────────────────────────────────────────────────
import numpy as np

def plan(cones: list[dict]) -> list[dict]:
    """
    Generate a path from the cone layout.
    Called ONCE before the simulation starts.

    Args:
        cones: List of cone dicts with keys x, y, side ("left"/"right"), index

    Returns:
        path: List of waypoints [{"x": float, "y": float}, ...]
              Ordered from start to finish.
    
    Tip: Try midline interpolation between matched left/right cones.
         You can also compute a curvature-optimised racing line.
    """
    path = []
    # TODO: implement your path planning here
    blue = np.array([[cone["x"], cone["y"]] for cone in cones if cone["side"] == "left"])
    yellow = np.array([[cone["x"], cone["y"]] for cone in cones if cone["side"] == "right"])

    # implement a planning algorithm to generate a path from the blue and yellow cones
#   i=0
#    x1,y1,x2,y2=0,0,0,0
#    while i<len(blue):
#        for cone in cones:
#            if cone["index"]==i and cone["side"]=="left":
#                x1=cone['x']
#                y1=cone['y']
#            if cone["index"]==i and cone["side"]=="right":
#                x2=cone['x']
#                y2=cone['y']
#        path.append({"x":(x1+x2)/2 , "y"=(y1+y2)/2})
#        i+=1

    cones_left=[{"x":cone["x"], "y":cone["y"], "side":cone["side"] , "index":cone["index"]} for cone in cones if cone["side"]=="left"]
    cones_right=[{"x":cone["x"], "y":cone["y"], "side":cone["side"] , "index":cone["index"]} for cone in cones if cone["side"]=="right"]
    cones_left.sort(key=lambda cone: cone["index"])
    cones_right.sort(key=lambda cone: cone["index"])
    for i in range(min(len(cones_left),len(cones_right))):
        path.append({"x":(cones_left[i]["x"]+cones_right[i]["x"])/2,"y":(cones_left[i]["y"]+cones_right[i]["y"])/2})
    
    
    return path

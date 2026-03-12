from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os

def generate_launch_description():

    urdf = os.path.join(
        os.getenv("HOME"),
        "workspace/src/robot_sim/urdf/robot.urdf"
    )

    return LaunchDescription([

        ExecuteProcess(
            cmd=["ign", "gazebo", "empty.sdf"],
            output="screen"
        ),

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{'robot_description': open(urdf).read()}]
        ),

        Node(
            package="ros_gz_sim",
            executable="create",
            arguments=[
                "-file", urdf,
                "-name", "diffbot",
                "-z", "1"
            ],
            output="screen"
        )
    ])

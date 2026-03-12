import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    # sudo apt install ros-humble-ros-gz
    bringup_share = get_package_share_directory('mf_gazebo_bringup')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    world_path = os.path.join(bringup_share, 'worlds', 'office_step1.world.sdf')
    model_path = os.path.join(bringup_share, 'models', 'mobile_bot', 'model.sdf')
    model_dir = os.path.join(bringup_share, 'models')

    # 调用 ros_gz_sim 包里的 gz_sim.launch.py 来启动 Gazebo Sim。
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': world_path,
            'on_exit_shutdown': 'true',
        }.items(),
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-world', 'office_step1',
            '-name', 'mobile_bot',
            '-file', model_path,
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.12',
        ],
    )

    return LaunchDescription([
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', model_dir),
        gz_sim,
        spawn_robot,
    ])
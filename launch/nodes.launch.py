import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace


def generate_launch_description():
    #ros2_x_omni args
    omni_serial_path_launch_arg = DeclareLaunchArgument(
        'x_omni_port', default_value=TextSubstitution(text='/dev/ttyXOmni')
    )

    #udp_joycon args
    port_launch_arg = DeclareLaunchArgument(
        'port', default_value=TextSubstitution(text='37501')
    )
    linear_launch_arg = DeclareLaunchArgument(
        'linear_max', default_value=TextSubstitution(text='0.2') #[m/s]
    )
    angular_launch_arg = DeclareLaunchArgument(
        'angular_max', default_value=TextSubstitution(text='0.7') #[rad/s]
    )

    #rplidar_ros args
    lidar_serial_path_launch_arg = DeclareLaunchArgument(
        'lidar_port', default_value=TextSubstitution(text='/dev/ttyRPLidar')
    )


    ros2_x_omni_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
             os.path.join(get_package_share_directory('ros2_x_omni'),'x_omni.launch.py')
        ),
        launch_arguments = (
            {'serial_port': LaunchConfiguration('x_omni_port')}
        ).items()
    )

    udp_joycon_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
             os.path.join(get_package_share_directory('udp_joycon'),'udp_joycon.launch.py')
        ),
        launch_arguments = (
            {'port': LaunchConfiguration('port'),
            'linear_max': LaunchConfiguration('linear_max'),
            'angular_max': LaunchConfiguration('angular_max')}
        ).items()
    )

    #rplidar_ros node (A1 model)
    rplidar_ros_node = Node(
        package='rplidar_ros',
        executable='rplidar_node',
        parameters=[
            {'serial_baudrate_':    115200},
            {'serial_port':         LaunchConfiguration('lidar_port')},
        ]
    )

    return LaunchDescription([
        omni_serial_path_launch_arg,
        port_launch_arg,
        linear_launch_arg,
        angular_launch_arg,
        lidar_serial_path_launch_arg,
        ros2_x_omni_launch,
        udp_joycon_launch,
        rplidar_ros_node,
    ])
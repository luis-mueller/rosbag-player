from setuptools import setup

setup(
    name='rosbag-player',
    version="1.0.0",
    py_modules=['rosbag_player'],
    entry_points = {
        'console_scripts': [
            'rosbag-player = rosbag_player:start',
            'rosbag-convert = rosbag_player:convert'
        ]},
    install_requires=[
        "py3rosmsgs>=1.18.2",
        "pycryptodomex>=3.14.1",
        "rospkg>=1.4.0"
    ]
)

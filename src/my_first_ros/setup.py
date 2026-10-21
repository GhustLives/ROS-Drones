
from setuptools import find_packages, setup

package_name = 'my_first_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='matthew',
    maintainer_email='matthew@todo.todo',
    description='My first ROS 2 Python package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hello_node = my_first_ros.hello_node:main',
            'altitude_publisher = my_first_ros.altitude_publisher:main',
            'altitude_subscriber = my_first_ros.altitude_subscriber:main',
        ],
    },
)

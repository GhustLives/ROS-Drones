from setuptools import find_packages, setup

package_name = "drone_landing"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name]
        ),
        (
            "share/" + package_name,
            ["package.xml"]
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Drone Landing Team",
    maintainer_email="vboxuser@todo.todo",
    description="Autonomous drone landing decision system",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "landing_node = drone_landing.landing_node:main",
        ],
    },
)

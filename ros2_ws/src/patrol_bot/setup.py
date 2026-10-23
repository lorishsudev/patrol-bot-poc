from setuptools import find_packages, setup

package_name = 'patrol_bot'

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
    maintainer='loris',
    maintainer_email='lorishsu.dev@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'hello = patrol_bot.hello:main',
            'heartbeat = patrol_bot.heartbeat:main',
            'battery = patrol_bot.battery:main',
            'status_monitor = patrol_bot.status_monitor:main',
        ],
    },
)

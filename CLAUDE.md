# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Proof-of-concept patrol robot built on **ROS 2 Jazzy** (installed at `/opt/ros/jazzy`). The ROS 2 colcon workspace lives in `ros2_ws/`; packages go under `ros2_ws/src/`. Currently there is a single `ament_python` package, `patrol_bot`, containing only a placeholder `hello` entry point.

## Environment

- Ubuntu 24.04 ARM64, ROS 2 Jazzy, Python nodes using `rclpy`, simulation in Gazebo Harmonic.
- Package: `ros2_ws/src/patrol_bot` (`ament_python`).
- Target robot is TurtleBot3: its `/cmd_vel` uses `geometry_msgs/msg/TwistStamped` (not `Twist`), so publishers must send stamped messages.
- Code also runs on a Raspberry Pi 5 (keep it ARM64-compatible and lightweight). Use `ROS_DOMAIN_ID=30` (`export ROS_DOMAIN_ID=30`) on both the dev machine and the Pi so they can discover each other.

## Commands

Run all of these from `ros2_ws/`, after sourcing ROS: `source /opt/ros/jazzy/setup.bash`.

```bash
colcon build --symlink-install            # build (outputs to build/ install/ log/, all gitignored)
source install/setup.bash                 # overlay the workspace before running nodes
ros2 run patrol_bot hello                 # run an entry point

colcon test --packages-select patrol_bot && colcon test-result --verbose   # run tests
(cd src/patrol_bot && python3 -m pytest test/test_flake8.py)               # single test; run from the package dir since the linters scan cwd
```

Linting is done through the ament tests (`test_flake8.py`, `test_pep257.py`), so code must pass flake8 and pep257 docstring checks for tests to pass. `test_copyright.py` is skipped until source files get copyright headers.

## Package conventions (ament_python)

- New executables must be registered in `setup.py` under `entry_points['console_scripts']` as `name = patrol_bot.module:main`; `setup.cfg` installs them to `lib/patrol_bot` so `ros2 run` can find them.
- Non-Python files (launch files, config, etc.) must be added to `data_files` in `setup.py` to be installed into `share/patrol_bot`.
- Runtime ROS dependencies (e.g. `rclpy`, message packages) must be declared in `package.xml` as `<depend>`/`<exec_depend>`; currently only test dependencies are declared.
- Rebuild after changing `setup.py`, `package.xml`, or adding files (symlink installs pick up edits to existing Python modules without rebuilding).

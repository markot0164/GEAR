# 🤖 Robot Programming Project – ROS Noetic (Dockerized)

This repository contains a **Robot Programming project** developed using **ROS Noetic**.  
The project is fully **containerized using Docker**, allowing it to run on any operating system without requiring a local ROS installation.

Originally developed on **Ubuntu 20.04 LTS** for a **Robot Programming university exam**, the project can now be executed on **Linux, macOS, and Windows**.

---

## 📖 Project Overview

The project simulates a sphere navigating an environment while avoiding being detected by rotating camera fields of view.

### 🛠️ Core mechanics:
- A sphere moves inside a 2D environment
- Two rotating camera cones detect collisions
- If the sphere enters a camera field of view, it is reset to the initial position
- If the sphere reaches the goal area, the simulation shuts down

All components communicate using **ROS topics and services**.

---
## ⚙️ Prerequisites
- Docker

## Platform-specific notes:

### macOS
    XQuartz (required only if RViz visualization is used)

### Windows
    Docker Desktop with WSL2 backend
    RViz supported via WSLg (optional)

### Linux
    X11 display server (RViz works out of the box)

## ⚠️ RViz is optional.
The project logic can be fully tested without any graphical interface.

---

## Project Structure

```text
rp_project/
├── Dockerfile
├── CMakeLists.txt
├── package.xml
├── scripts/
│   ├── sphere_control_node.py
│   ├── camera_detection.py
│   ├── keyboard_controller.py
│   ├── reset_position.py
│   ├── check_goal.py
│   └── rviz_map.py
├── msg/
│   └── Collision.msg
├── srv/
│   ├── ResetPosition.srv
│   └── CheckGoal.srv
```
---

## 🐳 Build the Docker Image
From the **root** of the project:
```bash
docker build -t rp_project .
```
## 🐳 Run Docker Image and start roscore
```bash
docker run --rm -it --name rp_container rp_project
```
inside the terminal container:

```bash
roscore
```
This command starts the ROS master required by all other nodes.  
Do not close this terminal.

## ⛓️ Run the nodes
Open additional terminals and attach to the container:
```bash
docker exec -it rp_container bash
```
Then run the following nodes:
### Sphere control node
```bash
rosrun rp_project sphere_control_node.py
```
### Camera collision detection
```bash
rosrun rp_project camera_detection.py
```
### Reset position service
```bash
rosrun rp_project reset_position.py
```
### Goal check service
```bash
rosrun rp_project check_goal.py
```
### Keyboard controller
```bash
rosrun rp_project keyboard_controller.py
```
To move the sphere use the keys **W, A, S, D**.  
Press **Q** to stop the controller.

### ⚠️ If the sphere is not moving
Make sure you are typing the commands in the **Keyboard Controller terminal**.

---
## 🖥️ Run the Project with RViz (Optional)
RViz provides a graphical visualization of:

- The sphere
- The goal
- Cameras and rotating fields of view
- Obstacles

## Start RViz map node
Inside a new terminal container:
```bash
rosrun rp_project rviz_map.py
```
Inside RViz, set the **Fixed Frame** to `world`.

You are now ready to interact with the simulation.

---

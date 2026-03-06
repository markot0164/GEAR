FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=noetic

# Base tools
RUN apt update && apt install -y \
    curl \
    gnupg2 \
    lsb-release \
    build-essential \
    python3-pip \
    git

# Add ROS repository key
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    | gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add ROS repository
RUN echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" \
    > /etc/apt/sources.list.d/ros1.list

RUN apt update && apt install -y \
    ros-noetic-desktop-full \
    python3-rosdep \
    python3-catkin-tools

# ROS setup
RUN rosdep init && rosdep update
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc

# Create catkin workspace
WORKDIR /root/catkin_ws
RUN mkdir src

# Copy ROS package into workspace
COPY . /root/catkin_ws/src/rp_project

# Build workspace
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make"

# Source workspace on container start
RUN echo "source /root/catkin_ws/devel/setup.bash" >> /root/.bashrc

CMD ["bash"]

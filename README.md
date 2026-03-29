# 🚗 Jarvis – Bosch Future Mobility Challenge (BFMC) 2026

Team Jarvis | Autonomous Driving System using ROS2, AI, and Embedded Systems

---

## 📌 Overview

This project presents a distributed autonomous driving system developed for the Bosch Future Mobility Challenge (BFMC) 2026.
The system focuses on real-time perception, decision-making, and control using ROS2, computer vision, and embedded systems.

The architecture distributes tasks across multiple hardware units (Laptop, Raspberry Pi, Arduino) to achieve efficient real-time performance.

---

## 🧠 Key Features

* Real-time lane detection and steering control
* AI-based object detection (YOLOv5)
* Priority-based autonomous decision system
* Distributed computing architecture
* IMU-based stabilization
* Hybrid AI + classical vision approach

---

## 🔍 Features & Implementation

### 🔹 Vision-Based Lane Detection

* Implemented using OpenCV
* Techniques used:

  * Color masking
  * Canny edge detection
  * Hough Transform
* Region of Interest (ROI) masking to focus on the road
* Curve targeting and smoothing for stable steering
* Steering output: **1300 / 1500 / 1700 PWM**

---

### 🔹 AI-Based Object Detection

* Built using YOLOv5
* Detects:

  * Stop signs
  * Pedestrians
  * Traffic lights
  * Obstacles
* Traffic light classification using HSV filtering
* Optimized for real-time performance

---

### 🔹 Central Decision System

Priority-based decision logic:

**Pedestrian > Stop Sign > Traffic Light > Lane Following**

* Immediate stop for pedestrians
* 3-second delay for stop signs
* Traffic light handling (STOP / WAIT / GO)
* Default behavior: lane following

Implemented as a ROS2 central node

---

### 🔹 Distributed System

* **Laptop** → AI + Lane detection + Decision making
* **Raspberry Pi** → Camera streaming + communication
* **Arduino Nano** → Motor control

Communication:

* ROS2 topics
* Socket communication

---

### 🔹 Real-Time Video Streaming

* Raspberry Pi streams video using MJPEG
* Frames decoded on laptop
* Published to ROS2 topics
* Enables parallel processing

---

### 🔹 IMU-Based Stabilization

* MPU6050 IMU integrated
* Local P-controller on Raspberry Pi
* Improves steering stability and motion correction

---

### 🔹 Control System

* Commands generated on laptop
* Raspberry Pi applies IMU correction
* Arduino executes PWM motor control

---

## ⚙️ Tech Stack

* ROS2 (rclpy)
* Python
* OpenCV
* YOLOv5 (PyTorch)
* Raspberry Pi
* Arduino Nano
* MPU6050 IMU
* Socket Programming

---


## ▶️ Demo Video

(Add YouTube link here)

---

## 📊 Results

* Achieved real-time perception and control
* Stable lane following with smooth steering
* Reliable object detection and response
* Successful integration of AI, vision, and embedded systems

---

## 📅 Latest Updates (March 2026)

* Improved lane detection stability
* Optimized YOLOv5 inference speed
* Added IMU-based correction system
* Enhanced decision-making logic

---

## 📦 Future Improvements

* Path planning
* Full autonomous navigation
* ROS2 optimization

---

## 👥 Team

Team Jarvis

* N Rohit Balaji
* Sujal Choudhary
* Asvith

Mentor: Dr. G. Y. Rajaa Vikhram

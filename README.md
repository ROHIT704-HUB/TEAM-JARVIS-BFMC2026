# Jarvis – BFMC 2026

This repository contains the software implementation for the Bosch Future Mobility Challenge (BFMC) 2026.

## Repository Structure
- **monitoring/**  
  Project plan and system architecture documentation.

- **Project status/**  
  Monthly reports and progress demonstration details.

- **src/**  
  Source code implementing perception, autonomy, and system integration.

## Implemented Features
- Manual vehicle control
- Vision-based stop sign detection
- Real vehicle braking using BFMC serial communication protocol
- Integration of stop sign perception into the BFMC main control loop

## Stop Sign Detection and Braking
The system detects stop signs using a vision-based perception module.
Upon detection, a real braking command (`#brake`) is sent through the BFMC serial interface to the STM32 Nucleo controller.
This command activates the braking state of the vehicle, causing the car to stop physically.

## Demonstration
The project status video demonstrates successful stop sign detection and real vehicle stopping behavior in accordance with competition rules.

## Technologies Used
- Python
- YOLO-based object detection
- BFMC serial command protocol
- Modular perception and autonomy architecture

# Copyright (c) 2019, Bosch Engineering Center Cluj and BFMC organizers
# All rights reserved.

import sys
import time
import os
import psutil

# Pin to CPU cores
available_cores = list(range(psutil.cpu_count()))
psutil.Process(os.getpid()).cpu_affinity(available_cores)

sys.path.append(".")

from multiprocessing import Queue, Event
from src.utils.bigPrintMessages import BigPrint
from src.utils.outputWriters import QueueWriter, MultiWriter
import logging
import logging.handlers

logging.basicConfig(level=logging.INFO)

# ===================================== PROCESS IMPORTS ==================================

from src.gateway.processGateway import processGateway
from src.dashboard.processDashboard import processDashboard
from src.hardware.camera.processCamera import processCamera
from src.hardware.serialhandler.processSerialHandler import processSerialHandler
from src.data.Semaphores.processSemaphores import processSemaphores
from src.data.TrafficCommunication.processTrafficCommunication import processTrafficCommunication
from src.utils.messages.messageHandlerSubscriber import messageHandlerSubscriber
from src.utils.messages.allMessages import StateChange
from src.statemachine.stateMachine import StateMachine
from src.statemachine.systemMode import SystemMode

# ===================== STOP SIGN IMPORTS (NEW) =====================

from src.perception.stopSignDetector import StopSignDetector
from src.autonomy.stopSignHandler import StopSignHandler

# ===================================== SHUTDOWN PROCESS ==================================

def shutdown_process(process, timeout=1):
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join(timeout)
        if process.is_alive():
            process.kill()

# ===================================== PROCESS MANAGEMENT ==================================

def manage_process_life(process_class, process_instance, process_args, enabled, allProcesses):
    if enabled:
        if process_instance is None:
            process_instance = process_class(*process_args)
            allProcesses.append(process_instance)
            process_instance.start()
    else:
        if process_instance is not None and process_instance.is_alive():
            shutdown_process(process_instance)
            allProcesses.remove(process_instance)
            process_instance = None
    return process_instance

# ======================================== SETTING UP ====================================

print(BigPrint.PLEASE_WAIT.value)

allProcesses = []
allEvents = []

queueList = {
    "Critical": Queue(),
    "Warning": Queue(),
    "General": Queue(),
    "Config": Queue(),
    "Log": Queue(),
}

logger = logging.getLogger()

original_stdout = sys.stdout
original_stderr = sys.stderr

queue_writer = QueueWriter(queueList["Log"])
sys.stdout = MultiWriter(original_stdout, queue_writer)
sys.stderr = MultiWriter(original_stderr, queue_writer)

# ===================================== INITIALIZE ==================================

stateChangeSubscriber = messageHandlerSubscriber(queueList, StateChange, "lastOnly", True)
StateMachine.initialize_shared_state(queueList)

# Gateway
processGateway = processGateway(queueList, logger)
processGateway.start()

# ===================================== INITIALIZE PROCESSES ==================================

dashboard_ready = Event()
processDashboard = processDashboard(queueList, logger, dashboard_ready, debugging=False)

camera_ready = Event()
processCamera = processCamera(queueList, logger, camera_ready, debugging=False)

semaphore_ready = Event()
processSemaphore = processSemaphores(queueList, logger, semaphore_ready, debugging=False)

traffic_com_ready = Event()
processTrafficCom = processTrafficCommunication(queueList, logger, 3, traffic_com_ready, debugging=False)

serial_handler_ready = Event()
processSerialHandler = processSerialHandler(
    queueList, logger, serial_handler_ready, dashboard_ready, debugging=False
)

allProcesses.extend([
    processCamera,
    processSemaphore,
    processTrafficCom,
    processSerialHandler,
    processDashboard
])

allEvents.extend([
    camera_ready,
    semaphore_ready,
    traffic_com_ready,
    serial_handler_ready,
    dashboard_ready
])

# ===================== STOP SIGN INITIALIZATION =====================

stop_sign_detector = StopSignDetector()
stop_sign_handler = StopSignHandler()

# ===================================== START PROCESSES ==================================

for process in allProcesses:
    process.daemon = True
    process.start()

# ===================================== STAYING ALIVE ====================================

blocker = Event()

try:
    # Wait for all processes
    for event in allEvents:
        event.wait()

    StateMachine.initialize_starting_mode()

    time.sleep(10)
    print(BigPrint.C4_BOMB.value)
    print(BigPrint.PRESS_CTRL_C.value)

    while True:
        # ===================== STOP SIGN LOGIC =====================
        if stop_sign_detector.detect():
            stop_sign_handler.execute()

        # ===================== BFMC STATE MACHINE ==================
        message = stateChangeSubscriber.receive()
        if message is not None:
            modeDictSemaphore = SystemMode[message].value["semaphore"]["process"]
            modeDictTrafficCom = SystemMode[message].value["traffic_com"]["process"]

            processSemaphore = manage_process_life(
                processSemaphores,
                processSemaphore,
                [queueList, logger, semaphore_ready, False],
                modeDictSemaphore["enabled"],
                allProcesses
            )

            processTrafficCom = manage_process_life(
                processTrafficCommunication,
                processTrafficCom,
                [queueList, logger, 3, traffic_com_ready, False],
                modeDictTrafficCom["enabled"],
                allProcesses
            )

        blocker.wait(0.1)

except KeyboardInterrupt:
    print("\n[MAIN] Keyboard interrupt detected. Shutting down...\n")

    stop_sign_detector.release()

    for proc in reversed(allProcesses):
        proc.stop()
    processGateway.stop()

    for proc in reversed(allProcesses):
        shutdown_process(proc)
    shutdown_process(processGateway)


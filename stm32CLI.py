import serial
import time
import os
import modbus
from JlinkCLI import JlinkFlasher

try:
    import RPi.GPIO as GPIO
except ImportError:
    pass
import re


class Stm32:
    DE_PIN: int = 21

    def __init__(self) -> None:
        OFF: int = 0
        self.AMPY_TIMEOUT = 20
        self.stopped = False
        self.baudrate = 9600
        self.modbusClient = modbus.Modbus()
        self.status = "Inactive"
        self.firmwareVersion = self.get_fimrwareVersion()
        self.serialPort = None
        self.attempt_cnt: int = 0
        try:
            self.serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(Stm32.DE_PIN, GPIO.OUT)
        except:
            pass

        self._stLinkReady = False
        self.jLink = JlinkFlasher()
        self.jLink.testJlinkConnection()

    def get_fimrwareVersion(self):
        arr = os.listdir()
        for i in arr:
            if i[-3:] == "bin":
                return i
        return "0.0"

    def start_flash(self):
        print("Start flashing ...")
        if self.jLink.testJlinkConnection() == False:
            self.status = "jLink not connected!!"
            return

        try:
            self.status = "Upload new firmware, please wait!"
            flashStatus = self.jLink.flashMCU()
            self.jLink.mcuHalt()
            print("Flash status", flashStatus)
            if flashStatus == True:
                self.status = "ok"
            else:
                self.status = "error during flashing"

        except Exception as e:
            self.jLink.mcuHalt()
            self.status = "{}".format(e)

    def start_testing(self):
        reg: int = 1000
        length: int = 3
        try:
            print("start testing")
            GPIO.output(Stm32.DE_PIN, True)
            time.sleep(0.1)
            readRegs = self.modbusClient.read_regs(reg, length)
            self.serialPort.write(readRegs)
            time.sleep(0.015)
            GPIO.output(Stm32.DE_PIN, False)
            receiveData = self.serialPort.readline()
            receiveData = self.modbusClient.mbrtu_data_processing(receiveData)
            evState = (receiveData[2])
            if evState:
                self.status = "ok"
            else:
                self.status = f"nok -> ev status: {evState}"
            self.attempt_cnt = 0
            return "OK"
        except Exception as e:
            self.attempt_cnt += 1
            if self.attempt_cnt <= 5:
                time.sleep(0.5)
                self.start_testing()
            else:
                self.attempt_cnt = 0
                self.status = "fail"
                return "{}".format(e)

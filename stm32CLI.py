import serial
import time
import os
import modbus
from pathlib import Path
from JlinkCLI import JlinkFlasher
try:
    import RPi.GPIO as GPIO
except:
    pass
import re


class Stm32:

    def __init__(self) -> None:
        OFF : int = 0
        self.AMPY_TIMEOUT = 20
        self.stopped = False
        self.baudrate = 9600
        self.modbusClient = modbus.Modbus()
        self.status = "Inactive"
        self.firmwareVersion = self.get_fimrwareVersion()
        self.serialPort = None
        try:
            self.serialPort = serial.Serial("/dev/ttyS0")
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        except:
            pass

        self._stLinkReady = False
        self.jLink = JlinkFlasher()
        self.jLink.testJlinkConnection()

    def get_fimrwareVersion(self):
        arr = os.listdir()
        for i in arr:
            if i[-3:] == "bin":
                version = i[:-4]
                version = version.split("_")
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
            print("Flash status", flashStatus)
            if flashStatus == True:
                self.status =  "ok"
            else:
                self.status =  "error during flashing"    
                            
        except Exception as e:
            self.status = "{}".format(e)
        

    def start_testing(self):
        reg: int = 1000
        length: int = 6
        try:
            print("start testing")
            readRegs = self.modbusClient.read_regs(reg, length)
            self.serialPort.write(readRegs)
            receiveData = self.serialPort.read(5+(2*length))
            receiveData = self.modbusClient.mbrtu_data_processing(receiveData)
            evState = ((receiveData[0]) << 8) | (receiveData[1])
            return "NOK"
        except Exception as e:
            self.status =  "fail"
            return "{}".format(e)


    

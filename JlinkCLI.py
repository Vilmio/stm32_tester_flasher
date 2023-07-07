
import pylink   #pip install pylink-square
from dataclasses import dataclass
import os

TARGET_DEV_NAME = 'STM32G030K6'
SWD_SPEED = 2000

class JlinkFlasher():   
   
    def __init__(self,parent = None  ):
    
        #super(JlinkFlasher, self).__init__(parent)

        self._jlink = pylink.JLink()
        self.binary_file = self.getBinaryFile()
        #self.connectJlink()

    def getBinaryFile(self):
        arr = os.listdir()
        for i in arr:
            if i[-3:] == "bin":
                print("binary file: ",i)
                return i
        return ""
    
    def eraseFlash(self):
        if self._jlink.erase() !=0:
           print("Flash mcu smazana")

    def _connectRequired(foo = None,):
        def wrapper(self):
            try:
                self._jlink.connect(TARGET_DEV_NAME,SWD_SPEED)
            except:
                self.connectMCUError()
            #self.jlink.reset(ms = 10, halt=True)
            return foo(self)
        return wrapper

    @_connectRequired
    def flashMCU(self):

        try:  
           # print("Erase MCU")
           # self._jlink.erase()
           # self._jlink.reset(ms = 10, halt=True)
           print("Upload Lora_485.bin file to MCU")
           self._jlink.flash_file(self.binary_file ,0)
           self._jlink.reset(ms = 10, halt=False)
           return True
        except:
            #self.connectMCUError()
            return False
    

    def flashSerialNumber(self,number = 0):
        #self.jlink.memory_write(EepromAddress["SerialNumber"],[int(165)])
        pass
         
    def connectMCUError(self):
        print("Error during flashing ")
        pass

    def notifyJlinkStat(self,jlinkOK):
        pass

    def connectJlink(self):
        try:
            #self._jlink.open(260102277)
            emuls = self._jlink.connected_emulators()
            self._jlink.open(emuls[0].SerialNumber)
            self._jlink.power_on()
            self._jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
            print("JLink connected")
            return True
        except:
            print("JLink not connected")
            return False

    def testJlinkConnection(self):
        ret = False
        print("Connectio test: ",self._jlink.connected())
        if self._jlink.connected() == False:
            try:
                del self._jlink
                self._jlink = pylink.JLink()
                ret = self.connectJlink()
                self.notifyJlinkStat(True)
                
            except:
                self.notifyJlinkStat(False)

        else:
            ret = True
            self.notifyJlinkStat(True) 
           
        return ret  

    def mcuHalt(self):
        
        while self._jlink.halted() == False:
              self._jlink.halt()

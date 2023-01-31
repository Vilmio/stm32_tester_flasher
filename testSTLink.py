
import subprocess


class STLink(): 
    
    def __init__(self,pathtoProgrammer):
        self.cubeProgPath=pathtoProgrammer

    def scanForSTLinks(self):
        tm = 1.5

        prcs = [ self.cubeProgPath+'/STM32_Programmer_CLI.exe',
                '-l'
                ]
        try:
            out = str(subprocess.check_output(prcs, stderr=subprocess.STDOUT, timeout=tm,creationflags=subprocess.CREATE_NO_WINDOW))

        except:
            return 1    #restart Link


        if 'No ST-Link detected!' in out:
            return 0
            

        elif 'DEV_USB_COMM_ERR' in out:
            return 1    #restart Link 

        return 2
        

    def connectToMCU(self):
    
        tm = 1

        prcs = [ self.cubeProgPath+'/STM32_Programmer_CLI.exe',
                '-c',
                'port=SWD',
                'freq=4000'
                ]
        try:
            out = str(subprocess.check_output(prcs, stderr=subprocess.STDOUT, timeout=tm,creationflags=subprocess.CREATE_NO_WINDOW))

        except:
            return False

        if 'Device type : MCU' in out:
            return True

        return False

    def eraseMCU(self):

        tm = 2
        prcs = [ self.cubeProgPath+'/STM32_Programmer_CLI.exe',
                '-c',
                'port=SWD',
                'freq=4000',
                '-e',
                'all'
                ]
        try:
            out = str(subprocess.check_output(prcs, stderr=subprocess.STDOUT, timeout=tm,creationflags=subprocess.CREATE_NO_WINDOW))

        except:
            return False

        if 'Mass erase successfully achieved' in out:
            return True
        
        return False


    def flashMCU(self,file, startAddr: int = 0x8000000, id: int = 0 ):
        
        tm = 5

        prcs = [ self.cubeProgPath+'/STM32_Programmer_CLI.exe',
                '-c',
                'port=SWD',
                'freq=4000',
                '-w',
                file,
                startAddr,
                '-v'
                ]
        try:
            out = str(subprocess.check_output(prcs, stderr=subprocess.STDOUT, timeout=tm,creationflags=subprocess.CREATE_NO_WINDOW))

        except:
            out = ''

        if 'Download verified successfully' in out:
            return True
        
        return False


    def resetMCU(self):

        tm = 1
        
        prcs = [ self.cubeProgPath+'/STM32_Programmer_CLI.exe',
                '-c',
                'port=SWD',
                'freq=4000',
                '-rst'
                ]
        try:
            out = str(subprocess.check_output(prcs, stderr=subprocess.STDOUT, timeout=tm,creationflags=subprocess.CREATE_NO_WINDOW))

        except:
            return False

        if 'Software reset is performed' in out:
            return True
        
        return False


    def writeU32ToMem(self,addr,u32):
        tm = 1
        
        prcs = [self.cubeProgPath+'/STM32_Programmer_CLI.exe',
                '-c',
                'port=SWD',
                '-w32',
                (addr),
                hex(u32),
                '-v'
                ]
        try:
            out = str(subprocess.check_output(prcs, stderr=subprocess.STDOUT, timeout=tm,creationflags=subprocess.CREATE_NO_WINDOW))

        except:
            return False

        if 'Download verified successfully' in out:
            return True
    
        return False
        
  
    def writeU8ToMem(self,addr,u32):
        tm = 1

        prcs = [ self.cubeProgPath+'/STM32_Programmer_CLI.exe',
                '-c',
                'port=SWD',
                'freq=4000',
                '-w8',
                (addr),
                hex(u32),
                '-v'
                ]
        try:
            out = str(subprocess.check_output(prcs, stderr=subprocess.STDOUT, timeout=tm,creationflags=subprocess.CREATE_NO_WINDOW))

        except:
            return False

        if 'Downloading 8-bit data done successfully' in out:
            return True
    
        return False


    def readU32Mem(self,addr):
        tm = 1
        
        prcs = [self.cubeProgPath+'/STM32_Programmer_CLI.exe',
                '-c',
                'port=SWD',
                '-r32',
                (addr),
                '12',
                ]
        try:
            out = str(subprocess.check_output(prcs, stderr=subprocess.STDOUT, timeout=tm,creationflags=subprocess.CREATE_NO_WINDOW))

        except:
            return False

        if 'Reading 32-bit memory content' in out:
            ID=out[out.find(addr+' : ')+len(addr+' : '):]
            ID=ID[0:26]
            ID=ID.replace(" ","")
            return ID
    
        return False

    def readU8Mem(self,addr,size):
        tm = 1
        prcs = [self.cubeProgPath+'/STM32_Programmer_CLI.exe',
                '-c',
                'port=SWD',
                '-r8',
                (addr),
                str(size),
                ]
        try:
            out = str(subprocess.check_output(prcs, stderr=subprocess.STDOUT, timeout=tm,creationflags=subprocess.CREATE_NO_WINDOW))

        except:
            return False

        if 'Flash size  :' in out:
            val=out[out.find(addr+' : ')+len(addr+' : '):]
            val=val.replace(" ","")
            val=val[0:size*2]
            
            return val
    
        return False

   
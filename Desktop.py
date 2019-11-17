from datetime import datetime
import ctypes


class Desktop:

    def __init__(self,path:str):
        #Use to set desktop image
        self.SPI_SETDESKWALLPAPER=0x0014
        #Use to set pattern to picture if ever needed
        self.SPI_SETDESKPATTERN=0x0015 
        #Use this for the flag
        self.SPI_UPDATEFLAG=0X01
        #path to image
        self.img_path=path+'C:/Users/icmuz/Pictures/Saved Pictures/apple.jpg'

    def updateBackground(self):
        #Uses C functionality set image to desktop
        user32 = ctypes.windll.user32
        success=user32.SystemParametersInfoW(self.SPI_SETDESKWALLPAPER,0,self.img_path,self.SPI_UPDATEFLAG)
    
    def updateImg(self, img_path):
        #updates image path
        self.img_path=img_path

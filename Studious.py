import ctypes

#Use to set desktop image
SPI_SETDESKWALLPAPER=0x0014
#Use to set pattern to picture if ever needed
SPI_SETDESKPATTERN=0x0015 
#Use this for the flag
SPI_UPDATEFLAG=0X01

img_path='C:/Users/icmuz/Pictures/Saved Pictures/apple.jpg'

user32 = ctypes.windll.user32
success=user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER,0,img_path,SPI_UPDATEFLAG)


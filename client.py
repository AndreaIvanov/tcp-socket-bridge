import socket
import time
import random

nome_server = socket.gethostname()
host = "127.0.0.1"
port = 1239
valore_temp = round(random.uniform(-273.15, 200), 2)


# CREAZIONE SOCKET

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if valore_temp >= -273.15 and valore_temp <= 200:

    try:
        # valore_temp = 1000 # mettiamo caso che in qualche modo strano il client bypassi i controlli ...
        print(f"(INFO) La temperatura di {valore_temp}°C è valida!\n")
        # CONNESSIONE AL SERVER
        print(f"Tentativo di connessione a [{host}:{port}]\n")
        client_socket.connect((host, port)) # def connect(self, address: _Address, /) -> None: ...
        print(f"[SUCCESS] Connesso al server [{nome_server}]!\n")

        # IMPORTANTE: Il server fa .decode(), quindi noi dobbiamo fare .encode()
        client_socket.send(str(valore_temp).encode('utf-8')) #da int la temperatura viene passata come stringa

        # INVIO MESSAGGIO
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[SUCCESS] Messaggio inviato dal client con successo! [{timestamp}]\n")

        # RICEZIONE MESSAGGIO SERVER
        risposta_dal_server = client_socket.recv(1024).decode('utf-8')
        print(f"Hai ricevuto il seguente messaggio dal server [{nome_server}]:\n\n[INIZIO SERVER-MSG]\n{risposta_dal_server}\n[FINE SERVER-MSG]\n")

    # GESTIONE ERRORI, GRAZIE PYTHON!
    except ConnectionRefusedError:
        print("(ERROR) Il server è spento o la porta è sbagliata.\n")
    except Exception as e:
        print(f"(ERROR) Errore imprevisto: {e}\n")

    finally:
        # CHIUSURA CONNESSIONE
        client_socket.close()
        print("[CLOSED] Connessione chiusa.\n")
else:
    print("Temperatura non valida!\n")
    exit()
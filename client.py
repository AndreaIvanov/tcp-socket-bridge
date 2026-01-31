import socket

nome_server = socket.gethostname()
host = "127.0.0.1"
port = 1237

# CREAZIONE SOCKET

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # CONNESSIONE AL SERVER
    print(f"Tentativo di connessione a {host}:{port}...\n")
    client_socket.connect((host, port)) # def connect(self, address: _Address, /) -> None: ...
    print(f"[SUCCESS] Connesso al server [{nome_server}]!\n")

    # PREPARAZIONE MESSAGGIO
    testo = input("Scrivi qualcosa da inviare al server: ")

    # IMPORTANTE: Il server fa .decode(), quindi noi dobbiamo fare .encode()
    client_socket.send(testo.encode('utf-8'))

    # INVIO MESSAGGIO
    print("[SUCCESS] Messaggio inviato dal client con successo!\n")

    # RICEZIONE MESSAGGIO SERVER
    risposta_dal_server = client_socket.recv(1024).decode('utf-8')
    print(f"[INIZIO SERVER-MSG]Hai ricevuto il seguente messaggio dal server [{nome_server}]:\n\n{risposta_dal_server}\n\n[FINE SERVER-MSG]\n")

# GESTIONE ERRORI, GRAZIE PYTHON
except ConnectionRefusedError:
    print("(ERROR) Il server è spento o la porta è sbagliata.\n")
except Exception as e:
    print(f"(ERROR) Errore imprevisto: {e}\n")

finally:
    # CHIUSURA
    client_socket.close()
    print("[CLOSED] Connessione chiusa.\n")
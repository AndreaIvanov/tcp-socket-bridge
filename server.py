import socket
import time

nome_server = socket.gethostname()
host = "127.0.0.1"
port = 1239
is_alive = True
file_di_log = "log_temperatura.txt"

# LISTA IP AUTORIZZATI
IP_AUTORIZZATI = ["127.0.0.1"]

# CREAZIONE SOCKET
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # INET = con IP esposto mentre UNIX localmente solo per la macchina

# GESTIONE ERRORE QUALORA PORTA FOSSE OCCUPATA DAL SISTEMA
try:
    server_socket.bind((host, port))  # def bind(self, address: _Address, /) -> None: ... 1 oggetto solo
except OSError as e:
    print(f"La seguente porta [{port}] è gia in uso.\n")
    exit()

# SOCKET IN ASCOLTO ED ATTESA
if is_alive == True:
    print(f"Server persistente attivo su [{host}:{port}]\n\n")
else:
    print(f"Server persistente non attivo, riavviare!\n")
    exit()

server_socket.listen(5)  # tieni in coda fino a 5 client alla volta!
counter = 0

try:
    while is_alive:
        conn, addr = server_socket.accept()  # conn, addr = server.accept()

        # CONTROLLO IP
        ip_client = addr[0]

        # LOGICA FIREWALL
        if ip_client not in IP_AUTORIZZATI:
            print(f"[REJECTED] Accesso negato per l'indirizzo: {ip_client}")
            conn.send("ERRORE) Accesso non autorizzato dal firewall del server.".encode('utf-8'))
            conn.close()
            continue  # salta il resto del ciclo per non ricevere nemmeno il messaggio dal client!

        counter += 1
        # CONNESSIONE CLIENT
        print(f"----------------------------\n[CONNESSO] Cliente [{counter}] {conn} connesso dall'indirizzo: {addr}\n")

        # STAMPA MESSAGGIO
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            messaggio_client = conn.recv(1024).decode('utf-8')  # def recv(self, bufsize: int, flags: int = 0, /) -> bytes: ...  1024 è la dimensione massima del pacchetto di dati

            # VALIDAZIONE RANGE (Sicurezza del dato)
            try:
                temp_float = float(messaggio_client)
                if -273.15 <= temp_float <= 200:
                    stato_validazione = True
                    messaggio_validazione = "OK"
                else:
                    stato_validazione = False
                    messaggio_validazione = "FUORI RANGE"

            except ValueError:
                stato_validazione = False
                messaggio_validazione = "ERRORE (DATO NON VALIDO)"

            # SE LO STATO DI VALIDAZIONE È FALSO, CHIUDIAMO E SALTIAMO TUTTO
            if stato_validazione == False:
                conn.close()  # chiudiamo senza mandare risposta
                print(f"[DISCONNESSO] Cliente [{counter}] {conn}.\n")
                print("[DISK] Dati non salvati nel log.")
                print(f"STATUS : [{messaggio_validazione}]\n----------------------------\n\n\n\n")
                continue  # torniamo all'inizio del ciclo while per il prossimo client


            print(f"Hai ricevuto il seguente messaggio dal client [{counter}][{timestamp}]:\n\n[INIZIO CLIENT-MSG] \n{messaggio_client} (Stato: {messaggio_validazione})\n[FINE CLIENT-MSG]\n")

            # MODIFICA MESSAGGIO
            if stato_validazione == True:
                messaggio_server = f"(INFO-SERVER) Ho ricevuto la temperatura : {messaggio_client}°C"
            else:
                messaggio_server = f"(ERRORE-SERVER) Il dato [{messaggio_client}] non è valido: {stato_validazione}"

            # INVIO MESSAGGIO MODIFICATO
            conn.send(messaggio_server.encode('utf-8'))  # encode mi raccomando!
            print(f"[INVIATO] Risposta elaborata spedita al cliente [{counter}]\n")

            # CHIUSURA CONNESSIONE
            conn.close()  # chiusura connessione
            print(f"[DISCONNESSO] Cliente [{counter}] {conn}.\n")

            # LOGICA DI SALVATAGGIO SU FILE
            log_line = f"[{timestamp}] Client {counter} ({ip_client}) - Temp: {messaggio_client}°C - Stato: {messaggio_validazione}\n"

            with open(file_di_log, "a", encoding="utf-8") as f:
                f.write(log_line)
                print("[DISK] Dati salvati correttamente nel log.")
                print(f"STATUS : [{messaggio_validazione}]\n----------------------------\n\n\n\n")

        # GESTIONE ERRORI, GRAZIE PYTHON!
        except ConnectionResetError:
            print(f"(ERRORE) Il cliente ha chiuso la connessione improvvisamente!")
        except UnicodeDecodeError:
            print(f"(ERRORE) Il cliente ha inviato dati che non sono nel formato UTF-8!\n")

except KeyboardInterrupt:
    print(f"[DEBUG] Server interrotto manualmente!")
finally:
    server_socket.close()
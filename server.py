import socket

nome_server = socket.gethostname()
numero_connessioni = 3
host = "127.0.0.1"
port = 1237

risposta_modificata = f"Si te lo meriti il 10 a prescindere!"

"""
socket() -- create a new socket object
socketpair() -- create a pair of new socket objects [*]
fromfd() -- create a socket object from an open file descriptor [*]
send_fds() -- Send file descriptor to the socket.
recv_fds() -- Receive file descriptors from the socket.
fromshare() -- create a socket object from data received from socket.share() [*]
gethostname() -- return the current hostname
gethostbyname() -- map a hostname to its IP number
gethostbyaddr() -- map an IP number or hostname to DNS info
getservbyname() -- map a service name and a protocol name to a port number
getprotobyname() -- map a protocol name (e.g. 'tcp') to a number
ntohs(), ntohl() -- convert 16, 32 bit int from network to host byte order
htons(), htonl() -- convert 16, 32 bit int from host to network byte order
inet_aton() -- convert IP addr string (123.45.67.89) to 32-bit packed format
inet_ntoa() -- convert 32-bit packed format IP to string (123.45.67.89)
socket.getdefaulttimeout() -- get the default timeout value
socket.setdefaulttimeout() -- set the default timeout value
create_connection() -- connects to an address, with an optional timeout and
                       optional source address.
"""

# CREAZIONE SOCKET
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #INET = con IP esposto mentre UNIX localmente solo per la macchina

# GESTIONE ERRORE QUALORA PORTA FOSSE OCCUPATA DAL SISTEMA
try:
    server_socket.bind((host,port)) # def bind(self, address: _Address, /) -> None: ... 1 oggetto solo
except OSError as e:
    print(f"La seguente porta [{port}] è gia in uso.\n")
    exit()

# SOCKET IN ASCOLTO ED ATTESA
server_socket.listen(numero_connessioni) # def listen(self, backlog: int = ..., /) -> None: ... numero_connessioni richieste per volta gestibili
plurale = "connessioni" if numero_connessioni > 1 else "connessione"
print(f"Il [{nome_server}] è pronto a ricevere [{numero_connessioni}] {plurale} all'indirizzo {host}:{port}") # printf più elegante
print("In attesa di un cliente...\n")

counter = 0
try:
    while counter < numero_connessioni:
        counter += 1
        conn, addr = server_socket.accept() # conn, addr = server.accept()

        # CONNESSIONE CLIENT
        print(f"[CONNESSO] Cliente [{counter}] {conn} connesso dall'indirizzo: {addr}\n")

        # STAMPA MESSAGGIO
        try:
            messaggio = conn.recv(1024).decode('utf-8') # def recv(self, bufsize: int, flags: int = 0, /) -> bytes: ...  1024 è la dimensione massima del pacchetto di dati --> i dati arrivano "grezzi" (bytes), li trasformiamo in testo (stringa)
            print(f"[INIZIO CLIENT-MSG] Hai ricevuto il seguente messaggio dal client [{counter}]:\n\n{messaggio}\n\n[FINE CLIENT-MSG]\n")

            # MODIFICA MESSAGGIO

            conn.send(risposta_modificata.encode('utf-8')) # encode mi raccomando!
            print(f"[INVIATO] Risposta elaborata spedita al cliente [{counter}]\n")


        except ConnectionResetError:
            print(f"(ERRORE) Il cliente ha chiuso la connessione improvvisamente!")
        except UnicodeDecodeError:
            print(f"(ERRORE) Il cliente ha inviato dati che non sono nel formato UTF-8!\n")

        # CHIUSURA CONNESSIONE
        conn.close() # chiusura connessione

except KeyboardInterrupt:
    print(f"[DEBUG] Server interrotto manualmente!")
finally:
    server_socket.close()



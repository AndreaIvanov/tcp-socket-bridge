# 🚀 TCP Socket Bridge: Architettura Client-Server in Python
### Relazione Tecnica Integrata - Sistemi e Reti

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Protocol](https://img.shields.io/badge/Protocol-TCP%2FIP-red.svg)](#)
[![Layer](https://img.shields.io/badge/OSI--Layer-4%20(Transport)-green.svg)](#)

## 1. Panoramica del Progetto
Il progetto implementa una comunicazione bidirezionale affidabile tra un **Server** e un **Client** basata sullo stack **TCP/IP**. L'analisi si concentra sul **Livello 4 (Trasporto)**, garantendo l'integrità del dato e la corretta gestione del flusso tramite l'interfaccia dei Socket.

---

## 2. Architettura e Workflow
Il sistema segue il modello di comunicazione *connection-oriented*. A differenza di protocolli stateless (come UDP), il TCP stabilisce una sessione dedicata prima dello scambio dati.



### Matrice delle Funzionalità
| Metodo | Entità | Descrizione Tecnica |
| :--- | :--- | :--- |
| **`socket()`** | Entrambi | Inizializzazione dell'endpoint (Famiglia: `AF_INET`, Tipo: `SOCK_STREAM`). |
| **`bind()`** | Server | Associazione del socket all'indirizzo IP (`127.0.0.1`) e alla porta (`1237`). |
| **`listen()`** | Server | Configurazione dello stato passivo con definizione della coda di attesa. |
| **`connect()`** | Client | Avvio della procedura di **Three-Way Handshake**. |
| **`accept()`** | Server | Metodo bloccante per la generazione di un socket dedicato alla sessione. |
| **`send/recv()`**| Entrambi | Scambio di buffer binari con codifica/decodifica **UTF-8**. |

---

## 3. Guida all'Esecuzione

### Workflow di Test
1. **Avvio Server:** Eseguire `python server.py`. Il sistema rimarrà in attesa sulla porta 1237.
2. **Avvio Client:** Aprire un secondo terminale ed eseguire `python client.py`.
3. **Scambio Dati:** Inviare una stringa dal client per ricevere il feedback dal server.

### Analisi dei Terminali
* **Lato Server:** Viene visualizzato l'endpoint del client composto da IP e **porta effimera** (es. `54321`).
* **Lato Client:** Viene visualizzata la risposta di validazione processata dal server.

---

## 4. Configurazione e Variabili
È possibile personalizzare i parametri di rete modificando le seguenti costanti nel codice:

* **Indirizzo IP (`127.0.0.1`):** Interfaccia di loopback. Modificare con l'IP locale per test su nodi distinti.
* **Porta (`1237`):** Porta applicativa. Se occupata, utilizzare valori nel range 1024-65535.
* **Payload:** La logica di risposta può essere modificata agendo sulla funzione `.send()` nel file `server.py`.

---

## 5. Robustezza e Troubleshooting

| Errore | Causa | Soluzione |
| :--- | :--- | :--- |
| **OSError** | Porta già in uso. | Terminare i processi pendenti o cambiare porta. |
| **ConnectionRefused** | Server non raggiungibile. | Verificare che `server.py` sia in esecuzione. |
| **Decoding Error** | Formato dati non valido. | Assicurarsi di utilizzare `.encode()`/`.decode()` UTF-8. |

---

## 6. Conclusioni Tecniche
L'implementazione mette in risalto tre caratteristiche fondamentali del protocollo TCP:
1. **Affidabilità:** Controllo degli errori e riscontro dei pacchetti (ACK).
2. **Sequenzialità:** Consegna dei segmenti nell'ordine corretto.
3. **Gestione Risorse:** Rilascio dei descrittori di file tramite blocchi `finally`.

---
**Sviluppatore:** Andrea Ivanov 

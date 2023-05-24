import sqlite3
import socket
import threading
import pickle

# Crearea serverului
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen()

# Aflam si afisam adresa IP si portul pe care ruleaza serverul
host, port = server.getsockname()
print(f'Serverul ruleaza pe IP: {host} si PORT: {port}')

# O lista pentru a tine evidenta clientilor conectati
clients = []
# Un dictionar pentru a tine evidenta obiectelor selectate de fiecare client
client_data = {}

def notify_clients(key):
    conn = sqlite3.connect('reteleProiect.db')
    c = conn.cursor()
    c.execute("SELECT * FROM STUDENTI WHERE ID = ?", (key,))
    updated_student = c.fetchone()
    for client in clients:
        if key in client_data[client]:
            client.send(pickle.dumps(('MODIFIED', updated_student)))

def handle_client(client):
    # Conectarea la baza de date
    conn = sqlite3.connect('reteleProiect.db')
    c = conn.cursor()

    while True:
        request = pickle.loads(client.recv(1024))
        if request == 'CLOSE':
            print(f'Clientul {client.getpeername()[0]} s-a deconectat.')
            clients.remove(client)
            client.close()
            break

        # Daca clientul interogheaza lista studentilor
        elif request == 'INTEROGARE':
            c.execute("SELECT * FROM STUDENTI")
            result = c.fetchall()
            client.send(pickle.dumps(result))

        elif isinstance(request, tuple) and request[0] == 'SELECTARE':
            c.execute("SELECT * FROM STUDENTI WHERE ID = ?", (request[1],))
            if c.fetchone() is not None:
                client_data[client].add(request[1])
                client.send(pickle.dumps('SELECTAT'))
            else:
                client.send(pickle.dumps('NU_EXISTA'))

        # Daca clientul adauga un student
        elif isinstance(request, tuple) and request[0] == 'ADAUGARE':
            c.execute("SELECT * FROM STUDENTI WHERE ID = ? AND Nume = ?", (request[1], request[2]))
            if c.fetchone() is not None:
                client.send(pickle.dumps('EXISTA'))
            else:
                c.execute("INSERT INTO STUDENTI (ID, Nume) VALUES (?, ?)", (request[1], request[2]))
                conn.commit()
                notify_clients(request[1])
                client.send(pickle.dumps(('ADAUGAT', request[1])))

        # Daca clientul modifica un student
        elif isinstance(request, tuple) and request[0] == 'UPDATE':
            c.execute("SELECT * FROM STUDENTI WHERE ID = ? AND Nume = ?", (request[1], request[2]))
            if c.fetchone() is not None:
                client.send(pickle.dumps('EXISTA'))
            else:
                c.execute("SELECT * FROM STUDENTI WHERE NUME = ?", (request[2],))
                if c.fetchone() is not None:
                    client.send(pickle.dumps('EXISTA'))
                else:
                    c.execute("UPDATE STUDENTI SET Nume = ? WHERE ID = ?", (request[2], request[1]))
                    conn.commit()
                    notify_clients(request[1])
                    client.send(pickle.dumps('ACTUALIZAT'))

        # Daca clientul sterge un student
        elif isinstance(request, tuple) and request[0] == 'STERGERE':
            c.execute("SELECT * FROM STUDENTI WHERE ID = ?", (request[1],))
            if c.fetchone() is not None:
                c.execute("DELETE FROM STUDENTI WHERE ID = ?", (request[1],))
                conn.commit()
                notify_clients(request[1],)
                c.execute("SELECT * FROM STUDENTI WHERE ID = ?", (request[1],))
                if c.fetchone() is None:
                    client.send(pickle.dumps('STERGERE'))
                else:
                    client.send(pickle.dumps('EXISTA'))
            else:
                client.send(pickle.dumps('NU_EXISTA'))

while True:
    client, address = server.accept()
    clients.append(client)
    client_data[client] = set()
    print(f'Clientul {address[0]} s-a conectat la server.')
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
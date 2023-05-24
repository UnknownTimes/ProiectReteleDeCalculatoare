import socket
import pickle

def print_menu():
    print()
    print('1. Interogare lista studenti')
    print('1.5 Selectare student pentru a fi notificat daca se schimba')
    print('2. Adaugare student')
    print('3. Modificare student')
    print('4. Stergere student')
    print('5. Inchidere program')
    print('Daca se modifica un student la care esti abonat, trebuie sa faci interogarea de 2 ori')
    print()

def is_numeric(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def handle_menu(client):
    while True:
        print_menu()
        choice = input('Introdu optiunea dorita: ')

        if choice == '1':
            # Interogam lista studentilor
            client.send(pickle.dumps('INTEROGARE'))
            while True:
                response = pickle.loads(client.recv(1024))
                if response[0] == 'MODIFIED':
                    print(f'Studentul {response[1]} a fost modificat.')
                else:
                    print('Studenti:')
                    for student in response:
                        print(student)
                break

        elif choice == '1.5':
            # Selectam un student pentru a fi notificati la schimbari
            id = input('Introdu ID-ul studentului pe care vrei sa-l selectezi: ')
            if not is_numeric(id):
                print('ID-ul trebuie sa fie numeric.')
                continue
            client.send(pickle.dumps(('SELECTARE', id)))
            response = pickle.loads(client.recv(1024))
            if response == 'SELECTAT':
                print('Ai selectat studentul pentru a fi notificat la schimbari.')
            elif response == 'NU_EXISTA':
                print('Studentul nu exista.')

        elif choice == '2':
            # Adaugam un student
            id = input('Introdu ID-ul pentru noul student: ')
            if not is_numeric(id):
                print('\n ID-ul trebuie sa fie numeric. \n')
                continue
            nume = input('Introdu numele noului student: ')
            client.send(pickle.dumps(('ADAUGARE', id, nume)))
            notification = pickle.loads(client.recv(1024))
            if notification[0] == 'ADAUGAT':
                print(f'Studentul cu ID-ul {notification[1]} a fost adaugat cu succes.')
            elif notification == 'EXISTA':
                print('Un student cu acelasi ID si nume exista deja.')

        elif choice == '3':
            # Modificam un student existent
            id = input('Introdu ID-ul studentului pe care vrei sa-l modifici: ')
            if not is_numeric(id):
                print('ID-ul trebuie sa fie numeric.')
                continue
            new_nume = input('Introdu noul nume al studentului: ')
            client.send(pickle.dumps(('UPDATE', id, new_nume)))
            response = pickle.loads(client.recv(1024))
            if response == 'EXISTA':
                print('Un student cu acest ID are deja numele specificat.')
            elif response == 'ACTUALIZAT':
                print('Studentul a fost actualizat cu succes.')

        elif choice == '4':
            # Stergem un student existent
            id = input('Introdu ID-ul studentului pe care vrei sa-l stergi: ')
            if not is_numeric(id):
                print('ID-ul trebuie sa fie numeric.')
                continue
            client.send(pickle.dumps(('STERGERE', id)))
            response = pickle.loads(client.recv(1024))
            if response == 'STERGERE':
                print(f'Studentul cu ID-ul {id} a fost sters cu succes.')
            elif response == 'NU_EXISTA':
                print(f'Studentul cu ID-ul {id} nu exista.')

        elif choice == '5':
            # Inchidem programul
            client.send(pickle.dumps('CLOSE'))
            break
        else:
            print('Optiunea introdusa nu este valida.')

# Crearea clientului
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

handle_menu(client)
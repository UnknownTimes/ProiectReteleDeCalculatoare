import socket
import pickle

def print_menu():
    print('1. Interogare lista studenti')
    print('2. Adaugare student')
    print('3. Modificare student')
    print('4. Stergere student')
    print('5. Inchidere program')
    print()

def handle_menu(client):
    while True:
        print_menu()
        choice = input('Introdu optiunea dorita: ')

        if choice == '1':
            # Interogam lista studentilor
            client.send(pickle.dumps('INTEROGARE'))
            response = pickle.loads(client.recv(1024))
            print('Studenti:')
            for student in response:
                print(student)

        elif choice == '2':
            # Adaugam un student
            id = input('Introdu ID-ul pentru noul student: ')
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
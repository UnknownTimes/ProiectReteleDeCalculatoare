
# Importuri si variabile "globale"
# ==========================================================

import sqlite3
conn = sqlite3.connect('reteleProiect.db')

studenti = 'STUDENTI'
lista_studenti = []

cursor = conn.cursor()

# Afisare intrari din tabela STUDENTI din baza de date.
# ==========================================================

cursor.execute(f"SELECT * FROM {studenti}")
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()

# Functie si apel pentru a adauga un student in baza de date.
# ==========================================================

def adauga_student_inDB(student):
    conn = sqlite3.connect('reteleProiect.db')
    cursor = conn.cursor()
    # verifica daca exista deja un student cu acelasi ID
    select_student_by_id = "SELECT * FROM studenti WHERE id = ?"
    cursor.execute(select_student_by_id, (student[0],))
    result = cursor.fetchone()
    if result is not None:
        print("Studentul cu acest ID exista deja in baza de date.")
        return

    # daca nu exista un student cu acelasi ID sau nume, adauga noul student
    insert_student = "INSERT INTO studenti (id, nume) VALUES (?, ?)"
    cursor.execute(insert_student, student)
    conn.commit()
    print("Studentul a fost ADAUGAT cu succes in baza de date!")
    cursor.close()
    conn.close()

id = int(input("Introduceti ID: "))
nume = input("Introduceti numele: ")

student_nou = (id, nume)

adauga_student_inDB(student_nou)
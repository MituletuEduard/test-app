import sqlite3
import hashlib
import pickle
import subprocess
import os

# --- VULNERABILITATE 1: Hardcoded Credentials ---
# CodeQL va detecta cheia secretă lăsată direct în cod
AWS_ACCESS_KEY = "AKIA1234567890EXAMPLE"
DB_PASSWORD = "supersecretpassword123"


def vulnerable_sql_query(user_input):
    # Creăm o bază de date temporară în memorie
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")

    # --- VULNERABILITATE 2: SQL Injection ---
    # Concatenarea string-urilor este periculoasă
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    print(f"Executare query: {query}")
    cursor.execute(query)
    conn.close()


def vulnerable_command_execution(filename):
    print(f"Citire fișier: {filename}")

    # --- VULNERABILITATE 3: Command Injection ---
    # Dacă utilizatorul introduce "; rm -rf /", comanda va fi executată
    # shell=True este periculos
    subprocess.call("type " + filename, shell=True)


def weak_hashing(password):
    # --- VULNERABILITATE 4: Weak Cryptography ---
    # MD5 este spart și nu trebuie folosit pentru parole
    h = hashlib.md5(password.encode())
    print(f"Hash MD5: {h.hexdigest()}")


def unsafe_deserialization(data_bytes):
    # --- VULNERABILITATE 5: Insecure Deserialization ---
    # pickle.loads poate executa cod arbitrar dacă datele sunt malițioase
    try:
        obj = pickle.loads(data_bytes)
        print("Obiect încărcat.")
    except:
        print("Eroare la deserializare")


def main():
    print("--- Start Aplicație Vulnerabilă ---")

    # Simulăm input de la utilizator (CodeQL urmărește fluxul datelor de aici)
    user_in = input("Introdu username pentru căutare: ")
    vulnerable_sql_query(user_in)

    file_in = input("Introdu nume fișier de citit: ")
    vulnerable_command_execution(file_in)

    pass_in = input("Introdu parola pentru hash: ")
    weak_hashing(pass_in)

    # Simulare date binare primite din exterior
    unsafe_deserialization(b"cos\nsystem\n(S'echo HACKED'\ntR.")


if __name__ == "__main__":
    main()

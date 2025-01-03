import socket
from cryptography.fernet import Fernet
import json
from decouple import config

KEY = config('KEY')
KEY_BYTES = KEY.encode('utf-8')
cipher_suite = Fernet(KEY_BYTES)

HOST = '127.0.0.1'  #'localhost'
PORT = 65432

def get_user_data():
    name = input("Введите имя: ")
    email = input("Введите email: ")
    age = int(input("Введите возраст: "))
    return {"name": name, "email": email, "age": age}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    user_data = get_user_data()
    json_data = json.dumps(user_data).encode('utf-8')
    encrypted_data = cipher_suite.encrypt(json_data)
    client_socket.sendall(encrypted_data)
    print("Данные отправлены серверу.")



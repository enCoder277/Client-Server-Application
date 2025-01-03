import socket
from cryptography.fernet import Fernet
import json
import django
import os
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataPipeline.settings')
django.setup()

from data_app.models import UserData

KEY = config('KEY')
KEY_BYTES = KEY.encode('utf-8')
cipher_suite = Fernet(KEY_BYTES)

HOST = '127.0.0.1'
PORT = 65432

def save_to_db(data):
    try:
        UserData.objects.create(**data)
        print("Данные успешно сохранены в БД.")
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Подключение от {addr}")
            encrypted_data = conn.recv(1024)
            if not encrypted_data:
                break
            decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
            data = json.loads(decrypted_data)
            save_to_db(data)








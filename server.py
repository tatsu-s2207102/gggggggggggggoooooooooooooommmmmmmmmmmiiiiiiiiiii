# -*- coding: utf-8 -*-
import socket
import threading

users = {
    "tatsu": "Tatsu0532",
    "yuki": "Yuki2525Masa",
    "yuha": "hayasi",
    "aoki": "aoki2871"
}

def handle_client(client_socket, addr, username):
    print({addr} + "が接続しました。")
    broadcast({username} + "が入室しました。", exclude=[client_socket])
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print({username} + ": " + {message})
            broadcast({username}+": " + {message}, exclude=[client_socket])
        except:
            break
    print({username} + "が退出しました。")
    broadcast({username} + "が退出しました。")
    client_socket.close()

def broadcast(message, exclude=[]):
    for client in clients:
        if client not in exclude:
            try:
                client.sendall(message.encode())
            except:
                clients.remove(client)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((localip, 80))
    server_socket.listen(5)

    print("サーバーを起動しました。")
    print(f"サーバーのIPアドレス: " + localip +", ポート番号: 80 で待ち受け中...")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        username, password = client_socket.recv(1024).decode().split(":")
        if username in users and users[username] == password:
            print({username} + "が認証に成功しました。")
            client_socket.sendall("success".encode())
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, username))
            client_handler.start()
        else:
            print({username} + "が認証に失敗しました。")
            client_socket.sendall("fail".encode())
            client_socket.close()

clients = []

if __name__ == "__main__":
    host = socket.gethostname()
    print(host)
    localip = socket.gethostbyname(host)
    start_server()

import socket
import threading
import sys
import time
import os
def receive_message(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print(message)
        except:
            break

def send_data(ip, port):
    try:
        # ソケットオブジェクトを作成し、指定したIPアドレスとポート番号に接続
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))

        for i in range(3):
            message = f"Message {i+1}"
            client_socket.sendall(message.encode())
            print(f"送信 {i+1}: {message}")

        client_socket.close()
    except Exception as e:
        print(f"送信エラー: {e}")

def clear_console():
    if os.name == 'nt':
        # Windowsの場合
        os.system('cls')
    else:
        # Windows以外（Linux、macOSなど）の場合
        os.system('clear')

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        port = 80
        client_socket.connect((host, port))
    except:
        print("サーバーに接続できません。 pingを送信しています...")
        send_data(target_ip, target_port)
        return

    username = input("ユーザー名を入力してください: ")
    password = input("パスワードを入力してください: ")

    login_data = f"{username}:{password}"
    client_socket.sendall(login_data.encode())

    response = client_socket.recv(1024).decode()

    if response == "success":
        print("認証に成功しました。チャットに接続しています。")
        time.sleep(1)  # 1秒間待つ
        clear_console()
        receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
        receive_thread.start()

        try:
            while True:
                message = input()
                if message.lower() == "dc":
                    print("切断しました。❌などを押してプログラムを終了させてください。")
                    return
                client_socket.sendall(message.encode())
        except:
            pass

        client_socket.close()
    else:
        print("認証に失敗しました。接続を終了します.")

if __name__ == "__main__":  
    target_ip = "192.168.1.128"  # 送信先のIPアドレスを指定
    target_port = 80 
    host = target_ip
    main()

import socket
from crypto_investment_SQL import *
import pickle


def handle_client(client_socket):
    while True:
        try:
            request = client_socket.recv(1024).decode('utf-8').split(',')
            print(f"Request received: {request}")

            if request[0] == 'CREATE':
                username = request[1]
                password = request[2]
                initial_deposit = float(request[3])
                create_account(username, password, initial_deposit)
                client_socket.send(f"Welcome {username}! Initial balance: £{initial_deposit:.2f}".encode('utf-8'))

            elif request[0] == 'VIEW':
                accounts = view_accounts()
                client_socket.send(pickle.dumps(accounts))

            elif request[0] == 'ASSET':
                assets = view_assets()
                client_socket.send(pickle.dumps(assets))

            elif request[0] == 'FUNDS':
                username = request[1]
                action = request[2]
                amount = float(request[3])
                deposit_withdraw(username, action, amount)
                client_socket.send(f"Funds {action} successful.".encode('utf-8'))

            elif request[0] == 'BUY':
                username = request[1]
                asset_name = request[2]
                quantity = float(request[3])
                buy_asset(username, asset_name, quantity)
                client_socket.send(f"Bought {quantity} {asset_name}.".encode('utf-8'))

            elif request[0] == 'SELL':
                username = request[1]
                asset_name = request[2]
                quantity = float(request[3])
                sell_asset(username, asset_name, quantity)
                client_socket.send(f"Sold {quantity} {asset_name}.".encode('utf-8'))

            elif request[0] == 'PORTO':
                username = request[1]
                portfolio_summary = view_portfolio(username)
                client_socket.send(pickle.dumps(portfolio_summary))

            elif request[0] == 'EXIT':
                print("Client disconnected.")
                client_socket.close()
                break

        except Exception as e:
            print(f"Error: {e}")
            client_socket.send(pickle.dumps({"error": str(e)}))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 5008))
s.listen(1)
print("Server is running and waiting for connection...")

while True:
    conn, addr = s.accept()
    print(f"Connection established with {addr}")
    conn.send("Welcome to the Crypto Trading Platform!".encode('utf-8'))
    handle_client(conn)

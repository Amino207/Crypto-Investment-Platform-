import socket
import pickle


def create_account(s, username, password, initial_deposit):
    s.send(f'CREATE,{username},{password},{initial_deposit}'.encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))


def view_account(s):
    s.send('VIEW,'.encode('utf-8'))
    accounts = pickle.loads(s.recv(1024))
    print("\nAccount Details:")
    for account in accounts:
        print(f"Username: {account['username']}, Balance: £{account['initial_deposit']:.2f}")


def view_assets(s):
    s.send('ASSET,'.encode('utf-8'))
    assets = pickle.loads(s.recv(1024))
    print("\nAssets:")
    for asset in assets:
        print(f"{asset['asset_name']}: £{asset['price']:.2f}")


def funds(s, username, action, amount):
    s.send(f'FUNDS,{username},{action},{amount}'.encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))


def buy_asset(s, username, asset_name, quantity):
    s.send(f'BUY,{username},{asset_name},{quantity}'.encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))


def sell_asset(s, username, asset_name, quantity):
    s.send(f'SELL,{username},{asset_name},{quantity}'.encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))


def view_portfolio(s, username):
    s.send(f'PORTO,{username},'.encode('utf-8'))
    portfolio = pickle.loads(s.recv(1024))
    print("\nPortfolio Summary:")
    print(portfolio)


def exit_program(s):
    s.send('EXIT,'.encode('utf-8'))
    print("Goodbye!")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5008))
print(s.recv(1024).decode('utf-8'))

while True:
    print("\nMenu:")
    print("1. Create Account")
    print("2. View Accounts")
    print("3. View Assets")
    print("4. Add/Withdraw Funds")
    print("5. Buy Assets")
    print("6. Sell Assets")
    print("7. View Portfolio")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Username: ")
        password = input("Password: ")
        initial_deposit = input("Initial Deposit: ")
        create_account(s, username, password, initial_deposit)
    elif choice == '2':
        view_account(s)
    elif choice == '3':
        view_assets(s)
    elif choice == '4':
        username = input("Username: ")
        action = input("Action (deposit/withdraw): ").lower()
        amount = float(input("Amount: "))
        funds(s, username, action, amount)
    elif choice == '5':
        username = input("Username: ")
        asset_name = input("Asset Name: ")
        quantity = float(input("Quantity: "))
        buy_asset(s, username, asset_name, quantity)
    elif choice == '6':
        username = input("Username: ")
        asset_name = input("Asset Name: ")
        quantity = float(input("Quantity: "))
        sell_asset(s, username, asset_name, quantity)
    elif choice == '7':
        username = input("Username: ")
        view_portfolio(s, username)
    elif choice == '8':
        exit_program(s)
        break

s.close()

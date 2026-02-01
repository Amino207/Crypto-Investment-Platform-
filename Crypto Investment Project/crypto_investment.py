#crypto_investment.py

import mysql.connector as mysql
import datetime

from assets import Assets
import json


#create_account function: This function fetch all user data to creat an account into 'account' dictionary and append all data into 'accounts.txt' file
account = {}
def create_account(username, password, initial_deposit):

    if username in account:
        print(f'Username {username} already exists!')
        return
    else :#buildind the account dictionary
        account[username] = {
        'password': password,
        'initial deposit': initial_deposit,
        }


    #Wrting users data in 'accounts.txt'
    with open('accounts.txt', 'a') as f:
        # Add header only if file is empty
        #tell() == 0 :prevent the header from being written multiple time.
        if f.tell() == 0:
            f.write('Username,Password,Initial Deposit\n')

        # Write account details to file
        f.write(f'{username},{password},{initial_deposit}\n')
    print(f'Welcome {username}!\nyour initial balance is: £{initial_deposit}')



#_________________________________________________________________
#load_account function: This function is designed to fetch and update account data from the accounts.txt file whenever needed.
#                       It ensures that the most recent account details, such as usernames, passwords, and balances, are available
#                       for actions like deposits, withdrawals, or buying and selling assets. By calling this function, the program
#                       can avoid repeating code to read the file and keeps the data consistent across all operations. Additionally,
#                       it can convert the account data into JSON format, making it easy to send information to a server when required.
def load_account():

    with open('accounts.txt', 'r') as f:
        contents = f.readlines() #reading all lines
        keys = contents[0].strip().split(',') #Extracting the header

        for key in keys: #Initializing the dictionary
            account[key] = []

        for data in contents[1:]: #Extraction the rest of values
            values = data.strip().split(',')
            for key, value in zip(keys, values):#Populating Data
                account[key].append(value)

    return json.dumps(account)  # Convert dictionary to JSON string



#----------------------------------------------
#deposit_withdraw function : Is used in the project to manage account balances by allowing users to either add money (deposit) or remove
#                           money (withdraw) from their accounts. It first loads the most recent account data using the load_account function
#                           to ensure all updates are accurate. Then, it checks if the user exists and performs the requested action based on
#                           the current balance. The updated balance is saved back to the file to keep the account records consistent.
#                           This function ensures smooth handling of transactions while preventing issues like overdrafts during withdrawals.

def deposit_withdraw(username,action,amount):
    # Calling load_accounts() fetch  data from account
    load_account()


    if username in account['Username']:
        index_ = account['Username'].index(username) #Getting the index to work with the elements of the list

        #Changing the data type of initial_deposit from string to float
        initial_deposit = float(account['Initial Deposit'][index_])

        #Checking condition for depositing cash
        if action == 'deposit':
            add_deposit = float(amount)
            initial_deposit += add_deposit #Update the initial deposit

        #Checking condition for withdrawing cash
        elif action == 'withdraw':
            withdraw = float(amount)
            # Ensures the balance cannot go negative on withdrawals
            if initial_deposit >= withdraw:
               initial_deposit -= withdraw #Update the initial deposit
            else:
                print("Insufficient funds.")
                return  # Exit if withdrawal is not possible

        # Update the dictionary with the new balance and change the data type to string
        account['Initial Deposit'][index_] = str(initial_deposit)

        #Updates accounts.txt with the new balance.
        with open('accounts.txt', 'w') as f:
            f.write('Username,Password,Initial Deposit\n')
            for username, password, new_balance in zip(account['Username'], account['Password'], account['Initial Deposit']):

                f.write(f"{username},{password},{new_balance}\n")


        print(f"Transaction successful! New balance for {username}: ${initial_deposit}")
    else:
        print("Username not found.")






#--------------------------------------------------------------------------
#load_assets function: Is used to read all available assets from the assets.txt file and create a list of Assets objects. Each object contains
#                      details like the asset's name and current price. It simplifies tasks like displaying available assets, calculating costs
#                      for purchases, and validating if a user's requested asset exists in the market. It avoids repetitive code and makes managing
#                      assets more efficient and consistent.
def load_assets():
    assets = []

    with open('assets.txt', 'r') as f:
        data = f.readlines()
        for l in data:
            name, current_price = l.strip().split(',')
            assets.append(Assets(name, current_price))

    return assets
assets_list = load_assets()



#----------------------------------------------------------------

# The save_transaction function: Is used to log every financial activity performed by the user, such as buying or selling assets.
#                                It records the date and time of the transaction, the username, the type of action (e.g., "buy" or "sell"),
#                                the asset involved, and the quantity. These details are appended to the transactions.txt file, ensuring a
#                                complete history of user activities is maintained. This makes it easy to track past actions, audit transactions,
#                                or display history to the user or a server.

#The reason I implemented save_transaction function before the buy_assets and sell_assets functions to log the transaction details immediately after
#           the user initiates a buy or sell action. This ensures that every transaction is recorded first, maintaining an accurate and real-time history
#           of actions before any changes are made to the account or portfolio.

def save_transaction(username, asset, quantity, action):

    #Transaction entry
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction_entry = f"{current_time},{username},{action},{asset},{quantity}\n"

    # Open the file in append mode
    with open("transactions.txt", "a") as f:
        # Check if the file is empty, and add the header only if it is
        if f.tell() == 0:
            f.write("Date&Time,Username,Action,Asset,Quantity\n")

        # Append the transaction
        f.write(transaction_entry)

    print(f"Transaction saved: {transaction_entry.strip()}")

#--------------------------------------------------------------------------


# Portfolio dictionary
portfolio = {}

# buy_assets function: In the project allows users to purchase assets from the market. It ensures the user has enough balance
#                      in their account by checking the cost of the asset against their available funds. If the user can afford the asset,
#                      the function deducts the cost from their balance, updates their portfolio with the purchased asset and quantity,
#                      and saves the transaction details. This function helps manage asset purchases efficiently and keeps both the account
#                      and portfolio records updated.

def buy_assets(username, asset_name, quantity):
    load_account()  # Load accounts from the file into the account dictionary

    # Check if the user exists in the account dictionary
    if username not in account['Username']:
        print('Username not found.')
        return

    # Find the asset object in the market
    asset = None #Initally I assign as None
    for i in assets_list:
        if i.get_name().capitalize() == asset_name.capitalize():
            asset = i #If user asset is match with the asset in the market then we can go further
            break #When finding the match I want to break the iteration

    # Check if the asset not found
    if not asset:
        print(f'Asset: {asset} not found!')
        return

    else:# When asset matched
        #Calculate the total cost for buy asset
        asset_price = float(asset.get_current_price())
        total_cost = asset_price * quantity


    #Find the user index(since I have a dictionary and store values as list)
    index_ = account['Username'].index(username)
    # Fetching the Initial balance
    balance = float(account['Initial Deposit'][index_])

    #Check if user has sufficient balance to buy asset or not
    if total_cost > balance or balance == 0:
        print('Insufficient funds.')
        return
    else: # if user has enough balance then ...
        # Deduct the cost from the user's balance
        balance -= total_cost
        #Update the account balance after purchasing assets
        account['Initial Deposit'][index_] = str(balance)

    # Update the portfolio quantity
    if username not in portfolio:
        portfolio[username] = {}
    if asset_name in portfolio[username]:
        portfolio[username][asset_name] += quantity
    else:
        portfolio[username][asset_name] = quantity

    # Update balance in the portfolio
    portfolio[username]['Balance'] = balance


    # Updates accounts.txt with the new balance.
    with open('accounts.txt', 'w') as f:
        f.write('Username,Password,Initial Deposit\n')
        for username, password, balance in zip(account['Username'], account['Password'], account['Initial Deposit']):
            f.write(f"{username},{password},{balance}\n")

    print(f"{username} successfully bought {quantity} {asset_name} for £{total_cost:.2f}.")


    # Save the transaction
    save_transaction(username, asset_name, quantity, 'buy')

# buy_assets('amino', 'Matic', 5)
# print(portfolio)
# print(account)



#-------------------------------------------------------------
# sell_assets function : In the project allows users to sell assets they own by fetching information from their asset portfolio,
#                        not their account data. It checks if the user has the specified asset and enough quantity in their portfolio
#                        before proceeding. If the sale is valid, the function calculates the total revenue based on the current market
#                        price, updates the portfolio to reflect the reduced asset quantity, and adds the earned amount to the user's balance.
#                        It also ensures the accounts.txt file is updated with the new balance and records the transaction for future reference.

def sell_assets(username, asset_name, quantity):
    # Check if the user exists in the portfolio
    if username not in portfolio:
        print('Username not found.')
        return

    # Checking the asset exists in the  market
    asset = None
    for i in assets_list:
        if i.get_name().capitalize() == asset_name.capitalize():
            asset = i
            break

    if not asset:
        print(f"Asset '{asset_name}' not found in the market.")
        return


    # Check if the user has the asset in the portfolio
    if asset_name not in portfolio[username]:
        print(f"Asset '{asset_name}' not found in portfolio.")
        return

    # Check if the user has enough of quantity of the asset to sell
    user_current_quantity = portfolio[username][asset_name]
    if quantity <= 0 or user_current_quantity < quantity:
        print('Insufficient quantity of {asset_name} to sell.')
        return

    else:
        #Current asset price
        current_asset_price = float(asset.get_current_price())
        #Calculate total revenue
        total_revenue =  quantity * current_asset_price

        # Update quantity
        portfolio[username][asset_name] -= quantity

        # Update the portfolio
        if portfolio[username][asset_name] <= 0:  # Remove asset if quantity is zero
            del portfolio[username][asset_name]

        #update user's balance in account and portfolio
        index_ = account['Username'].index(username)
        balance = float(account['Initial Deposit'][index_])
        balance += total_revenue
        #Update user's balance in portfolio
        account['Initial Deposit'][index_] = str(balance)
        portfolio[username]['Balance'] = balance

        #Update the account.txt balance
        with open('accounts.txt', 'w') as f:
            f.write('Username,Password,Initial Deposit\n')
            for username, password, balance in zip(account['Username'], account['Password'], account['Initial Deposit']):
                f.write(f"{username},{password},{balance}\n")

        print(f"{username} successfully sold {quantity} {asset_name} for £{total_revenue:.2f}.")

        # Save the transaction
        save_transaction(username, asset_name, quantity, 'sell')

# sell_assets('amino','Matic',50)
# print(portfolio)
# print(account)

#------------------------------------------------
#view_portfolio function: To display a user's portfolio, showing the assets they own, the quantity of each asset,
#                         and the total value based on current market prices. It calculates the overall portfolio value,
#                         skipping the user's balance. This function makes it easy to summarize and share the portfolio information,
#                         either for the user's reference or to send it to a server for further processing or display.
def view_portfolio(username):
    # Check if the username exists in the portfolio
    if username not in portfolio:
        print(f"User '{username}' not found.")
        return

    total_portfolio_value = 0
    portfolio_details = [] #I need to append all data in a list


    for key, value in portfolio[username].items():
        if key == 'Balance': #Skiping Balance since i don't need it
            continue         #protfolio dict(before) => {'amino': {'Matic': 5, 'Balance': 835.0}}
                             #protfolio dict(after) => {'amino': {'Matic': 5}}
        #Since i looped over {'amino': {'Matic': 5}}   key = Matic      value = 5
        quantity = value

        #Find the current price of the asset in user's portfolio
        for asset in assets_list:
            if asset.get_name().capitalize() == key.capitalize(): #Checking if the market list asset match the user's asset
                current_price = float(asset.get_current_price()) #If it matched return the current price
                break # Exit the loop once we find the matching asset (it's optional)


        # Calculate the total value of the asset
        total_value = quantity * current_price
        total_portfolio_value += total_value

        #I added(appended) all details to a list (portfolio_details), which will eventually hold all the assets' details
#        as single line string(I need to transfer data as string into server) and data saved (one string per asset)
        portfolio_details.append(f"{username} - {key}: {quantity} units - Total Value: ${total_value:.2f}")



    #Joining everything as one complete string in separate line in the list the result look like this =>
    # portfolio_details = [
    #                      "Matic: 5 units, Total Value: $50.00",
    #                      "Bitcoin: 1 units, Total Value: $10000.00", ]
    portfolio_summary = "\n".join(portfolio_details)
    portfolio_summary += f"\nTotal Portfolio Value: ${total_portfolio_value:.2f}"

    return portfolio_summary


    # print(f"Total Portfolio Value: ${total_portfolio_value:.2f}")


# view_portfolio('amino')
# print(portfolio)
# print(account)





#-------------------------------------------------------------------






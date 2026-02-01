📖 Project Overview

The Crypto Investment Platform is a Python-based client–server application designed to simulate a basic cryptocurrency investment system.
It allows users to create accounts, manage balances, trade crypto assets, and view portfolios through a graphical user interface.

The project was developed using Python, Tkinter, and MySQL, following a structured and incremental approach.
The system focuses on data consistency, usability, and clear separation of responsibilities between components.
-----------------------------------------------------------------------------------------------------------------------------------------
⚙️ Key Features

- Account creation and management

- Deposit and withdrawal of funds

- Buy and sell cryptocurrency assets

- Portfolio tracking and valuation

- Client–server communication using sockets

- SQL-based data storage

- GUI built with Tkinter

- Error handling and input validation
-----------------------------------------------------------------------------------------------------------------------------------------

📁 Project Structure

├── crypto_investment_SQL.py
├── server.py
├── client_GUI.py
├── assets.py
├── crypto_investment_db.sql

-----------------------------------------------------------------------------------------------------------------------------------------

File Descriptions

🔹 crypto_investment_SQL.py

Handles all database operations:
  - Account creation and validation

  - Asset and transaction management

  - Portfolio updates

  -  Balance tracking

  -  SQL queries and error handling

🔹 server.py

  - Manages client-server communication

  - Uses sockets for data transmission

  - Handles requests such as account access, trades, and portfolio queries

  - Integrates database logic using crypto_investment_SQL.py

  - Transfers data using pickle

🔹 client_GUI.py

  - Tkinter-based graphical interface

  - Allows users to:

  - Create accounts

  - View assets

  - Buy / sell cryptocurrency

  - View portfolio

  - Deposit and withdraw funds

  - Communicates with server via sockets
    

🔹 assets.py

  - Implements Object-Oriented Programming

  - Defines asset structure and related methods

  - Used to manage crypto asset behaviour cleanly
    

🔹 crypto_investment_db.sql

Creates the database schema:

  - accounts – user information and balances

  - assets – available cryptocurrencies and prices

  - transactions – buy/sell records

  - portfolio – asset ownership per user

  - Includes initial asset data
-----------------------------------------------------------------------------------------------------------------------------------------

🧩 Implementation Stages
1️⃣ Initial Text-Based System

User account creation

Asset management using text files

Buy/sell logic

Portfolio tracking

Transaction logging

2️⃣ Object-Oriented Refactoring

Introduced Asset class

Improved data structure and reusability

Cleaner logic and better scalability

3️⃣ Client–Server Model

Server handles data processing

Client handles user interaction

Socket-based communication

Separation of logic and interface

4️⃣ Database Integration

Migrated from text files to MySQL

Improved data consistency

Implemented SQL queries for all operations

5️⃣ GUI Development

Built using Tkinter

Buttons for all major functions

User-friendly interaction

Error messages and validation

-----------------------------------------------------------------------------------------------------------------------------------------
▶️ How to Run the Project
✅ Prerequisites

Python 3.x

MySQL Server

Required Python libraries:

socket
pickle
tkinter
mysql-connector-python

▶️ Steps

1. Run the SQL file to create the database
2. Start server.py
3. Run client_GUI.py

-----------------------------------------------------------------------------------------------------------------------------------------
▶️ Future Improvements
- Improved UI
- Web-based interface
- Better security
- Authentication system
- Using API
- Web scripting 




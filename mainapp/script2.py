import MetaTrader5 as mt5
import pymongo
from pymongo import MongoClient
from datetime import datetime

def fetch_account_data(account_collection, path="C:/Program Files/MetaTrader 5/terminal64.exe"):
    if not mt5.initialize(login=account_collection["login"], server=account_collection["server"], password=account_collection["password"], path=path):
        print(f"initialize() failed for login {account_collection['login']}, error code =", mt5.last_error())
        mt5.shutdown()
        return None

    account = mt5.account_info()
    balance = account.balance
    equity = account.equity
    login = account.login
    server = account.server
    watch_time = mt5.symbol_info_tick("EURUSD").time
    watch_time = datetime.fromtimestamp(watch_time)
    mt5.shutdown()

    account_detail = {
        "login": login,
        "server": server,
        "balance": balance,
        "equity": equity,
        "watch_time": watch_time
    }
    return account_detail

def fetch_and_save_data(path="C:/Program Files/MetaTrader 5/terminal64.exe"):
    print("Hello22")
    mt5.initialize()

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['your_database_name']
    account_collection = db["Accounts"]
    account_details_collection = db["AccountDetails"]
    print("Task has been called")

    def run_fetch_and_save():
        bulk_operations = []
        for account in account_collection.find():
            account_detail = fetch_account_data(account, path)
            if account_detail:
                bulk_operations.append(account_detail)

        if bulk_operations:
            try:
                account_details_collection.insert_many(bulk_operations)
            except Exception as e:
                print("Failed to insert account details:", e)

        print("Account details saved...")

    # Run the loop every 1 minute
    while True:
        run_fetch_and_save()
        time.sleep(60)

if __name__ == "__main__":
    fetch_and_save_data()

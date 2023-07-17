import MetaTrader5 as mt5
import pymongo
from pymongo import MongoClient
from datetime import datetime,timedelta
import threading
import time

db_connection = None

def get_database_connection():
    global db_connection

    if db_connection is None:
        # Create a new database connection
        client = MongoClient("mongodb+srv://ft9ja:BuildGreatSoftware@cluster0.sk0xsnb.mongodb.net/?retryWrites=true&w=majority")
        db_connection = client["ft9ja"]
        db_connection = client["newdb"]

    return db_connection


# def run_fetch_and_save(account_list):
#     db = get_database_connection()
#     account_details_collection = db["AccountDetails"]
#     account_details_collection.insert_many(account_list)
#     print(account_list, "in thread")
#     print("Account details saved...")

def login_and_save(login, server, password, path):
    try:
        db = get_database_connection()
        account_details_collection = db["AccountDetails"]
        if not mt5.initialize(login=login, server=server, password=password, path=path):
            print("initialize() failed for login:", login, ", error code =", mt5.last_error())
            print("Login failed")
            mt5.shutdown()

        account = mt5.account_info()
        balance = account.balance
        equity = account.equity
        login = account.login
        server=account.server
        watch_time = mt5.symbol_info_tick("EURUSD").time
        watch_time = datetime.fromtimestamp(watch_time)
        # mt5.shutdown()

        account_detail = {
            "login": login,
            "server": server,
            "balance": balance,
            "equity": equity,
            "watch_time": watch_time
        }
        account_details_collection.insert_one(account_detail)
        print("saved thread")
    except Exception as e:
        print("Error occurred in thread:", str(e))

def fetch_and_save_data(path="C:/Program Files/MetaTrader 5/terminal64.exe"):
    while True:
        try:
            print("Hello22")
            db = get_database_connection()
            account_collection = db["Accounts"]
            print("Task has been called")
            for account in account_collection.find():
                print(account,"Account")
                if account:
                    fetch_thread = threading.Thread(target=login_and_save, args=(account["login"], account["server"], account["password"], path))
                    fetch_thread.daemon = True
                    fetch_thread.start()            

        except Exception as e:
            print("Error occurred:", str(e))

        # Wait for 30 seconds before running again
        time.sleep(30)

if __name__ == "__main__":
    fetch_and_save_data()

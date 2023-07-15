from django.http import HttpResponse
from .utils import initialize_mt5
import MetaTrader5 as mt5
from .database import get_database_connection
import datetime
from datetime import datetime, timedelta


def fetch_and_save_data(login, server, password,path="C:/Program Files/MetaTrader 5/terminal64.exe"):
    initialize_mt5()
    print("Hello22")   
    db=get_database_connection()
    account_collection = db["Accounts"]
    account_details_collection=db["AccountDetails"]
    account_list=[]
    print("Task has been called")
    # for account_collection in account_collection.find():

    if not mt5.initialize(login=login, server=server, password=password,path=path):
        print("initialize() failed, error code =", mt5.last_error())
        mt5.shutdown()
    # print("Login was successsful")
    # print(account_collection["login"], account_collection["server"],account_collection["password"])
    # if not mt5.initialize(login=account_collection["login"], server=account_collection["server"],password=account_collection["password"],path=path):
    #     print("initialize() failed, error code =", mt5.last_error())
    #     print("Login failed")
    #     mt5.shutdown()
 
    account = mt5.account_info()
    balance = account.balance
    equity = account.equity
    login = account.login
    server=account.server
    watch_time = mt5.symbol_info_tick("EURUSD").time
    watch_time = datetime.fromtimestamp(watch_time)
    mt5.shutdown()
    # Save data to db
    account_detail={
    "login":login,
    "server":server,
    "balance":balance,
    "equity":equity,
    "watch_time":watch_time

    }
    # account_list.append(account_detail)
    account_details_collection.insert_one(account_detail)
    print(account_list, "All availbale accounts")
    print("Account details saved...")


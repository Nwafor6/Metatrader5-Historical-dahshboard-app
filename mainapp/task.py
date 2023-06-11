from django.http import HttpResponse
from .utils import initialize_mt5
import MetaTrader5 as mt5
from .database import get_database_connection
import datetime
from datetime import datetime, timedelta


def fetch_and_save_data():
    initialize_mt5()   
    db=get_database_connection()
    AccountCollections=db["Accounts"]
    account_list=[]
    print("Task has been called")
    # Check if the login was successful 
    for account in AccountCollections.find():
        
        if not mt5.login(login=account["login"], server=account["server"], password=account["password"]):
            print("account-info:",mt5.account_info())
            return HttpResponse("Login failed")
        account = mt5.account_info()
        balance = account.balance
        equity = account.equity
        login = account.login
        server=account.server
        watch_time = mt5.symbol_info_tick("EURUSD").time
        watch_time = datetime.fromtimestamp(watch_time)
        mt5.shutdown()
        print("MT5 section for")
        # Save data to db
        account_detail={
        "login":login,
        "server":server,
        "balance":balance,
        "equity":equity,
        "watch_time":watch_time

        }
        account_list.append(account_detail)
    AccountCollections.insert_many(account_list)
    return HttpResponse("Saved Successfully")
import MetaTrader5 as mt5
import datetime

# Connect to the MetaTrader 5 terminal
if not mt5.initialize(login=22212588, server="Deriv-Demo", password="udas3mvw",path="C:/Program Files/MetaTrader 5/terminal64.exe"):
        print("initialize() failed, error code =", mt5.last_error())
        mt5.shutdown()
# Set the desired date range
start_date = datetime.datetime(2023, 7, 13)
end_date = datetime.datetime(2023, 7, 13)

# Request account information within the date range
account_info = mt5.account_info()
if account_info is not None:
    account_history = mt5.copy_rates_range(account_info.login)
    print(account_history)
    if account_history is not None:
        for bar in account_history:
            print("Date:", datetime.datetime.fromtimestamp(bar[0]))
            print("Open:", bar[1])
            print("High:", bar[2])
            print("Low:", bar[3])
            print("Close:", bar[4])
            print("Volume:", bar[5])
            print("----")

# Disconnect from the MetaTrader 5 terminal
mt5.shutdown()

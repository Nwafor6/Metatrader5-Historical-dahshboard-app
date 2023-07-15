import MetaTrader5 as mt5

def initialize_mt5(login=5014876145, server="MetaQuotes-Demo", password="c2qxofya"):
    # Connect to the MetaTrader 5 terminal
    if not mt5.initialize(login=login, server=server, password=password,path="C:/Program Files/MetaTrader 5/terminal64.exe"):
        print("initialize() failed, error code =", mt5.last_error())
        quit()
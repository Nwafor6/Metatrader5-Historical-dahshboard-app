import MetaTrader5 as mt5

def initialize_mt5():
    # Connect to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
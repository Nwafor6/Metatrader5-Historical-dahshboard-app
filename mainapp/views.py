from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from threading import Thread
import time
from .utils import initialize_mt5
import MetaTrader5 as mt5
from bson import ObjectId
from .task import fetch_and_save_data
from .database import get_database_connection
import datetime
from datetime import datetime, timedelta


# Get Specific account to display
def account_dashboard(request):
    db=get_database_connection()
    AccountCollections=db["Accounts"]
    account_list = []
    login_list=[account["login"] for account in AccountCollections.find()]
    if request.method=="POST":
        login=request.POST["login"]
        for account in AccountCollections.find({"login":login}):
            account["_id"] = str(account["_id"])
            account_list.append(account)
        return JsonResponse({"details":account_list}, status=200, safe=False)
    return render(request, "partials/dashboard.html", {"account":login_list})

def bgtransaction(request):
    thread=Thread(target=fetch_and_save_data)
    thread.start()
    print("Tranfered request")
    return JsonResponse({"detail":"Requested added to queue"})

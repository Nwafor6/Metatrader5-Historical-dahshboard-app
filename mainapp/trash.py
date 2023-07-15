from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from threading import Thread
import time
from .utils import initialize_mt5
import MetaTrader5 as mt5
from bson import ObjectId
from bson import Int64
from .task import fetch_and_save_data
from .database import get_database_connection
import datetime
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from .serializers import AccountSerializer




# Get Specific account to display
@csrf_exempt
def account_dashboard(request):
        
    if request.method == "POST":
        login = request.POST.get("login")
        db = get_database_connection()
        account_collection = db["Accounts"]
        account_details_collection=db["AccountDetails"]
        account_list = []
        account=account_collection.find_one({"login": int(login)})
        thread=Thread(target=fetch_and_save_data, args=(account["login"], account["server"], account["password"]))
        thread.start()
        for account in account_details_collection.find({"login": int(login)}):
            account["_id"] = str(account["_id"])
            account_list.append(account)
        print("Transffered request")

        return JsonResponse({"details": account_list}, status=200)


    else:
        db = get_database_connection()
        account_collection = db["Accounts"]
        login_list = [account['login'] for account in account_collection.find()]
        return JsonResponse({"details": login_list}, status=200)
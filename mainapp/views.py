from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from threading import Thread
import time
# from .utils import initialize_mt5
import MetaTrader5 as mt5
from bson import ObjectId
from bson import Int64
from .task import fetch_and_save_data
from .database import get_database_connection
import datetime
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt




# Get Specific account to display
@csrf_exempt
def account_dashboard(request):
    if request.method == "POST":
        login = request.POST.get("login")

        if login:
            db = get_database_connection()
            account_collection = db["Accounts"]
            account_list = []

            for account in account_collection.find({"login": int(login)}):
                account["_id"] = str(account["_id"])
                account_list.append(account)


            thread=Thread(target=fetch_and_save_data)
            thread.start()
            return JsonResponse({"details": account_list}, status=200)
            
        else:
            return JsonResponse({"error": "Missing login parameter"}, status=400)

    else:
        db = get_database_connection()
        account_collection = db["Accounts"]
        login_list = [account['login'] for account in account_collection.find()]

        return render(request, "partials/dashboard.html", {"login_list": login_list})



# def bgtransaction(request):
#     # thread=Thread(target=fetch_and_save_data)
#     # thread.start()
#     print("Tranfered request")
#     return JsonResponse({"detail":"Requested added to queue"})

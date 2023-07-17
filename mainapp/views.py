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
from bson import ObjectId
import json
from django.core.cache import cache




# Get Specific account to display
# @csrf_exempt
# @cache_page(60 * 5)
# def account_dashboard(request):
        
#     if request.method == "POST":
#         login = request.POST.get("login")
#         db = get_database_connection()
#         account_collection = db["Accounts"]
#         account_details_collection=db["AccountDetails"]
#         account_list = []
#         account=account_collection.find_one({"login": int(login)})
#         thread=Thread(target=fetch_and_save_data, args=(account["login"], account["server"], account["password"]))
#         thread.start()
#         for account in account_details_collection.find({"login": int(login)}):
#             account["_id"] = str(account["_id"])
#             account_list.append(account)
#         print("Transffered request")

#         return JsonResponse({"details": account_list}, status=200)


#     else:
#         db = get_database_connection()
#         account_collection = db["Accounts"]
#         account_details_collection = db["AccountDetails"]
#         login_list = [account['login'] for account in account_collection.find()]
#         # accounts = [json.loads(json.dumps(account, default=str)) for account in account_details_collection.find()]
#         return JsonResponse({"details": login_list}, status=200)

#         # return render(request, "partials/dashboard.html", {"login_list": login_list})

@csrf_exempt
def account_dashboard(request):
    if request.method == "POST":
        login = request.POST.get("login")
        print(login,"Login")
        cached_data = cache.get(f"account_dashboard_{login}")

        if cached_data is None:
            print("Not cahed")
            db = get_database_connection()
            account_collection = db["Accounts"]
            account_details_collection = db["AccountDetails"]
            account_list = []
            account = account_collection.find_one({"login": int(login)})
            if account:
                # thread = Thread(target=fetch_and_save_data, args=(account["login"], account["server"], account["password"]))
                # thread.start()
                print("Account exist")
                for account_detail in account_details_collection.find({"login": int(login)}):
                    account_detail["_id"] = str(account_detail["_id"])
                    account_list.append(account_detail)

                # Cache the data for future requests
                cache.set(f"account_dashboard_{login}", account_list, 60 * 3)  # Cache for 5 minutes

                print("Data fetched from MongoDB")
                return JsonResponse({"details": account_list}, status=200)
            else:
                return JsonResponse({"error": "Account not found"}, status=404)
        else:
            print("Data retrieved from cache")
            print(cached_data,"cached")

        return JsonResponse({"details": cached_data}, status=200)
    else:
        cached_login_list = cache.get("account_login_list")

        if cached_login_list is None:
            db = get_database_connection()
            account_collection = db["Accounts"]
            login_list = [account['login'] for account in account_collection.find()]
            # Cache the login list for future requests
            cache.set("account_login_list", login_list, 60 * 30)  # Cache for 5 minutes

            print("Login list fetched from MongoDB")
        else:
            login_list = cached_login_list
            print("Login list retrieved from cache")

        return JsonResponse({"details": login_list}, status=200)

def home(request):
    return render(request, "mainapp/index.html")

# @csrf_exempt
# def account_dashboard(request):
#     if request.method == "POST":
#         login = request.POST.get("login")

#         if login:
#             db = get_database_connection()
#             account_collection = db["Accounts"]
#             account_details_collection=db["AccountDetails"]
#             account_list = []

#             for account in account_collection.find({"login": int(login)}):
#                 account["_id"] = str(account["_id"])
#                 account_list.append(account)


            # thread=Thread(target=fetch_and_save_data)
            # thread.start()
#             return JsonResponse({"details": account_list}, status=200)
            
#         else:
#             return JsonResponse({"error": "Missing login parameter"}, status=400)

#     else:
#         db = get_database_connection()
#         account_collection = db["Accounts"]
#         login_list = [account['login'] for account in account_collection.find()]

#         return render(request, "partials/dashboard.html", {"login_list": login_list})



# def bgtransaction(request):
#     # thread=Thread(target=fetch_and_save_data)
#     # thread.start()
#     print("Tranfered request")
#     return JsonResponse({"detail":"Requested added to queue"})

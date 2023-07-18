from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from threading import Thread
import time
from .database import get_database_connection
import datetime
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.cache import cache
from bson import ObjectId



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

@csrf_exempt
def adminGetAccount(request):
    if request.method=="POST":
        login=request.POST["login"]
        server=request.POST["server"]
        password=request.POST["password"]

        # Add the new account to the database
        db = get_database_connection()
        account_collection = db["Accounts"]
        account={
            "login":login,
            "server":server,
            "password":password
        }
        addAccount=account_collection.insert_one(account)
        account["_id"] = str(addAccount.inserted_id)
        return JsonResponse({"details": account}, status=201)
    else:
        try:
            cached_account_list = cache.get("account_list")

            if cached_account_list is None:
                print("Fetching account list from MongoDB")
                db = get_database_connection()
                account_collection = db["Accounts"]
                account_list = []
                for account in account_collection.find():
                    account["_id"] = str(account["_id"])
                    account_list.append(account)
                # Cache the account list for future requests
                cache.set("account_list", account_list, 60 * 10)  # Cache for 10 minutes
                return JsonResponse({"details": account_list}, status=201)
            else:
                print("Retrieving account list from cache")
                return JsonResponse({"details":cached_account_list}, status=201)

        except Exception as e:
            print("Error occurred while fetching account list:", str(e))
            return JsonResponse({"error": "An error occurred while fetching account list."}, status=500)



def home(request):
    return render(request, "mainapp/index.html")
def dashboard(request):
    return render(request, "mainapp/admin.html")

from django.shortcuts import render, redirect
import csv
import threading
from imports import check_tree_object
# Create your views here.


def csv_writer(file_name, word1, word2):
    with open(f"{file_name}", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([word1, word2])
    pass


def logout(request):
    request.session['mentor'] = None
    request.session['mentee'] = None
    request.session['adminmm'] = None

    return login(request)


def login(request):

    if request.method == "GET":
        # request.session[f'{status}'] = None
        return render(request, "Login.html")
    if request.method == "POST":
        if request.session.get("isFirst") is None:
            t1 = threading.Thread(target=check_tree_object, args=(request,))
            t1.start()
            
        else:
            request.session["isFirst"] = False
        print(request)
        username = parse_string(request.POST.get("username"))
        password = reverse_parse_string(request.POST.get("password"))

        status = check_credentials(username, password)
        if status != False:
            request.session[f'{status}'] = username
            redirect_url = f"/{status}/{status}/"
            return redirect(redirect_url)
        else:
            return render(request, "Login.html", {"error": "Invalid credentials"})


def check_credentials(username, password):
    with open('logindetails.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            stored_username, stored_password, status = row
            if username.strip() == stored_username.strip() and password.strip() == stored_password.strip():
                return status
    return False


def parse_string(string: str):
    if "," in string:
        string = string.replace(",", "_")
    if "\n" in string:
        string = string.replace("\n", "->")
    if "\r" in string:
        string = string.replace("\r", "<")

    return string


def reverse_parse_string(string: str):
    return string.replace("_", ","). replace("->", "\n").replace("<", "\r")


def forgotpassword(request):
    return render(request, "forgotpassword.html")

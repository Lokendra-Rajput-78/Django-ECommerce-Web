from django.shortcuts import render
import json
from django.http import JsonResponse, Http404
from pathlib import Path
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from allauth.account.models import EmailAddress


BASE = Path(__file__).resolve().parent.parent


# Create your views here.
def about(request):
    return render(request, "about.html")

def login_register(request):
    return render(request, "login.html")

def register_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return JsonResponse({"status":"error","msg":"Gmail already exists"})

        username = email.split("@")[0]  # auto username

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return JsonResponse({"status":"success","msg":"Account created successfully!"})


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            username = User.objects.get(email=email).username
        except:
            return JsonResponse({"status":"error","msg":"Gmail not found!"})

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({"status":"error","msg":"Wrong password!"})

        login(request, user)
        return JsonResponse({"status":"success","msg":"Login successful!"})



def logout_user(request):
    logout(request)
    return redirect("/")


def load_products():
    with open(BASE / "myapp/static/data/products.json" , encoding="utf-8") as f:
        return json.load(f)

def index(request):
    data = load_products()

    cat = request.GET.get("cat", "he")  # default = he

    trend = []
    ms = []

    if cat == "he":
        for item in data["heData_trend"]:
            item["cat"] = "he"
            trend.append(item)

        for item in data["heData_MS"]:
            item["cat"] = "he"
            ms.append(item)

        theme = "he-theme"

    else:  # she
        for item in data["sheData_trend"]:
            item["cat"] = "she"
            trend.append(item)

        for item in data["sheData_MS"]:
            item["cat"] = "she"
            ms.append(item)

        theme = "she-theme"

    return render(request, "index.html", {
        "trend": trend,
        "ms": ms,
        "active_cat": cat,
        "theme": theme
    })


def product_detail(request, cat, id):
    data = load_products()

    # Correct dataset selection
    if cat == "he":
        products = data["heData_trend"] + data["heData_MS"]
    else:
        products = data["sheData_trend"] + data["sheData_MS"]

    # Find product
    item = next((p for p in products if p["id"] == id), None)

    if not item:
        raise Http404("Product Not Found")

    related = [p for p in products if p["id"] != id][:6]

    return render(request, "product_detail.html", {
        "p": item,
        "related": related,
        "cat": cat
    })



def profile(request):
    user = request.user

    social = None
    pic = None
    email = ""

    if user.is_authenticated:

        # 1) GOOGLE PHOTO
        social = user.socialaccount_set.first()
        if social:
            pic = social.get_avatar_url()

        # 2) EMAIL (MOST RELIABLE)
        # Get from EmailAddress table (Allauth stores verified email here)
        email_obj = EmailAddress.objects.filter(user=user).first()
        if email_obj:
            email = email_obj.email
        else:
            # fallback
            email = user.email

    return render(request, "profile.html", {
        "name": user.first_name,
        "last_name": user.last_name,
        "email": email,
        "pic": pic
    })

    user = request.user

    social = None
    pic = None

    if user.is_authenticated:
        social = user.socialaccount_set.first()
        if social:
            pic = social.get_avatar_url()

                        # GOOGLE EMAIL (most reliable)
            google_email = social.extra_data.get("email")
            if google_email:
                email = google_email

    return render(request, "profile.html", {
        "name": user.first_name, 
        "last_name" : user.last_name,
        "email": user.email,
        "pic": pic
    })



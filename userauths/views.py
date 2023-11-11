from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import User
from .forms import UserRegisterForm

def register_view(request ,*args,  **kwargs):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Hey {username}, your account was created successfully")
            new_user = authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password1"])
            login(request, new_user)
            return redirect("core:index")
    elif request.user.is_authenticated:
        messages.warning(request, "You are adreadly logged in!")
        return redirect("core:index")
    context = {
        'form': form
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("core:index")
            else:
                messages.warning(request, "Username or password is not exist.")
                return redirect("userauths:sign-in")
        except:
             messages.warning(request, "User does not exist.")
            
    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You already logout.")
    return redirect("userauths:sign-in")

    
    
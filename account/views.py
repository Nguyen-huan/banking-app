from django.shortcuts import render, redirect
from django.contrib import messages

from account.forms import KYCForm
from .models import Account, KYC
from core.forms import CreditCardForm
from core.models import CreditCard
def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your KYC")
            return redirect("account:kyc-reg")
        account = Account.objects.get(user=request.user)
    else:
        messages.warning(request, "You need to login to access the dashboard!")
        return redirect("userauths:sign-in")
        
    context = {
        "account":account,
        "kyc":kyc
    }
    return render(request, "account/account.html", context)

def kyc_regisration(request):
    user = request.user
    account = Account.objects.get(user=user)
    
    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None
    
    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "KYC Form submited successfully, In Review Now")
            return redirect("core:index")
    else:
        form = KYCForm(instance=kyc)
    context = {
        "account":account,
        "form": form,
        "kyc":kyc,
    }
    return render(request, "account/kyc-form.html", context)
    

def dashboard(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your KYC")
            return redirect("account:kyc-reg")
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user)
        print(credit_card)
        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user 
                new_form.save()
                
                
                card_id = new_form.card_id
                messages.success(request, "Card Added Successfully.")
                return redirect("account:dashboard")
        else:
            form = CreditCardForm()
    else:
        messages.warning(request, "You need to login to access the dashboard!")
        return redirect("userauths:sign-in")
        
    context = {
        "account":account,
        "kyc":kyc,
        "form":form,
        'credit_card':credit_card
    }
    return render(request, "account/dashboard.html", context)
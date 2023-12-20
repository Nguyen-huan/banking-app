from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from account.models import Account
from core.models import CreditCard

def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    context = {
        'account':account,
        'credic_card':credit_card
    }
    return render(request, "credit_card/credit-card.html", context)

def delete_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    
    # New Feature
    # BEfore deleting card, it'll be nice to transfer all the money from the card to the main account balance.
    account = request.user.account
    
    if credit_card.amount > 0:
        account.account_balance += credit_card.amount
        account.save()
        messages.success(request, "The money in your card has been transferred to your account")
    
    credit_card.delete()
    messages.success(request, "Card Deleted Successfull")
    return redirect("account:dashboard")


def fund_credit_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account
    
    if request.method == "POST":
        amount = request.POST.get("funding_amount") 
        
        if Decimal(amount) <= account.account_balance:
            account.account_balance -= Decimal(amount) 
            account.save()
            
            credit_card.amount += Decimal(amount)
            credit_card.save()
            
            messages.success(request, "Funding Successfull")
            messages.success(request, f"Current balance is ${account.account_balance}")
            return redirect("core:card-detail", credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Funds")
            return redirect("core:card-detail", credit_card.card_id)
        

def withdraw_fund(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        print(amount)

        if credit_card.amount >= Decimal(amount) and credit_card.amount != 0.00:
            account.account_balance += Decimal(amount)
            account.save()

            credit_card.amount -= Decimal(amount)
            credit_card.save()

            messages.success(request, "Withdrawal Successfull")
            messages.success(request, f"Current balance is ${account.account_balance}")
            return redirect("core:card-detail", credit_card.card_id)
        elif credit_card.amount == 0.00:
            messages.warning(request, "Insufficient Funds")
            return redirect("core:card-detail", credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Funds")
            return redirect("core:card-detail", credit_card.card_id)
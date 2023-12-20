from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal

from .models import Transaction
from account.models import Account

@login_required
def search_user_request(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")
    if query:
        account = Account.objects.filter(
            Q(account_number=query) | Q(account_id=query)
        ).distinct()
    context = {
        'account':account,
        "query":query
    }
    return render(request, "payment_request/search-user.html", context)


@login_required
def amount_request(request, account_number):
    account = Account.objects.get(account_number=account_number)
    context = {
        'account':account,
    }
    return render(request, "payment_request/amount-request.html", context)


@login_required
def amount_request_process(request, account_number):
    account = Account.objects.get(account_number=account_number)

    sender = request.user
    receiver = account.user

    request_sender_account = request.user.account
    request_receiver_account = account

    if request.method == "POST":
        amount = request.POST.get("amount-request")
        description = request.POST.get("description")
        new_request = Transaction.objects.create(
            user = request.user,
            amount = amount,
            description = description,
            receiver = receiver,
            sender = sender,
            sender_account = request_sender_account,
            receiver_account = request_receiver_account,
            status = "request_proccessing",
            transaction_type="request"
        )
        new_request.save()
        transaction_id = new_request.transaction_id
        return redirect("core:amount-request-confirmation", account.account_number, transaction_id)
    else:
        messages.warning(request, "Error Occured! Try again later!")
        return redirect("account:dashboard")
    

def amount_request_confirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transaction does not exist!")
        return redirect("core:request-search-account")
    context = {
        'account':account,
        'transaction':transaction,

    }
    return render(request, "payment_request/amount-request-confirmation.html", context)

def amount_request_final_process(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        sender_account = request.user.account
    except:
        messages.warning(request, "An Occured, Try again.")
        return redirect("account:dashboard")
    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if sender_account.pin_number == pin_number:
            transaction.status = "request_sent"
            transaction.save()
            messages.success(request, "Your payment request have been successfully!")
            return redirect("core:amount-request-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Inconnect Pin Number.", )
            return redirect("core:transfer-confirmation",account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "An Occured, Try again.")
        return redirect("account:dashboard")
    

def request_completed(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "An Occured, Try again.")
        return redirect("account:dashboard")
    context = {
        'account':account,
        'transaction':transaction,
    }
    return render(request, "payment_request/amount-request-completed.html", context)


def settlement_confirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "An Occured, Try again.")
        return redirect("account:dashboard")
    context = {
        'account':account,
        'transaction':transaction,
    }
    return render(request, "payment_request/settlement-confirmation.html", context)

def settlement_processing(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        sender = request.user
        sender_account = request.user.account

        if request.method == "POST":
            pin_number = request.POST.get("pin-number")
            if pin_number == request.user.account.pin_number:
                if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
                    messages.warning(request, "Insufficient Funds, fund your account and try angain.")
                else:
                    sender_account.account_balance -= transaction.amount
                    sender_account.save()

                    account.account_balance += transaction.amount
                    account.save()

                    transaction.status = "request_settled"
                    transaction.save()
                    messages.success(request, f"Settled to {account.user.kyc.full_name} was successfully!")
                    return redirect("core:settlement-completed",account.account_number, transaction.transaction_id)

            else:
                messages.warning(request, f"Incorrect Pin!")
                return redirect("core:settlement-confirmation" ,account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, f"Error Occured!")
            return redirect("account:dashboard")
    except:
        messages.warning(request, "An Occured, Try again.")
        return redirect("account:dashboard")
    context = {
            'account':account,
            'transaction':transaction,
        }
    return render(request, "payment_request/settlement-confirmation.html", context)


def settlement_completed(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "An Occured, Try again.")
        return redirect("account:dashboard")
    context = {
        'account':account,
        'transaction':transaction,
    }
    return render(request, "payment_request/settlement_complete.html", context)



def delete_payment_request(request, transaction_id):
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        if request.user == transaction.user:
            transaction.delete()
            messages.success(request, "Paymet request delete successfully!")
            return redirect("core:transactions")
    except:
        messages.warning(request, "An Occured, Try again.")
        return redirect("account:dashboard")
    context = {
        'transaction':transaction,
    }
    return render(request, "payment_request/settlement_complete.html", context)
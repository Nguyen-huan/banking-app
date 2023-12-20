from django.urls import path
from . import credit_card, views, transfer, transaction, payment_request


app_name="core"
urlpatterns = [
    path('', views.index, name = "index"),

    path('search-account/', transfer.search_users_account_number, name = "search-account"),
    path('amount-transfer/<amount_number>/', transfer.amount_transfer, name = "amount-transfer"),
    path('amount-transfer-process/<account_number>/', transfer.amount_transfer_proccess, name = "amount-transfer-process"),
    path('transfer-confirmation/<account_number>/<transaction_id>/', transfer.transfer_confirmation, name = "transfer-confirmation"),
    path('transfer-process/<account_number>/<transaction_id>/', transfer.transfer_proccess, name = "transfer-process"),
    path('transfer-completed/<account_number>/<transaction_id>/', transfer.transfer_completed, name = "transfer-completed"),

    path('transactions/', transaction.get_transactions_list, name = "transactions"),
    path('transaction_detail/<transaction_id>/', transaction.transaction_detail, name = "transaction_detail"),

    # Payment Request
    path('request-search-account/', payment_request.search_user_request, name = "request-search-account"),
    path('amount-request/<account_number>/', payment_request.amount_request, name = "amount-request"),
    path('amount-request-process/<account_number>/', payment_request.amount_request_process, name = "amount-request-process"),
    path('amount-request-confirmation/<account_number>/<transaction_id>/', payment_request.amount_request_confirmation, name = "amount-request-confirmation"),
    path('amount-request-final-process/<account_number>/<transaction_id>/', payment_request.amount_request_final_process, name = "amount-request-final-process"),
    path('amount-request-completed/<account_number>/<transaction_id>/', payment_request.request_completed, name = "amount-request-completed"),
    

    # Request Settlement
    path('settlement-confirmation/<account_number>/<transaction_id>/', payment_request.settlement_confirmation, name = "settlement-confirmation"),
    path('settlement-processing/<account_number>/<transaction_id>/', payment_request.settlement_processing, name = "settlement-processing"),
    path('settlement-completed/<account_number>/<transaction_id>/', payment_request.settlement_completed, name = "settlement-completed"),
    path('delete-payment-request/<transaction_id>/', payment_request.delete_payment_request, name = "delete-payment-request"),

    # Credit Card
    path('card-detail/<card_id>/', credit_card.card_detail, name = "card-detail"),
    path("fund-credit-card/<card_id>/", credit_card.fund_credit_card, name="fund-credit-card"),
    path("withdraw_fund/<card_id>/", credit_card.withdraw_fund, name="withdraw_fund"),
    path("delete_card/<card_id>/", credit_card.delete_card, name="delete_card"),














]
from django.urls import path
from . import views
from . import transfer
from . import transaction


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
    path('transaction_detail/<transaction_id>', transaction.transaction_detail, name = "transaction_detail"),






]
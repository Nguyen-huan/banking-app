from django.db import models
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField
import uuid

from userauths.models import User

ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("in-active", "In-active")
)

MARITAL_STATUS = (
    ("married", "Married"),
    ("single", "Single"),
    ("other", "Other")
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)


IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s" % (instance.id, ext)
    return f"user_{instance.user.id}/{filename}"

class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_number = ShortUUIDField(unique=True ,length=10, max_length=25, prefix="217", alphabet="1234567890")
    account_id = ShortUUIDField(unique=True ,length=7, max_length=25, prefix="DEX", alphabet="1234567890") # Sử dụng trong các giao dịch 
    pin_number = ShortUUIDField(unique=True ,length=4, max_length=7, alphabet="1234567890")
    red_code = ShortUUIDField(unique=True ,length=10, max_length=10, alphabet="abcdefgh1234567890") #Mã này có thể được sử dụng trong các quy trình xác thực, chẳng hạn như khi xác nhận một giao dịch quan trọng hoặc khi thực hiện các thao tác quan trọng liên quan đến tài khoản.
    account_status = models.CharField(max_length=100 ,choices=ACCOUNT_STATUS, default="in-active")
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="recommended_by")
    
    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user}"


class KYC(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="kyc", default="default.png")
    marital_status = models.CharField(choices=MARITAL_STATUS, max_length=40)
    gender = models.CharField(choices=GENDER, max_length=40)
    identity_type = models.CharField(choices=IDENTITY_TYPE, max_length=140)
    identity_image = models.ImageField(upload_to="kyc", blank=True, null=True)
    date_of_birth = models.DateField(auto_now_add=False)
    signature = models.ImageField(upload_to="kyc")

    # Address
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    # Contact detail
    mobile = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    
    

# Hàm xử lý tín hiệu
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

def save_account(sender, instance, **kwargs):
    instance.account.save()

post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)

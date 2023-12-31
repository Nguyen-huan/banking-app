# Generated by Django 4.0.10 on 2023-11-26 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0007_kyc_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=15, max_length=20, prefix='TRN', unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('desciption', models.CharField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(choices=[('failed', 'Failed'), ('completed', 'Completed'), ('pending', 'Pending'), ('processing', 'Processing')], default='pending', max_length=100)),
                ('transaction_type', models.CharField(choices=[('transfer', 'Transfer'), ('recieved', 'Recieved'), ('withdraw', 'Withdraw'), ('refund', 'Refund'), ('request', 'Request'), ('none', 'Rone')], default='none', max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('update', models.DateField(blank=True, null=True)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('receiver_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver_account', to='account.account')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('sender_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender_account', to='account.account')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

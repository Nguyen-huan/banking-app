# Generated by Django 4.0.10 on 2023-11-15 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_account_red_code_kyc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kyc',
            name='image',
        ),
        migrations.AddField(
            model_name='kyc',
            name='identity_image',
            field=models.ImageField(blank=True, null=True, upload_to='kyc'),
        ),
    ]
# Generated by Django 4.0.10 on 2023-11-15 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_kyc_image_kyc_identity_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='image',
            field=models.ImageField(default='default.png', upload_to='kyc'),
        ),
    ]
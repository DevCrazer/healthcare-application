# Generated by Django 4.0.6 on 2022-08-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sslcommerz', '0002_remove_payment_name_payment_patient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='patient',
        ),
        migrations.AddField(
            model_name='payment',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

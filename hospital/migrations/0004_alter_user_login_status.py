# Generated by Django 4.0.6 on 2022-09-14 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_user_login_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login_status',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.1 on 2023-03-26 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login_count',
            field=models.PositiveIntegerField(max_length=100, null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-25 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_alter_order_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='food_name',
            field=models.CharField(max_length=50),
        ),
    ]

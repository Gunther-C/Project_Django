# Generated by Django 5.0 on 2024-08-24 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_environment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
